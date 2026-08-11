"""Audit SBIR/STTR as a candidate P1 acquisition block without using the 2020 test."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

SOURCE_URL = (
    "https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/"
    "award_data_no_abstract.csv"
)
USECOLS = ["Company", "State", "Proposal Award Date", "Date of Notification", "Award Year", "UEI", "Duns"]
LEGAL_SUFFIX = re.compile(
    r"\b(INCORPORATED|INC|CORPORATION|CORP|COMPANY|CO|LIMITED|LTD|LLC|L L C|LP|L P|PLC)\b"
)
STATE_CODES = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR",
    "CALIFORNIA": "CA", "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE",
    "FLORIDA": "FL", "GEORGIA": "GA", "HAWAII": "HI", "IDAHO": "ID",
    "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA", "KANSAS": "KS",
    "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS",
    "MISSOURI": "MO", "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ", "NEW MEXICO": "NM", "NEW YORK": "NY",
    "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND", "OHIO": "OH", "OKLAHOMA": "OK",
    "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT",
    "VERMONT": "VT", "VIRGINIA": "VA", "WASHINGTON": "WA", "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI", "WYOMING": "WY", "DISTRICT OF COLUMBIA": "DC",
}


def normalize_name(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    text = text.upper().replace("&", " AND ")
    text = LEGAL_SUFFIX.sub(" ", text)
    return re.sub(r"[^A-Z0-9]+", " ", text).strip()


def clean_state(value: object) -> str:
    text = str(value or "").strip().upper()
    if re.fullmatch(r"[A-Z]{2}", text):
        return text
    return STATE_CODES.get(text, "")


def firm_id(frame: pd.DataFrame) -> pd.Series:
    uei = frame["UEI"].fillna("").astype(str).str.strip()
    duns = frame["Duns"].fillna("").astype(str).str.strip()
    return uei.where(uei.ne(""), duns.where(duns.ne(""), frame["match_key"]))


def load_sbir(source: str) -> pd.DataFrame:
    chunks = []
    for chunk in pd.read_csv(source, usecols=USECOLS, dtype=str, chunksize=200_000, low_memory=False):
        chunk["name_norm"] = chunk["Company"].map(normalize_name)
        chunk["state_norm"] = chunk["State"].map(clean_state)
        chunk = chunk[chunk["name_norm"].ne("") & chunk["state_norm"].ne("")].copy()
        chunk["match_key"] = chunk["name_norm"] + "|" + chunk["state_norm"]
        chunk["firm_id"] = firm_id(chunk)
        chunk["award_date"] = pd.to_datetime(chunk["Proposal Award Date"], format="mixed", errors="coerce")
        chunk["notification_date"] = pd.to_datetime(chunk["Date of Notification"], format="mixed", errors="coerce")
        chunks.append(chunk[["match_key", "firm_id", "award_date", "notification_date"]])
    return pd.concat(chunks, ignore_index=True)

def run(cohort_path: Path, source: str, output_dir: Path) -> dict:
    cohort = pd.read_csv(cohort_path, dtype={"cik": str})
    cohort["filing_time"] = pd.to_datetime(cohort["filing_time"], format="mixed", errors="coerce")
    cohort["decision_time"] = pd.to_datetime(cohort["decision_time"], format="mixed", errors="coerce")
    cohort = cohort[
        cohort["is_first_eligible_anchor"].eq(1)
        & cohort["filing_time"].dt.year.between(2016, 2019)
    ].copy()
    cohort["name_norm"] = cohort["entity_name"].map(normalize_name)
    cohort["state_norm"] = cohort["state"].map(clean_state)
    cohort["match_key"] = cohort["name_norm"] + "|" + cohort["state_norm"]

    sbir = load_sbir(source)
    key_stats = sbir.groupby("match_key").agg(
        distinct_firms=("firm_id", "nunique"),
        award_rows=("firm_id", "size"),
        first_award_date=("award_date", "min"),
        first_notification_date=("notification_date", "min"),
    ).reset_index()
    joined = cohort.merge(key_stats, on="match_key", how="left", validate="many_to_one")
    joined["candidate_match"] = joined["award_rows"].notna()
    joined["unambiguous_source_key"] = joined["distinct_firms"].eq(1)
    joined["award_known_by_decision_upper_bound"] = (
        joined["unambiguous_source_key"]
        & joined["first_award_date"].notna()
        & (joined["first_award_date"] <= pd.to_datetime(joined["decision_time"]))
    )

    candidate = joined[joined["candidate_match"]].copy()
    report = {
        "scope": "development and validation anchors only; 2020 excluded",
        "source": source,
        "matching_rule": "exact normalized company name plus two-letter state",
        "point_in_time_warning": (
            "Proposal Award Date is an event-time upper bound, not proof of SBIR.gov public availability."
        ),
        "cohort_rows": int(len(joined)),
        "candidate_matches": int(joined["candidate_match"].sum()),
        "candidate_coverage": float(joined["candidate_match"].mean()),
        "unambiguous_source_keys": int(joined["unambiguous_source_key"].sum()),
        "ambiguous_source_keys": int((joined["candidate_match"] & ~joined["unambiguous_source_key"]).sum()),
        "award_by_decision_upper_bound": int(joined["award_known_by_decision_upper_bound"].sum()),
        "missing_notification_date_rate_among_candidates": (
            None if candidate.empty else float(candidate["first_notification_date"].isna().mean())
        ),
        "manual_review_required": True,
        "data_gate_pass": False,
        "block_decision": "conditional candidate; not approved for a VoI experiment",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_columns = [
        "cik", "entity_name", "state", "filing_time", "decision_time", "match_key",
        "candidate_match", "distinct_firms", "award_rows", "first_award_date",
        "first_notification_date", "award_known_by_decision_upper_bound",
    ]
    joined[audit_columns].to_csv(output_dir / "sbir_match_audit.csv", index=False)
    (output_dir / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["summary_sha256"] = hashlib.sha256(
        (output_dir / "summary.json").read_bytes()
    ).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cohort",
        type=Path,
        default=Path("datasets/processed/sec_form_d_v2/p1_cohort_enriched.csv"),
    )
    parser.add_argument("--source", default=SOURCE_URL)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("datasets/processed/sec_form_d_v2/sbir_audit"),
    )
    args = parser.parse_args()
    print(json.dumps(run(args.cohort, args.source, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
