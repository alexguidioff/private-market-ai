"""Select a deterministic blinded 20-issuer pilot from the P1 gold review sample."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def stable_score(seed: int, record_id: str) -> str:
    return hashlib.sha256(f"{seed}|{record_id}".encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("datasets/processed/sec_form_d_v2/gold/sampling_audit.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("datasets/processed/sec_form_d_v2/gold/pilot20"),
    )
    parser.add_argument("--per-year-class", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()

    data = pd.read_csv(args.input, dtype={"cik": str})
    required = {
        "gold_record_id", "cik", "entity_name", "accession_number", "filing_time",
        "decision_time", "label_window_end", "industry_group", "state", "jurisdiction",
        "split", "anchor_year", "subsequent_notice_18m",
    }
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    data["selection_score"] = data["gold_record_id"].map(
        lambda value: stable_score(args.seed, str(value))
    )
    pilot = (
        data.sort_values("selection_score")
        .groupby(["anchor_year", "subsequent_notice_18m"], group_keys=False)
        .head(args.per_year_class)
        .sort_values("gold_record_id")
        .reset_index(drop=True)
    )
    expected = data["anchor_year"].nunique() * 2 * args.per_year_class
    if len(pilot) != expected or pilot["cik"].nunique() != expected:
        raise AssertionError("Pilot size or issuer uniqueness check failed")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    queue_columns = [
        "gold_record_id", "cik", "entity_name", "accession_number", "filing_time",
        "decision_time", "label_window_end", "industry_group", "state", "jurisdiction", "split",
        "anchor_year",
    ]
    queue = pilot[queue_columns].rename(columns={"accession_number": "anchor_accession"})
    queue["canonical_company_id"] = ""
    queue["review_status"] = "pending"
    queue.to_csv(args.output_dir / "pilot_annotation_queue.csv", index=False)

    audit_columns = queue_columns + ["subsequent_notice_18m", "selection_score"]
    pilot[audit_columns].to_csv(args.output_dir / "pilot_sampling_audit.csv", index=False)
    manifest = {
        "schema_version": "1.0.0",
        "seed": args.seed,
        "rows": int(len(pilot)),
        "unique_cik": int(pilot["cik"].nunique()),
        "selection": "lowest stable SHA-256 score per anchor_year and hidden SEC weak-proxy class",
        "per_year_per_hidden_class": args.per_year_class,
        "weak_proxy_counts": {
            str(key): int(value)
            for key, value in pilot["subsequent_notice_18m"].value_counts().sort_index().items()
        },
        "year_counts": {
            str(key): int(value)
            for key, value in pilot["anchor_year"].value_counts().sort_index().items()
        },
        "blinding": "Weak proxy and selection score are absent from pilot_annotation_queue.csv",
    }
    (args.output_dir / "pilot_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
