"""Build a privacy-minimized, point-in-time SEC Form D research dataset."""
from __future__ import annotations

import argparse
import io
import json
import sqlite3
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

BASE_URL = "https://www.sec.gov/files/structureddata/data/form-d-data-sets/{year}q{quarter}_d.zip"
LEGACY_URL = "https://www.sec.gov/files/structureddata/data/form-d-data-sets/{year}q{quarter}_d_0.zip"
USER_AGENT = "Private-Market-AI academic research alexguidioff@gmail.com"
TECH_INDUSTRIES = {
    "Other Technology", "Computers", "Telecommunications", "Business Services",
}
US_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY","DC",
}


def quarters(start_year: int, end_year: int, end_quarter: int):
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            if year == end_year and quarter > end_quarter:
                return
            yield year, quarter


def download(url: str, target: Path) -> bool:
    if target.exists() and target.stat().st_size > 0:
        return True
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                target.write_bytes(response.read())
            time.sleep(0.15)
            return True
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return False
            if error.code not in {403, 429, 500, 502, 503, 504} or attempt == 3:
                raise
        except (TimeoutError, urllib.error.URLError):
            if attempt == 3:
                raise
        time.sleep(2 ** attempt)
    return False
def locate_member(archive: zipfile.ZipFile, filename: str) -> str:
    matches = [name for name in archive.namelist() if Path(name).name.upper() == filename.upper()]
    if len(matches) != 1:
        raise ValueError(f"Expected one {filename}, found {matches}")
    return matches[0]


def read_table(archive_path: Path, filename: str) -> pd.DataFrame:
    with zipfile.ZipFile(archive_path) as archive:
        with archive.open(locate_member(archive, filename)) as stream:
            return pd.read_csv(stream, sep="\t", dtype=str, low_memory=False)


def clean_bool(series: pd.Series) -> pd.Series:
    return series.fillna("").str.strip().str.lower().isin({"true", "yes", "1"}).astype("int8")


def clean_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.replace({"Indefinite": np.nan, "": np.nan}), errors="coerce")


def load_all(raw_dir: Path, start_year: int, end_year: int, end_quarter: int):
    submissions, issuers, offerings, loaded, missing = [], [], [], [], []
    for year, quarter in quarters(start_year, end_year, end_quarter):
        archive = raw_dir / f"{year}q{quarter}_d.zip"
        found = download(BASE_URL.format(year=year, quarter=quarter), archive)
        if not found:
            found = download(LEGACY_URL.format(year=year, quarter=quarter), archive)
        if not found:
            missing.append(f"{year}Q{quarter}")
            print(f"missing official archive {year} Q{quarter}")
            continue
        submissions.append(read_table(archive, "FORMDSUBMISSION.tsv"))
        issuers.append(read_table(archive, "ISSUERS.tsv"))
        offerings.append(read_table(archive, "OFFERING.tsv"))
        loaded.append(f"{year}Q{quarter}")
        print(f"loaded {year} Q{quarter}")
    if not loaded:
        raise RuntimeError("No SEC Form D archives loaded")
    return (pd.concat(submissions, ignore_index=True), pd.concat(issuers, ignore_index=True),
            pd.concat(offerings, ignore_index=True), loaded, missing)


def build_filings(submissions: pd.DataFrame, issuers: pd.DataFrame, offerings: pd.DataFrame):
    primary = issuers[issuers["IS_PRIMARYISSUER_FLAG"].fillna("").str.upper().eq("YES")].copy()
    primary = primary.sort_values(["ACCESSIONNUMBER", "ISSUER_SEQ_KEY"]).drop_duplicates("ACCESSIONNUMBER")
    issuer_columns = ["ACCESSIONNUMBER", "CIK", "ENTITYNAME", "CITY", "STATEORCOUNTRY",
                      "JURISDICTIONOFINC", "ENTITYTYPE", "YEAROFINC_TIMESPAN_CHOICE",
                      "YEAROFINC_VALUE_ENTERED"]
    filing = submissions.merge(primary[issuer_columns], on="ACCESSIONNUMBER", how="inner", validate="one_to_one")
    filing = filing.merge(offerings, on="ACCESSIONNUMBER", how="inner", validate="one_to_one")
    # SEC changed from ISO timestamps to DD-MON-YYYY during the archive window.
    filing["filing_time"] = pd.to_datetime(filing["FILING_DATE"], errors="coerce", format="mixed")
    filing["sale_date"] = pd.to_datetime(filing["SALE_DATE"], errors="coerce", format="mixed")
    filing["is_amendment"] = clean_bool(filing["ISAMENDMENT"])
    filing["is_equity"] = clean_bool(filing["ISEQUITYTYPE"])
    filing["is_debt"] = clean_bool(filing["ISDEBTTYPE"])
    filing["is_pooled_fund"] = clean_bool(filing["ISPOOLEDINVESTMENTFUNDTYPE"])
    filing["is_business_combination"] = clean_bool(filing["ISBUSINESSCOMBINATIONTRANS"])
    filing["total_offering_amount"] = clean_number(filing["TOTALOFFERINGAMOUNT"])
    filing["total_amount_sold"] = clean_number(filing["TOTALAMOUNTSOLD"])
    filing["investor_count"] = clean_number(filing["TOTALNUMBERALREADYINVESTED"])
    filing["is_us"] = filing["STATEORCOUNTRY"].isin(US_CODES).astype("int8")
    filing["is_technology"] = filing["INDUSTRYGROUPTYPE"].isin(TECH_INDUSTRIES).astype("int8")
    return filing
