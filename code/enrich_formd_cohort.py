"""Add point-in-time issuer-history features to the SEC Form D P1 cohort."""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


def prepare_history(database: Path) -> pd.DataFrame:
    columns = [
        "CIK", "filing_time", "is_amendment", "is_equity", "is_debt",
        "total_offering_amount", "total_amount_sold", "investor_count",
    ]
    with sqlite3.connect(database) as connection:
        history = pd.read_sql_query(f"SELECT {','.join(columns)} FROM filings", connection)
    history["filing_time"] = pd.to_datetime(history["filing_time"], format="mixed", errors="coerce")
    history = history.dropna(subset=["CIK", "filing_time"]).sort_values(["filing_time", "CIK"])
    history["is_new_notice"] = (history["is_amendment"] == 0).astype("int8")
    history["new_amount_sold"] = history["total_amount_sold"].where(history["is_new_notice"] == 1, 0).fillna(0)
    history["new_offering_amount"] = history["total_offering_amount"].where(history["is_new_notice"] == 1, 0).fillna(0)
    grouped = history.groupby("CIK", sort=False)
    history["known_filing_count"] = grouped.cumcount() + 1
    history["known_new_notice_count"] = grouped["is_new_notice"].cumsum()
    history["known_amendment_count"] = grouped["is_amendment"].cumsum()
    history["known_equity_filing_count"] = grouped["is_equity"].cumsum()
    history["known_debt_filing_count"] = grouped["is_debt"].cumsum()
    history["known_cumulative_amount_sold"] = grouped["new_amount_sold"].cumsum()
    history["known_cumulative_offering_amount"] = grouped["new_offering_amount"].cumsum()
    history["known_max_amount_sold"] = grouped["new_amount_sold"].cummax()
    history["issuer_first_seen_time"] = grouped["filing_time"].transform("min")
    return history
def enrich(cohort_path: Path, database: Path) -> pd.DataFrame:
    cohort = pd.read_csv(cohort_path, dtype={"cik": str})
    cohort["decision_time"] = pd.to_datetime(cohort["decision_time"], format="mixed", errors="coerce")
    cohort["filing_time"] = pd.to_datetime(cohort["filing_time"], format="mixed", errors="coerce")
    history = prepare_history(database)
    left = cohort.sort_values(["decision_time", "cik"]).copy()
    right = history.sort_values(["filing_time", "CIK"]).copy()
    enriched = pd.merge_asof(
        left, right, left_on="decision_time", right_on="filing_time",
        left_by="cik", right_by="CIK", direction="backward", allow_exact_matches=True,
        suffixes=("", "_latest_known"),
    )
    enriched["days_since_latest_known_filing"] = (
        enriched["decision_time"] - enriched["filing_time_latest_known"]
    ).dt.days
    enriched["issuer_observed_age_days"] = (
        enriched["decision_time"] - enriched["issuer_first_seen_time"]
    ).dt.days
    enriched["latest_known_amount_sold"] = enriched["total_amount_sold_latest_known"]
    enriched["latest_known_investor_count"] = enriched["investor_count_latest_known"]
    enriched = enriched.sort_values(["cik", "filing_time", "accession_number"])
    enriched["eligible_anchor_sequence"] = enriched.groupby("cik").cumcount() + 1
    enriched["is_first_eligible_anchor"] = (enriched["eligible_anchor_sequence"] == 1).astype("int8")
    drop = ["CIK", "is_amendment", "is_equity_latest_known", "is_debt_latest_known",
            "total_offering_amount_latest_known", "total_amount_sold_latest_known",
            "investor_count_latest_known", "is_new_notice", "new_amount_sold", "new_offering_amount"]
    enriched = enriched.drop(columns=[column for column in drop if column in enriched], errors="ignore")
    return enriched.sort_values(["filing_time", "accession_number"])


