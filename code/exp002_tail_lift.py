"""EXP-002: tail lift of point-in-time SEC information.

Question
--------
EXP-001D established that issuer filing history transports as baseline
information for the weak SEC outcome, raising ROC-AUC from 0.5930 to 0.6551. An
AUC of 0.65 is modest. It is also the wrong summary if the decision only
concerns the extreme: an analyst screens the top slice of a pipeline, not the
median company.

This experiment asks whether the same information is sharply informative in the
tail, and whether that sharpness transports to a company-disjoint later cohort.

Design
------
* Development cohort: issuers whose anchor filing is in 2021.
* Validation cohort: issuers whose anchor filing is in 2022, zero CIK overlap.
* Outcome: the same weak proxy as EXP-001B/C/D, a subsequent non-amendment
  Form D notice within 18 months of the decision time.
* Statistic: lift(q) = P(outcome | feature in top q) / P(outcome), for
  q in {0.30, 0.20, 0.10, 0.05}.
* Uncertainty: bootstrap interval on the lift plus a permutation p-value.
* Multiplicity: Benjamini-Hochberg across the entire feature-by-threshold scan.
* Reporting: ROC-AUC alongside every lift, so the gap between average and tail
  behaviour is visible rather than asserted.

The 2023 locked test cohort is not touched.

    python code/exp002_tail_lift.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tail_lift import screen, transport_check  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COHORT = ROOT / "datasets" / "processed" / "sec_form_d_future_2021_2023" / "p1_cohort_enriched.csv"
OUT_DIR = ROOT / "experiments" / "EXP-002"

# Declared before running: point-in-time fields available at the decision time.
# Grouped so the report can separate issuer history from single-filing terms.
HISTORY_FEATURES = [
    "known_filing_count",
    "known_new_notice_count",
    "prior_notice_count",
    "known_amendment_count",
    "known_equity_filing_count",
    "issuer_observed_age_days",
    "days_since_latest_known_filing",
]

FILING_FEATURES = [
    "total_offering_amount",
    "total_amount_sold",
    "investor_count",
    "filing_lag_days",
    "known_cumulative_amount_sold",
    "known_max_amount_sold",
    "latest_known_investor_count",
    "latest_known_amount_sold",
]

FEATURES = HISTORY_FEATURES + FILING_FEATURES

QUANTILES = (0.30, 0.20, 0.10, 0.05)
BOOTSTRAP = 500
SEED = 20260728
FDR_ALPHA = 0.05


def load_rows() -> list[dict]:
    """Load the cohort, keeping only rows with a complete label window."""
    with COHORT.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return [
        r
        for r in rows
        if r.get("label_window_complete") == "1"
        and r.get("subsequent_notice_18m") in ("0.0", "1.0")
    ]


def numeric(row: dict, key: str) -> float:
    raw = row.get(key, "")
    if raw in ("", None):
        return 0.0
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0


def labels(rows: list[dict]) -> list[int]:
    return [1 if r["subsequent_notice_18m"] == "1.0" else 0 for r in rows]


def split_by_anchor_year(rows: list[dict]) -> tuple[list[dict], list[dict], dict]:
    """Development on 2021 anchors, validation on 2022 anchors, CIK-disjoint.

    An issuer can file in both years, so a naive year split shares issuers: the
    first run of this experiment found 846 CIKs on both sides. Leaving them in
    would let the same company's history appear in development and validation,
    inflating any transport claim.

    Issuers present in both years are removed from validation, keeping their
    earlier observation in development. Dropping them from development instead
    would discard the richer-history cases that carry the signal, biasing the
    scan; dropping from validation costs sample but keeps the test honest.
    """
    dev = [r for r in rows if r["filing_time"][:4] == "2021"]
    raw_test = [r for r in rows if r["filing_time"][:4] == "2022"]

    dev_ciks = {r["cik"] for r in dev}
    test = [r for r in raw_test if r["cik"] not in dev_ciks]

    # One row per issuer, keeping the earliest anchor, so no issuer is counted
    # twice inside a cohort either.
    def first_per_issuer(rs: list[dict]) -> list[dict]:
        seen: dict[str, dict] = {}
        for r in sorted(rs, key=lambda x: x["filing_time"]):
            seen.setdefault(r["cik"], r)
        return list(seen.values())

    dev = first_per_issuer(dev)
    test = first_per_issuer(test)

    audit = {
        "raw_dev_rows": len([r for r in rows if r["filing_time"][:4] == "2021"]),
        "raw_test_rows": len(raw_test),
        "removed_from_test_cross_year": len(raw_test) - len([
            r for r in raw_test if r["cik"] not in dev_ciks
        ]),
        "dev_rows_after_dedup": len(dev),
        "test_rows_after_dedup": len(test),
    }
    return dev, test, audit


def verify_disjoint(dev: list[dict], test: list[dict]) -> dict:
    """Confirm no issuer appears in both cohorts."""
    dev_ciks = {r["cik"] for r in dev}
    test_ciks = {r["cik"] for r in test}
    overlap = dev_ciks & test_ciks
    return {
        "dev_issuers": len(dev_ciks),
        "test_issuers": len(test_ciks),
        "cik_overlap": len(overlap),
        "disjoint": not overlap,
    }


def main() -> int:
    if not COHORT.exists():
        print(f"error: cohort not found at {COHORT}", file=sys.stderr)
        print("Run code/enrich_formd_cohort.py first.", file=sys.stderr)
        return 2

    rows = load_rows()
    dev, test, split_audit = split_by_anchor_year(rows)
    disjoint = verify_disjoint(dev, test)

    print("EXP-002 — tail lift of point-in-time SEC information")
    print()
    print(f"  usable rows          {len(rows)}")
    print(f"  development (2021)   {len(dev)}  base rate {sum(labels(dev)) / len(dev):.1%}")
    print(f"  validation  (2022)   {len(test)}  base rate {sum(labels(test)) / len(test):.1%}")
    print(f"  removed from test    {split_audit['removed_from_test_cross_year']} "
          f"(issuers also present in 2021)")
    print(f"  CIK overlap          {disjoint['cik_overlap']} "
          f"({'disjoint' if disjoint['disjoint'] else 'NOT DISJOINT'})")
    print()

    if not disjoint["disjoint"]:
        print("  ABORT: cohorts share issuers; the transport check would be invalid.",
              file=sys.stderr)
        return 2

    y_dev = labels(dev)
    y_test = labels(test)

    # --- development scan ----------------------------------------------------
    dev_features = {k: [numeric(r, k) for r in dev] for k in FEATURES}
    profiles, summary = screen(
        dev_features, y_dev, QUANTILES, n_boot=BOOTSTRAP, alpha=FDR_ALPHA, seed=SEED
    )

    print("  --- development scan (2021) ---")
    print()
    for prof in sorted(profiles, key=lambda p: -(p.best.lift if p.best and p.best.lift else 0)):
        print(prof.report())
        print()

    print(f"  surviving FDR ({summary['n_tests']} tests): "
          f"{', '.join(summary['survivors_fdr']) or 'none'}")
    print(f"  monotone lift:      {', '.join(summary['monotone']) or 'none'}")
    print(f"  tail-only signals:  {', '.join(summary['tail_only']) or 'none'}")
    print()

    # --- transport check -----------------------------------------------------
    paired = {
        k: ([numeric(r, k) for r in dev], [numeric(r, k) for r in test])
        for k in FEATURES
    }
    transport = transport_check(paired, y_dev, y_test, q=0.05, n_boot=BOOTSTRAP, seed=SEED)

    print("  --- transport to company-disjoint 2022 cohort (q = 0.05) ---")
    print()
    print(f"  {'feature':<32}{'dev':>8}{'test':>8}  {'test 95% CI':<18}{'transports':>10}")
    for row in transport:
        dev_lift = f"{row['dev_lift']:.2f}x" if row["dev_lift"] else "n/a"
        test_lift = f"{row['test_lift']:.2f}x" if row["test_lift"] else "n/a"
        ci = f"[{row['test_ci'][0]:.2f}, {row['test_ci'][1]:.2f}]" if row["test_ci"] else "-"
        mark = "yes" if row["transports"] else ""
        print(f"  {row['feature']:<32}{dev_lift:>8}{test_lift:>8}  {ci:<18}{mark:>10}")

    transported = [r["feature"] for r in transport if r["transports"]]
    print()
    print(f"  transports: {', '.join(transported) or 'none'}")

    # --- artefacts -----------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        "experiment": "EXP-002",
        "question": "Is point-in-time SEC information sharply informative in the tail, "
                    "and does that transport to a company-disjoint cohort?",
        "cohort_file": str(COHORT.relative_to(ROOT)),
        "development_anchor_year": 2021,
        "validation_anchor_year": 2022,
        "outcome": "subsequent non-amendment Form D notice within 18 months "
                   "(weak regulatory proxy)",
        "features_history": HISTORY_FEATURES,
        "features_filing": FILING_FEATURES,
        "quantiles": list(QUANTILES),
        "bootstrap": BOOTSTRAP,
        "seed": SEED,
        "fdr_alpha": FDR_ALPHA,
        "locked_2023_test_used": False,
    }
    (OUT_DIR / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    results = {
        "cohorts": {
            "development": {"n": len(dev), "base_rate": round(sum(y_dev) / len(dev), 4)},
            "validation": {"n": len(test), "base_rate": round(sum(y_test) / len(test), 4)},
            "disjointness": disjoint,
            "split_audit": split_audit,
        },
        "development_scan": {
            "summary": summary,
            "profiles": [p.as_dict() for p in profiles],
        },
        "transport_q05": transport,
    }
    (OUT_DIR / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    print()
    print(f"  wrote {OUT_DIR / 'config.json'}")
    print(f"  wrote {OUT_DIR / 'results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
