"""EXP-003 — What share of quantitative claims is deterministically checkable?

Design
------
Claims are generated *from* real filing data, with a known ground truth, then
verified as if their provenance were unknown. Generating them removes the need to
hand-label a corpus, and — more importantly — lets the error be injected on
purpose, so sensitivity and specificity are both measurable. A verifier that
accepts everything scores perfectly on correct claims; only injected errors
expose it.

Claim styles mirror how the numbers actually get written in memos: exact figures,
scaled figures, rounded figures, hedged figures, and figures whose stated unit
differs from the source's unit.

Errors injected, each a real failure mode:

* **wrong field** — the number belongs to a different line item. This is
  attribution hallucination in its purest form and the one a plain link cannot
  catch, because the cited document genuinely contains the number.
* **transposed digits** — 5,234,000 written as 5,324,000.
* **scale error** — thousands read as millions.
* **stale value** — a figure from an earlier filing by the same issuer.

The last is the one this project is unusually equipped to test, because the
point-in-time pipeline knows which value was current at which date.

Reported
--------
Coverage (share checkable at all), sensitivity to each injected error class, false
alarm rate on correct claims, and the same for the naive string-equality
baseline. The declared kill conditions are in `docs/Idea_Falsification_Log.md`.
"""

from __future__ import annotations

