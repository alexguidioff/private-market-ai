"""Audit SEC Form C as a PiT acquisition block on 2021/2022 only."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

BASE_URL = (
    "https://www.sec.gov/files/dera/data/crowdfunding-offerings-data-sets/"
    "{year}q{quarter}_cf.zip"
)
USER_AGENT = "Private-Market-AI academic research alexguidioff@gmail.com"
ALLOWED_SPLITS = {"future_train": 2369, "future_validation": 2243}
COHORT_COLUMNS = ["accession_number", "cik", "filing_time", "decision_time", "split"]
SOURCE_TABLES = ["FORM_C_SUBMISSION.tsv", "FORM_C_DISCLOSURE.tsv"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quarters(start_year: int, end_year: int):
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            if year == 2016 and quarter < 2:
                continue
            yield year, quarter


def download(url: str, target: Path) -> None:
    if target.exists() and target.stat().st_size > 0:
        return
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                target.write_bytes(response.read())
            time.sleep(0.15)
            return
        except (TimeoutError, urllib.error.URLError):
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)

def locate(archive: zipfile.ZipFile, filename: str) -> str:
    expected = filename.upper()
    matches = [name for name in archive.namelist() if Path(name).name.upper() == expected]
    if len(matches) != 1:
        raise ValueError(f"Expected one {filename}, found {matches}")
    return matches[0]


def read_tsv(archive: zipfile.ZipFile, filename: str) -> pd.DataFrame:
    with archive.open(locate(archive, filename)) as stream:
        return pd.read_csv(stream, sep="\t", dtype=str, low_memory=False)


def clean_cik(series: pd.Series) -> pd.Series:
    return series.fillna("").str.replace(r"\D", "", regex=True).str.lstrip("0").replace("", pd.NA)


def load_cohort(path: Path) -> pd.DataFrame:
    cohort = pd.read_csv(path, usecols=COHORT_COLUMNS, dtype={"cik": str, "split": str})
    unexpected = set(cohort["split"].dropna().unique()) - set(ALLOWED_SPLITS) - {"locked_test"}
    if unexpected:
        raise AssertionError(f"Unexpected splits: {sorted(unexpected)}")
    counts = cohort["split"].value_counts().to_dict()
    expected_all = {**ALLOWED_SPLITS, "locked_test": 914}
    if counts != expected_all:
        raise AssertionError(f"Unexpected split counts: {counts}")
    cohort = cohort[cohort["split"].isin(ALLOWED_SPLITS)].copy()
    if cohort["split"].value_counts().to_dict() != ALLOWED_SPLITS:
        raise AssertionError("Development/validation split counts changed")
    cohort["cik"] = clean_cik(cohort["cik"])
    cohort["decision_time"] = pd.to_datetime(cohort["decision_time"], format="mixed", errors="raise")
    if cohort["cik"].isna().any() or cohort["cik"].duplicated().any():
        raise AssertionError("Cohort CIK is missing or duplicated")
    return cohort


def load_source(raw_dir: Path, start_year: int, end_year: int):
    submissions, disclosures, manifests = [], [], []
    raw_dir.mkdir(parents=True, exist_ok=True)
    for year, quarter in quarters(start_year, end_year):
        target = raw_dir / f"{year}q{quarter}_cf.zip"
        url = BASE_URL.format(year=year, quarter=quarter)
        download(url, target)
        with zipfile.ZipFile(target) as archive:
            submission = read_tsv(archive, "FORM_C_SUBMISSION.tsv")
            disclosure = read_tsv(archive, "FORM_C_DISCLOSURE.tsv")
        submission.columns = submission.columns.str.upper()
        disclosure.columns = disclosure.columns.str.upper()
        submissions.append(submission[["ACCESSION_NUMBER", "SUBMISSION_TYPE", "FILING_DATE", "CIK"]])
        numeric = [column for column in disclosure.columns if column != "ACCESSION_NUMBER"]
        disclosure = disclosure[["ACCESSION_NUMBER", *numeric]].copy()
        disclosures.append(disclosure)
        manifests.append({
            "quarter": f"{year}Q{quarter}", "url": url, "bytes": target.stat().st_size,
            "sha256": sha256(target), "submission_rows": len(submission),
        })
    source = pd.concat(submissions, ignore_index=True)
    source["cik"] = clean_cik(source["CIK"])
    source["filing_date"] = pd.to_datetime(source["FILING_DATE"], format="%Y%m%d", errors="raise")
    source = source.rename(columns={"ACCESSION_NUMBER": "formc_accession", "SUBMISSION_TYPE": "formc_type"})
    disclosure = pd.concat(disclosures, ignore_index=True).rename(
        columns={"ACCESSION_NUMBER": "formc_accession"}
    )
    source = source.merge(disclosure, on="formc_accession", how="left", validate="one_to_one")
    return source, manifests

def run(args) -> dict:
    cohort = load_cohort(args.cohort)
    source, manifests = load_source(args.raw_dir, args.start_year, args.end_year)
    source = source[source["cik"].notna()].copy()
    joined = cohort[["cik", "decision_time", "split"]].merge(source, on="cik", how="left")
    joined["known_by_decision"] = (
        joined["formc_accession"].notna() & (joined["filing_date"] <= joined["decision_time"])
    )
    known = joined[joined["known_by_decision"]].copy()
    issuer = known.groupby(["cik", "split"], as_index=False).agg(
        known_formc_filings=("formc_accession", "nunique"),
        first_formc_date=("filing_date", "min"),
        latest_formc_date=("filing_date", "max"),
        known_formc_types=("formc_type", lambda values: "|".join(sorted(set(values.dropna())))),
    )
    base = cohort[["cik", "decision_time", "split"]].merge(
        issuer, on=["cik", "split"], how="left", validate="one_to_one"
    )
    base["known_formc_filings"] = base["known_formc_filings"].fillna(0).astype(int)
    base["formc_available_by_decision"] = base["known_formc_filings"].gt(0)
    coverage = {}
    for split, expected in ALLOWED_SPLITS.items():
        part = base[base["split"].eq(split)]
        matched = int(part["formc_available_by_decision"].sum())
        coverage[split] = {"cohort_rows": expected, "matched_issuers": matched, "coverage": matched / expected}
    useful_columns = [column for column in source.columns if column not in {
        "formc_accession", "formc_type", "FILING_DATE", "CIK", "cik", "filing_date"
    }]
    known_disclosure = known[useful_columns] if useful_columns else pd.DataFrame()
    nonmissing = {
        column: float(known_disclosure[column].notna().mean())
        for column in useful_columns if known_disclosure[column].notna().any()
    }
    matched_dev = coverage["future_train"]["matched_issuers"]
    report = {
        "scope": "future_train 2021 and future_validation 2022 only; locked_test excluded",
        "locked_test_accessed": False,
        "source": "official SEC Crowdfunding Offerings quarterly data sets",
        "source_period": f"{args.start_year}Q2-{args.end_year}Q4",
        "matching_rule": "exact SEC issuer CIK only; no name matching",
        "available_time_rule": "Form C FILING_DATE <= Form D decision_time",
        "quarter_count": len(manifests),
        "source_submission_rows": int(len(source)),
        "source_unique_ciks": int(source["cik"].nunique()),
        "coverage_by_split": coverage,
        "known_formc_rows_by_decision": int(len(known)),
        "known_submission_types": sorted(known["formc_type"].dropna().unique().tolist()),
        "disclosure_nonmissing_rate_among_known_rows": nonmissing,
        "manual_review_required": False,
        "minimum_development_matches": args.minimum_development_matches,
        "data_gate_pass": matched_dev >= args.minimum_development_matches,
        "block_decision": (
            "coverage gate pass; proceed to feature/source-version freeze before modelling"
            if matched_dev >= args.minimum_development_matches
            else "coverage gate fail; do not run a VoI experiment"
        ),
        "hashes": {"cohort_sha256": sha256(args.cohort), "script_sha256": sha256(Path(__file__))},
        "source_archives": manifests,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    base.to_csv(args.output_dir / "formc_match_audit.csv", index=False)
    (args.output_dir / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["summary_sha256"] = sha256(args.output_dir / "summary.json")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort", type=Path, default=Path(
        "datasets/processed/sec_form_d_future_2021_2023/p1_first_anchor_model_ready.csv"
    ))
    parser.add_argument("--raw-dir", type=Path, default=Path("datasets/raw/sec_form_c"))
    parser.add_argument("--output-dir", type=Path, default=Path(
        "datasets/processed/sec_form_d_future_2021_2023/formc_audit"
    ))
    parser.add_argument("--start-year", type=int, default=2016)
    parser.add_argument("--end-year", type=int, default=2023)
    parser.add_argument("--minimum-development-matches", type=int, default=100)
    print(json.dumps(run(parser.parse_args()), indent=2))


if __name__ == "__main__":
    main()