def build_cohort(
    filing: pd.DataFrame, anchor_start: int, anchor_end: int, coverage_buffer_months: int = 0
):
    observation_end = filing["filing_time"].max()
    label_coverage_end = observation_end - pd.DateOffset(months=coverage_buffer_months)
    new_notice = filing[(filing["is_amendment"] == 0) & filing["filing_time"].notna()].copy()
    new_notice = new_notice.sort_values(["CIK", "filing_time", "ACCESSIONNUMBER"])
    new_notice["prior_notice_count"] = new_notice.groupby("CIK").cumcount()
    new_notice["days_since_prior_notice"] = new_notice.groupby("CIK")["filing_time"].diff().dt.days
    new_notice["next_notice_time"] = new_notice.groupby("CIK")["filing_time"].shift(-1)
    new_notice["days_to_next_notice"] = (new_notice["next_notice_time"] - new_notice["filing_time"]).dt.days
    anchor = new_notice[
        new_notice["filing_time"].dt.year.between(anchor_start, anchor_end)
        & (new_notice["is_us"] == 1)
        & (new_notice["is_technology"] == 1)
        & (new_notice["is_pooled_fund"] == 0)
        & (new_notice["is_business_combination"] == 0)
    ].copy()
    anchor["decision_time"] = anchor["filing_time"] + pd.DateOffset(months=12)
    anchor["label_window_end"] = anchor["decision_time"] + pd.DateOffset(months=18)
    anchor["observation_end"] = observation_end
    anchor["label_coverage_end"] = label_coverage_end
    anchor["label_window_complete"] = (anchor["label_window_end"] <= label_coverage_end).astype("int8")
    timelines = {
        cik: group["filing_time"].sort_values().to_numpy(dtype="datetime64[ns]")
        for cik, group in new_notice.groupby("CIK")
    }
    def first_after_decision(row):
        values = timelines[row["CIK"]]
        position = np.searchsorted(values, np.datetime64(row["decision_time"]), side="right")
        return pd.NaT if position >= len(values) else pd.Timestamp(values[position])
    anchor["first_notice_after_decision"] = anchor.apply(first_after_decision, axis=1)
    anchor["subsequent_notice_18m"] = (
        anchor["first_notice_after_decision"].notna()
        & (anchor["first_notice_after_decision"] <= anchor["label_window_end"])
    ).astype("int8")
    anchor["pre_decision_followon"] = (
        anchor["next_notice_time"].notna()
        & (anchor["next_notice_time"] <= anchor["decision_time"])
    ).astype("int8")
    anchor["filing_lag_days"] = (anchor["filing_time"] - anchor["sale_date"]).dt.days
    selected = {
        "ACCESSIONNUMBER": "accession_number", "CIK": "cik", "ENTITYNAME": "entity_name",
        "filing_time": "filing_time", "sale_date": "sale_date", "decision_time": "decision_time",
        "label_window_end": "label_window_end", "observation_end": "observation_end",
        "label_coverage_end": "label_coverage_end", "label_window_complete": "label_window_complete",
        "first_notice_after_decision": "first_notice_after_decision",
        "INDUSTRYGROUPTYPE": "industry_group", "ENTITYTYPE": "entity_type", "STATEORCOUNTRY": "state",
        "JURISDICTIONOFINC": "jurisdiction", "YEAROFINC_TIMESPAN_CHOICE": "incorporation_age_band",
        "YEAROFINC_VALUE_ENTERED": "incorporation_year", "REVENUERANGE": "revenue_range",
        "FEDERALEXEMPTIONS_ITEMS_LIST": "federal_exemptions", "is_equity": "is_equity",
        "is_debt": "is_debt", "total_offering_amount": "total_offering_amount",
        "total_amount_sold": "total_amount_sold", "investor_count": "investor_count",
        "prior_notice_count": "prior_notice_count", "days_since_prior_notice": "days_since_prior_notice",
        "filing_lag_days": "filing_lag_days", "pre_decision_followon": "pre_decision_followon",
        "subsequent_notice_18m": "subsequent_notice_18m",
    }
    return anchor[list(selected)].rename(columns=selected)