import json
import random
import sqlite3
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from claim_verify import (  # noqa: E402
    CONTRADICTED,
    NOT_CHECKABLE,
    SOURCE_MISSING,
    VERIFIED,
    NumericClaim,
    is_hedged,
    naive_verify,
    verify_claim,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-003"
SEED = 20260728

# Fields a memo would quote, with the phrasing a human would use.
QUOTABLE_FIELDS = {
    "total_offering_amount": "the total offering amount",
    "total_amount_sold": "the amount sold",
    "investor_count": "the number of investors",
}


def find_dataset() -> Path | None:
    """Locate the built Form D dataset, whatever form it took."""
    for pattern in ("**/*.sqlite", "**/*.db", "**/formd*.parquet", "**/formd*.csv"):
        for candidate in sorted(ROOT.glob(pattern)):
            if candidate.stat().st_size > 10_000:
                return candidate
    return None


def load_rows(limit: int = 4000) -> list[dict]:
    """Load issuer-offering rows with the numeric fields needed."""
    path = find_dataset()
    if path is None:
        return []

    print(f"  source dataset: {path.relative_to(ROOT)}")

    if path.suffix in (".sqlite", ".db"):
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        tables = [
            r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        ]
        print(f"  tables: {tables}")

        for table in tables:
            cols = {
                r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()
            }
            if {"total_offering_amount", "total_amount_sold"} & cols:
                wanted = [c for c in (
                    "cik", "accession_number", "filing_date",
                    "total_offering_amount", "total_amount_sold", "investor_count",
                ) if c in cols]
                query = (
                    f"SELECT {', '.join(wanted)} FROM {table} "
                    f"WHERE total_amount_sold IS NOT NULL LIMIT {limit}"
                )
                rows = [dict(r) for r in conn.execute(query).fetchall()]
                conn.close()
                print(f"  loaded {len(rows)} rows from {table}")
                return rows
        conn.close()
        return []

    if path.suffix == ".csv":
        import csv

        with path.open(encoding="utf-8", errors="replace") as handle:
            return [row for _, row in zip(range(limit), csv.DictReader(handle))]

    try:
        import pandas as pd

        frame = pd.read_parquet(path).head(limit)
        return frame.to_dict("records")
    except Exception:  # noqa: BLE001
        return []


# --------------------------------------------------------------------------
# claim generation
# --------------------------------------------------------------------------

def render(value: Decimal, style: str, rng: random.Random) -> str:
    """Write a number the way a person would, in the requested style."""
    if style == "exact":
        return f"${value:,.0f}"
    if style == "scaled":
        if value >= 1_000_000_000:
            return f"${value / Decimal(1_000_000_000):.2f} billion"
        if value >= 1_000_000:
            return f"${value / Decimal(1_000_000):.2f} million"
        if value >= 1_000:
            return f"${value / Decimal(1_000):.0f}K"
        return f"${value:,.0f}"
    if style == "rounded":
        if value >= 1_000_000:
            return f"${value / Decimal(1_000_000):.1f} million"
        if value >= 1_000:
            return f"${value / Decimal(1_000):.0f}K"
        return f"${value:,.0f}"
    if style == "hedged":
        word = rng.choice(["approximately", "about", "roughly"])
        if value >= 1_000_000:
            return f"{word} ${value / Decimal(1_000_000):.0f} million"
        return f"{word} ${value:,.0f}"
    if style == "plain":
        return f"{value:,.0f}"
    return f"${value:,.0f}"


@dataclass
class Generated:
    claim: NumericClaim
    source_row: dict
    truth: str          # "correct" or the injected error class
    style: str


def build_claims(rows: list[dict], per_row: int = 1) -> list[Generated]:
    """Generate claims with known truth, half correct and half corrupted."""
    rng = random.Random(SEED)
    out: list[Generated] = []

    styles = ("exact", "scaled", "rounded", "hedged")
    errors = ("wrong_field", "transposed", "scale_error", "stale")

    # Index by issuer so a stale value can be drawn from the same issuer's other
    # filing, which is what actually happens in a memo.
    by_cik: dict[str, list[dict]] = {}
    for row in rows:
        by_cik.setdefault(str(row.get("cik", "")), []).append(row)

    for row in rows:
        candidates = [
            f for f in QUOTABLE_FIELDS
            if row.get(f) not in (None, "", "Indefinite")
        ]
        if not candidates:
            continue

        for _ in range(per_row):
            field_name = rng.choice(candidates)
            try:
                true_value = Decimal(str(row[field_name]).replace(",", ""))
            except Exception:  # noqa: BLE001
                continue
            if true_value <= 0:
                continue

            style = rng.choice(styles)
            corrupt = rng.random() < 0.5

            if not corrupt:
                text = render(true_value, style, rng)
                out.append(Generated(
                    NumericClaim(text, field_name, str(row.get("accession_number", "")),
                                 is_hedged(text)),
                    row, "correct", style,
                ))
                continue

            error = rng.choice(errors)
            shown = true_value
            cited_field = field_name

            if error == "wrong_field":
                others = [
                    f for f in candidates
                    if f != field_name and row.get(f) not in (None, "", "Indefinite")
                ]
                if not others:
                    continue
                try:
                    shown = Decimal(str(row[rng.choice(others)]).replace(",", ""))
                except Exception:  # noqa: BLE001
                    continue
                if shown == true_value:
                    continue

            elif error == "transposed":
                digits = list(f"{true_value:.0f}")
                if len(digits) < 3:
                    continue
                i = rng.randrange(len(digits) - 1)
                if digits[i] == digits[i + 1]:
                    continue
                digits[i], digits[i + 1] = digits[i + 1], digits[i]
                shown = Decimal("".join(digits))

            elif error == "scale_error":
                shown = true_value * Decimal(1000)

            elif error == "stale":
                siblings = [
                    r for r in by_cik.get(str(row.get("cik", "")), [])
                    if r is not row and r.get(field_name) not in (None, "", "Indefinite")
                ]
                if not siblings:
                    continue
                try:
                    shown = Decimal(str(rng.choice(siblings)[field_name]).replace(",", ""))
                except Exception:  # noqa: BLE001
                    continue
                if shown == true_value:
                    continue

            text = render(shown, style, rng)
            out.append(Generated(
                NumericClaim(text, cited_field, str(row.get("accession_number", "")),
                             is_hedged(text)),
                row, error, style,
            ))

    return out


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------

def evaluate(generated: list[Generated]) -> dict:
    """Coverage, per-error sensitivity, and false alarms, against the baseline."""
    verdicts = Counter()
    naive_verdicts = Counter()
    by_error: dict[str, Counter] = {}
    by_error_naive: dict[str, Counter] = {}
    by_style: dict[str, Counter] = {}

    for item in generated:
        verdict = verify_claim(item.claim, item.source_row).verdict
        naive = naive_verify(item.claim, item.source_row)

        verdicts[verdict] += 1
        naive_verdicts[naive] += 1
        by_error.setdefault(item.truth, Counter())[verdict] += 1
        by_error_naive.setdefault(item.truth, Counter())[naive] += 1
        by_style.setdefault(item.style, Counter())[verdict] += 1

    total = len(generated)
    checkable = total - verdicts[NOT_CHECKABLE] - verdicts[SOURCE_MISSING]

    correct = by_error.get("correct", Counter())
    n_correct = sum(correct.values())
    false_alarm = correct[CONTRADICTED] / n_correct if n_correct else 0.0

    naive_correct = by_error_naive.get("correct", Counter())
    n_naive_correct = sum(naive_correct.values())
    naive_false_alarm = (
        naive_correct[CONTRADICTED] / n_naive_correct if n_naive_correct else 0.0
    )

    sensitivity: dict[str, dict] = {}
    for error, counts in by_error.items():
        if error == "correct":
            continue
        n = sum(counts.values())
        naive_counts = by_error_naive.get(error, Counter())
        sensitivity[error] = {
            "n": n,
            "caught": counts[CONTRADICTED] / n if n else 0.0,
            "missed_as_verified": counts[VERIFIED] / n if n else 0.0,
            "not_checkable": counts[NOT_CHECKABLE] / n if n else 0.0,
            "naive_caught": (
                naive_counts[CONTRADICTED] / n if n else 0.0
            ),
        }

    return {
        "n_claims": total,
        "coverage": checkable / total if total else 0.0,
        "false_alarm_rate": false_alarm,
        "naive_false_alarm_rate": naive_false_alarm,
        "verdicts": dict(verdicts),
        "naive_verdicts": dict(naive_verdicts),
        "sensitivity": sensitivity,
        "by_style": {s: dict(c) for s, c in by_style.items()},
    }


def report(results: dict) -> str:
    lines = [
        "",
        "  EXP-003 — deterministic verification of quantitative claims",
        "  " + "=" * 70,
        f"  claims generated: {results['n_claims']}",
        f"  coverage (decidable at all): {results['coverage']:.1%}",
        "",
        "  false alarms on correct claims:",
        f"    precision-aware verifier {results['false_alarm_rate']:.2%}",
        f"    naive string equality    {results['naive_false_alarm_rate']:.2%}",
        "",
        "  detection of injected errors (caught = flagged as contradicted):",
    ]
    for error, info in sorted(results["sensitivity"].items()):
        lines.append(
            f"    {error:<14} n={info['n']:<6} caught {info['caught']:>6.1%}   "
            f"missed {info['missed_as_verified']:>6.1%}   "
            f"naive caught {info['naive_caught']:>6.1%}"
        )

    lines += ["", "  by claim style:"]
    for style, counts in sorted(results["by_style"].items()):
        total = sum(counts.values())
        lines.append(f"    {style:<10} n={total:<6} {dict(counts)}")

    coverage_ok = results["coverage"] >= 0.40
    adds_value = (
        results["naive_false_alarm_rate"] - results["false_alarm_rate"] > 0.05
    )
    lines += [
        "",
        "  " + "-" * 70,
        f"  coverage >= 40%: {'PASS' if coverage_ok else 'FAIL'}",
        f"  beats naive baseline: {'PASS' if adds_value else 'FAIL'}",
    ]
    return "\n".join(lines)


def main() -> None:
    rows = load_rows()
    if not rows:
        print("  no Form D dataset found; cannot run on real data")
        return

    generated = build_claims(rows)
    print(f"  generated {len(generated)} claims from {len(rows)} filings")

    results = evaluate(generated)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(report(results))


if __name__ == "__main__":
    main()