def audit(data: pd.DataFrame) -> dict:
    complete = data.get("label_window_complete", pd.Series(1, index=data.index)).eq(1)
    positives = data["subsequent_notice_18m"].eq(1) & complete
    future = pd.to_datetime(data["first_notice_after_decision"], errors="coerce")
    decision = pd.to_datetime(data["decision_time"], errors="coerce")
    window_end = pd.to_datetime(data["label_window_end"], errors="coerce")
    by_year = data.groupby(pd.to_datetime(data["filing_time"]).dt.year)["subsequent_notice_18m"].agg(["size", "sum", "mean"])
    return {
        "rows": int(len(data)), "columns": int(len(data.columns)),
        "unique_accessions": int(data["accession_number"].nunique()),
        "unique_issuers": int(data["cik"].nunique()),
        "complete_label_windows": int(complete.sum()),
        "censored_label_windows": int((~complete).sum()),
        "positive_labels": int(positives.sum()),
        "positive_rate": float(data.loc[complete, "subsequent_notice_18m"].mean()),
        "duplicate_accessions": int(data["accession_number"].duplicated().sum()),
        "positive_before_or_at_decision": int((positives & (future <= decision)).sum()),
        "positive_after_window": int((positives & (future > window_end)).sum()),
        "negative_with_in_window_notice": int((complete & data["subsequent_notice_18m"].eq(0) & future.notna() & (future <= window_end)).sum()),
        "negative_history_counts": int((data["known_filing_count"] < 1).sum()),
        "by_anchor_year": {str(year): {"rows": int(row["size"]), "positive": int(row["sum"]), "rate": float(row["mean"])} for year, row in by_year.iterrows()},
        "feature_missing_rates": {column: float(data[column].isna().mean()) for column in ["known_filing_count", "known_cumulative_amount_sold", "latest_known_amount_sold", "latest_known_investor_count", "days_since_latest_known_filing"]},
    }
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("datasets/processed/sec_form_d_v2"))
    parser.add_argument("--output", type=Path, default=Path("datasets/processed/sec_form_d_v2/p1_cohort_enriched.csv"))
    parser.add_argument("--split-scheme", choices=["legacy", "future"], default="legacy")
    parser.add_argument(
        "--exclude-ciks-from", type=Path,
        help="CSV whose CIKs must be excluded from a future independent cohort.",
    )
    parser.add_argument(
        "--blind-report", action="store_true",
        help="Suppress outcome counts/rates when preparing a future locked cohort.",
    )
    args = parser.parse_args()
    if args.split_scheme == "future" and not args.blind_report:
        raise ValueError("--blind-report is required for the future split scheme")
    data = enrich(args.input_dir / "p1_cohort.csv", args.input_dir / "formd.sqlite")
    report = audit(data)
    if any(report[key] for key in ["duplicate_accessions", "positive_before_or_at_decision", "positive_after_window", "negative_with_in_window_notice", "negative_history_counts"]):
        raise AssertionError(report)
    first_anchor = data[data["is_first_eligible_anchor"] == 1].copy()
    excluded_prior_ciks = 0
    if args.split_scheme == "future":
        first_anchor = first_anchor[first_anchor["label_window_complete"].eq(1)].copy()
        if not args.exclude_ciks_from:
            raise ValueError("--exclude-ciks-from is required for the future split scheme")
        prior_ciks = set(pd.read_csv(args.exclude_ciks_from, usecols=["cik"], dtype={"cik": str})["cik"])
        prior_mask = first_anchor["cik"].astype(str).isin(prior_ciks)
        excluded_prior_ciks = int(prior_mask.sum())
        first_anchor = first_anchor[~prior_mask].copy()
    anchor_year = first_anchor["filing_time"].dt.year
    if args.split_scheme == "legacy":
        first_anchor["split"] = np.select(
            [anchor_year <= 2018, anchor_year == 2019, anchor_year == 2020],
            ["train", "validation", "test"], default="excluded")
    else:
        first_anchor["split"] = np.select(
            [anchor_year == 2021, anchor_year == 2022, anchor_year == 2023],
            ["future_train", "future_validation", "locked_test"], default="excluded")
    if first_anchor["cik"].duplicated().any():
        raise AssertionError("CIK leakage in model-ready cohort")
    model_ready = first_anchor.copy()
    if args.split_scheme == "future":
        locked = first_anchor[first_anchor["split"].eq("locked_test")].copy()
        labels = locked[["accession_number", "cik", "subsequent_notice_18m"]].copy()
        features = locked.drop(columns=["subsequent_notice_18m", "first_notice_after_decision"], errors="ignore")
        labels_path = args.output.parent / "p1_locked_test_labels.csv"
        features_path = args.output.parent / "p1_locked_test_features.csv"
        locked_keys = set(zip(locked["accession_number"].astype(str), locked["cik"].astype(str)))
        if labels_path.exists():
            existing_keys_frame = pd.read_csv(
                labels_path, usecols=["accession_number", "cik"], dtype=str
            )
            existing_keys = set(zip(
                existing_keys_frame["accession_number"], existing_keys_frame["cik"]
            ))
            if existing_keys != locked_keys:
                raise AssertionError("Existing locked-label vault keys differ from locked test")
        else:
            if labels["subsequent_notice_18m"].isna().any():
                raise AssertionError("Cannot create locked-label vault from masked outcomes")
            labels.to_csv(labels_path, index=False)
        features.to_csv(features_path, index=False)
        locked_ciks = set(locked["cik"].astype(str))
        locked_data_mask = data["cik"].astype(str).isin(locked_ciks)
        data.loc[locked_data_mask, "subsequent_notice_18m"] = np.nan
        data.loc[locked_data_mask, "first_notice_after_decision"] = pd.NaT
        source_cohort_path = args.input_dir / "p1_cohort.csv"
        source_cohort = pd.read_csv(source_cohort_path, dtype={"cik": str})
        source_locked_mask = source_cohort["cik"].isin(locked_ciks)
        source_cohort.loc[source_locked_mask, "subsequent_notice_18m"] = np.nan
        source_cohort.loc[source_locked_mask, "first_notice_after_decision"] = pd.NA
        source_cohort.to_csv(source_cohort_path, index=False)
        with sqlite3.connect(args.input_dir / "formd.sqlite") as connection:
            connection.execute("DROP TABLE IF EXISTS locked_ciks")
            connection.execute("CREATE TEMP TABLE locked_ciks (cik TEXT PRIMARY KEY)")
            connection.executemany(
                "INSERT INTO locked_ciks(cik) VALUES (?)", ((cik,) for cik in locked_ciks)
            )
            connection.execute(
                "UPDATE p1_cohort SET subsequent_notice_18m = NULL, "
                "first_notice_after_decision = NULL WHERE CAST(cik AS TEXT) IN "
                "(SELECT cik FROM locked_ciks)"
            )
        locked_mask = model_ready["split"].eq("locked_test")
        model_ready.loc[locked_mask, "subsequent_notice_18m"] = np.nan
        model_ready.loc[locked_mask, "first_notice_after_decision"] = pd.NaT
        report["locked_test_label_sha256"] = hashlib.sha256(labels_path.read_bytes()).hexdigest()
        report["locked_test_feature_sha256"] = hashlib.sha256(features_path.read_bytes()).hexdigest()
        report["masked_panel_rows"] = int(locked_data_mask.sum())
        report["masked_source_rows"] = int(source_locked_mask.sum())
    data.to_csv(args.output, index=False)
    model_ready.to_csv(args.output.parent / "p1_first_anchor_model_ready.csv", index=False)
    report["model_ready_rows"] = int(len(first_anchor))
    report["model_ready_unique_issuers"] = int(first_anchor["cik"].nunique())
    report["excluded_prior_cohort_ciks"] = excluded_prior_ciks
    report["model_ready_splits"] = {key: int(value) for key, value in first_anchor["split"].value_counts().to_dict().items()}
    report["split_scheme"] = args.split_scheme
    report["outcome_metrics_blinded"] = bool(args.blind_report)
    if args.blind_report:
        for key in ["positive_labels", "positive_rate", "by_anchor_year", "model_ready_positive_rate"]:
            report.pop(key, None)
        report["locked_test_labels_separated"] = True
        report["locked_test_labels_file"] = "p1_locked_test_labels.csv"
        report["locked_test_features_file"] = "p1_locked_test_features.csv"
    else:
        report["model_ready_positive_rate"] = float(first_anchor["subsequent_notice_18m"].mean())
    (args.output.parent / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
