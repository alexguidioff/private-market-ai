"""Create a deterministic, blinded 200-issuer queue for open-source adjudication.

The queue is balanced on the existing SEC weak proxy only for audit/sampling. Reviewers must
create stronger labels from public evidence and may return ``unknown``. A sampled weak-proxy
negative is never treated as proof that no financing occurred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED = {
    "accession_number", "cik", "entity_name", "filing_time", "decision_time",
    "label_window_end", "industry_group", "total_amount_sold", "subsequent_notice_18m", "split",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def amount_bucket(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    observed = numeric.notna()
    result = pd.Series("unknown", index=values.index, dtype="object")
    if observed.any():
        ranked = numeric[observed].rank(method="first")
        bins = min(4, int(observed.sum()))
        labels = [f"q{i}" for i in range(1, bins + 1)]
        result.loc[observed] = pd.qcut(ranked, q=bins, labels=labels).astype(str)
    return result


def allocate(capacities: pd.Series, target: int) -> dict[str, int]:
    capacities = capacities[capacities > 0].sort_index().astype(int)
    if int(capacities.sum()) < target:
        raise ValueError(f"Only {int(capacities.sum())} eligible rows for target {target}")
    allocation = pd.Series(0, index=capacities.index, dtype=int)
    if len(capacities) <= target:
        allocation[:] = 1
    else:
        allocation.loc[capacities.sort_values(ascending=False).index[:target]] = 1
    while int(allocation.sum()) < target:
        remaining = capacities - allocation
        eligible = remaining[remaining > 0]
        weights = eligible / eligible.sum()
        desired = weights * (target - int(allocation.sum()))
        addition = np.floor(desired).astype(int).clip(upper=eligible)
        if int(addition.sum()) == 0:
            addition.loc[(desired - np.floor(desired)).sort_values(ascending=False).index[0]] = 1
        allocation.loc[addition.index] += addition
    return {str(key): int(value) for key, value in allocation.items() if value > 0}


def build_sample(data: pd.DataFrame, per_class: int, seed: int) -> tuple[pd.DataFrame, dict]:
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if data["cik"].astype(str).duplicated().any():
        raise ValueError("Input must contain one row per CIK")
    data = data.copy()
    data["cik"] = data["cik"].astype(str)
    data["anchor_year"] = pd.to_datetime(
        data["filing_time"], errors="raise", format="mixed"
    ).dt.year
    data["amount_bucket"] = amount_bucket(data["total_amount_sold"])
    data["sampling_stratum"] = (
        data["anchor_year"].astype(str) + "|" + data["industry_group"].fillna("unknown").astype(str)
        + "|" + data["amount_bucket"]
    )
    sampled = []
    allocations: dict[str, dict[str, int]] = {}
    for label in (0, 1):
        subset = data[data["subsequent_notice_18m"] == label]
        allocation = allocate(subset["sampling_stratum"].value_counts(), per_class)
        allocations[str(label)] = allocation
        for stratum, count in allocation.items():
            group = subset[subset["sampling_stratum"] == stratum]
            stratum_seed = int(hashlib.sha256(f"{seed}|{label}|{stratum}".encode()).hexdigest()[:8], 16)
            sampled.append(group.sample(n=count, random_state=stratum_seed, replace=False))
    result = pd.concat(sampled, ignore_index=True)
    result["gold_record_id"] = result["accession_number"].map(
        lambda value: "P1G-" + hashlib.sha256(str(value).encode()).hexdigest()[:12].upper()
    )
    result = result.sort_values("gold_record_id").reset_index(drop=True)
    counts = result.groupby("subsequent_notice_18m").size().to_dict()
    if counts != {0: per_class, 1: per_class}:
        raise AssertionError(f"Class balance failure: {counts}")
    if result["cik"].duplicated().any() or result["gold_record_id"].duplicated().any():
        raise AssertionError("Duplicate issuer or gold record")
    return result, allocations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path,
                        default=Path("datasets/processed/sec_form_d_v2/p1_first_anchor_model_ready.csv"))
    parser.add_argument("--output-dir", type=Path,
                        default=Path("datasets/processed/sec_form_d_v2/gold"))
    parser.add_argument("--per-class", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()
    if args.per_class < 1:
        raise ValueError("--per-class must be positive")
    data = pd.read_csv(args.input, dtype={"cik": str})
    sample, allocations = build_sample(data, args.per_class, args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    queue_columns = [
        "gold_record_id", "cik", "entity_name", "accession_number", "filing_time", "decision_time",
        "label_window_end", "industry_group", "state", "jurisdiction", "split", "anchor_year",
    ]
    queue = sample[queue_columns].rename(columns={"accession_number": "anchor_accession"})
    queue["canonical_company_id"] = ""
    queue["reviewer_1_status"] = "pending"
    queue["reviewer_2_status"] = "pending"
    queue.to_csv(args.output_dir / "annotation_queue.csv", index=False)

    audit_columns = queue_columns + [
        "sampling_stratum", "amount_bucket", "total_amount_sold", "subsequent_notice_18m"
    ]
    sample[audit_columns].to_csv(args.output_dir / "sampling_audit.csv", index=False)
    manifest = {
        "schema_version": "1.0.0",
        "purpose": "Balanced review sample; not a population prevalence estimate",
        "input": str(args.input),
        "input_sha256": sha256_file(args.input),
        "seed": args.seed,
        "per_weak_proxy_class": args.per_class,
        "rows": int(len(sample)),
        "unique_cik": int(sample["cik"].nunique()),
        "weak_proxy_counts": {str(k): int(v) for k, v in sample["subsequent_notice_18m"].value_counts().sort_index().items()},
        "split_counts": {str(k): int(v) for k, v in sample["split"].value_counts().sort_index().items()},
        "anchor_year_counts": {str(k): int(v) for k, v in sample["anchor_year"].value_counts().sort_index().items()},
        "industry_counts": {str(k): int(v) for k, v in sample["industry_group"].value_counts().sort_index().items()},
        "allocation_by_weak_class_and_stratum": allocations,
        "reviewer_blinded_fields": ["subsequent_notice_18m", "sampling_stratum", "amount_bucket", "total_amount_sold"],
        "negative_semantics": "weak-proxy negative; not evidence that no financing occurred",
    }
    (args.output_dir / "sampling_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps({key: manifest[key] for key in (
        "rows", "unique_cik", "weak_proxy_counts", "split_counts", "anchor_year_counts", "industry_counts"
    )}, indent=2))


if __name__ == "__main__":
    main()