def save_sqlite(filing: pd.DataFrame, cohort: pd.DataFrame, target: Path):
    safe_filing = filing[["ACCESSIONNUMBER", "CIK", "ENTITYNAME", "filing_time", "sale_date",
                          "SUBMISSIONTYPE", "INDUSTRYGROUPTYPE", "ENTITYTYPE", "STATEORCOUNTRY",
                          "is_amendment", "is_equity", "is_debt", "is_pooled_fund",
                          "total_offering_amount", "total_amount_sold", "investor_count"]].copy()
    with sqlite3.connect(target) as connection:
        safe_filing.to_sql("filings", connection, if_exists="replace", index=False)
        cohort.to_sql("p1_cohort", connection, if_exists="replace", index=False)
        connection.execute("CREATE INDEX IF NOT EXISTS idx_filings_cik_time ON filings(CIK, filing_time)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_cohort_cik ON p1_cohort(cik)")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-year", type=int, default=2008)
    parser.add_argument("--end-year", type=int, default=2023)
    parser.add_argument("--end-quarter", type=int, default=2)
    parser.add_argument("--anchor-start", type=int, default=2016)
    parser.add_argument("--anchor-end", type=int, default=2020)
    parser.add_argument("--raw-dir", type=Path, default=Path("datasets/raw/sec_form_d"))
    parser.add_argument("--processed-dir", type=Path, default=Path("datasets/processed/sec_form_d"))
    parser.add_argument(
        "--coverage-buffer-months", type=int, default=0,
        help="Subtract this many months from the latest filing when deciding label completeness.",
    )
    parser.add_argument(
        "--blind-summary", action="store_true",
        help="Suppress outcome counts/rates when preparing a future locked cohort.",
    )
    args = parser.parse_args()
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    args.processed_dir.mkdir(parents=True, exist_ok=True)
    submissions, issuers, offerings, loaded_archives, missing_archives = load_all(
        args.raw_dir, args.start_year, args.end_year, args.end_quarter)
    filing = build_filings(submissions, issuers, offerings)
    cohort = build_cohort(
        filing, args.anchor_start, args.anchor_end, args.coverage_buffer_months
    )
    cohort.to_csv(args.processed_dir / "p1_cohort.csv", index=False)
    save_sqlite(filing, cohort, args.processed_dir / "formd.sqlite")
    summary = {
        "source": "SEC Form D quarterly structured datasets",
        "source_url_patterns": [BASE_URL, LEGACY_URL],
        "archive_window": f"{args.start_year}Q1-{args.end_year}Q{args.end_quarter}",
        "loaded_archives": loaded_archives,
        "missing_archives": missing_archives,
        "anchor_window": f"{args.anchor_start}-{args.anchor_end}",
        "filings": int(len(filing)), "unique_issuers": int(filing["CIK"].nunique()),
        "cohort_rows": int(len(cohort)), "cohort_issuers": int(cohort["cik"].nunique()),
        "observation_end": filing["filing_time"].max().isoformat(),
        "label_coverage_end": cohort["label_coverage_end"].max().isoformat(),
        "coverage_buffer_months": args.coverage_buffer_months,
        "complete_label_windows": int(cohort["label_window_complete"].sum()),
        "censored_label_windows": int((cohort["label_window_complete"] == 0).sum()),
        "missing_sale_date_rate": float(cohort["sale_date"].isna().mean()) if len(cohort) else None,
        "privacy": "No related-person, signature, phone, street-address, or recipient tables retained.",
        "label": "A later non-amendment Form D notice between decision_time and +18 months; not a priced/institutional Series A label.",
        "outcome_metrics_blinded": bool(args.blind_summary),
    }
    if not args.blind_summary:
        summary["positive_labels"] = int(cohort["subsequent_notice_18m"].sum())
        summary["positive_rate"] = float(cohort["subsequent_notice_18m"].mean()) if len(cohort) else None
    (args.processed_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
