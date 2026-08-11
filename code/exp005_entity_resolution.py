"""EXP-005 — Is private-market entity resolution actually hard?

Why this experiment
-------------------
Every job posting and outsourcing price list gathered for this question describes
the same verb: *match*. PitchBook pays a Seattle associate to audit an offshore
team's output; S&P pays analysts to clear QC exceptions on fund documents;
freelance bidders assemble one investor list out of five overlapping sources.
Reading a document is no longer the bottleneck. Deciding whether two records
denote the same entity still is — or so the spending pattern suggests.

That claim has to be tested, not assumed, because entity resolution is a mature
field. If ordinary fuzzy string matching resolves these entities well, the money
being spent is inertia and there is nothing to build.

The test
--------
SEC Form D filings carry a CIK, which is a *true* identity assigned by the
regulator. Issuer names are entered by filers as free text. So the same CIK gives
name variants that are known to be the same entity, and different CIKs give names
known to be different — a ground truth that costs nothing to obtain and that
nobody had to label.

Measured on that ground truth:

* **Baseline**: token-set similarity, the standard approach.
* **Hard negatives**: different CIKs whose names are nearly identical. These are
  what an offshore analyst gets wrong and what a reviewer is paid to catch.
* **Hard positives**: same CIK, names that look nothing alike (rebrand, "Inc."
  dropped, DBA, holding-company restructure).

The two error classes matter separately. A matcher that scores well overall while
failing on hard negatives is worse than useless in this domain, because a false
merge silently corrupts a database and a false split merely duplicates a row.

Declared before running: if the baseline exceeds ~95% accuracy on hard negatives,
the problem is solved and H3 dies.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "datasets" / "processed" / "sec_form_d" / "formd.sqlite"
# Distinct from experiments/EXP-005, which holds the value-of-information
# diagnosis. Both experiments were originally numbered EXP-005 and wrote the same
# results.json, so whichever ran second silently destroyed the other's artefact.
# The VoI folder keeps the number because the agenda and the working paper cite it;
# this one is disambiguated instead.
OUT = ROOT / "experiments" / "EXP-005-ER"
SEED = 20260728

# Corporate form suffixes carry no identity information and dominate token
# overlap if left in: "Acme Holdings LLC" and "Beta Holdings LLC" share two of
# three tokens while being unrelated companies.
LEGAL_SUFFIXES = {
    "inc", "incorporated", "llc", "l l c", "lp", "l p", "llp", "ltd", "limited",
    "corp", "corporation", "co", "company", "plc", "sa", "nv", "bv", "gmbh",
    "ag", "kk", "pte", "pty", "trust", "fund", "partners", "partnership",
    "holdings", "holding", "group", "capital", "ventures", "venture",
    "management", "advisors", "advisers", "associates", "the", "and",
}


def normalise(name: str) -> str:
    text = (name or "").lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(name: str, drop_suffixes: bool = True) -> set[str]:
    parts = normalise(name).split()
    if drop_suffixes:
        parts = [p for p in parts if p not in LEGAL_SUFFIXES]
    return set(parts)


def token_set_ratio(a: str, b: str) -> float:
    """Jaccard similarity over identity-bearing tokens."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        # Everything was a legal suffix; fall back to the raw form rather than
        # returning zero, which would call "The Company LLC" unlike itself.
        ta, tb = tokens(a, False), tokens(b, False)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def sequence_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def combined(a: str, b: str) -> float:
    """The pragmatic default: whichever signal is stronger."""
    return max(token_set_ratio(a, b), sequence_ratio(a, b))


@dataclass
class Pair:
    name_a: str
    name_b: str
    same_entity: bool
    stratum: str


def load_name_groups(limit: int = 60_000) -> dict[str, set[str]]:
    """CIK -> set of issuer names used in filings. CIK is the ground truth."""
    if not DB.exists():
        return {}

    conn = sqlite3.connect(DB)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(filings)").fetchall()]
    lookup = {c.lower(): c for c in cols}
    cik_col = lookup.get("cik")
    name_col = lookup.get("entityname")
    if not cik_col or not name_col:
        conn.close()
        return {}

    groups: dict[str, set[str]] = defaultdict(set)
    for cik, name in conn.execute(
        f"SELECT {cik_col}, {name_col} FROM filings "
        f"WHERE {name_col} IS NOT NULL LIMIT {limit}"
    ):
        if cik and name:
            groups[str(cik)].add(str(name).strip())
    conn.close()
    return groups


def build_pairs(groups: dict[str, set[str]]) -> list[Pair]:
    """Construct positives and negatives, including deliberately hard ones."""
    import random

    rng = random.Random(SEED)
    pairs: list[Pair] = []

    # --- positives: same CIK, different name strings -----------------------
    multi = {cik: names for cik, names in groups.items() if len(names) > 1}
    for cik, names in multi.items():
        ordered = sorted(names)
        for i, a in enumerate(ordered):
            for b in ordered[i + 1:]:
                similarity = combined(a, b)
                # A rebrand or restructure shows up as a same-entity pair whose
                # names barely resemble each other. These are the expensive ones.
                stratum = "positive_hard" if similarity < 0.60 else "positive_easy"
                pairs.append(Pair(a, b, True, stratum))

    # --- negatives: different CIK ------------------------------------------
    # Random negatives are trivially separable and would flatter any method, so
    # hard negatives are built by blocking on a shared identity token.
    # Both `names` and `tokens(...)` are sets of strings. Iterating a string set
    # yields a different order in every process, because string hashing is
    # randomised per interpreter, so the blocking lists were built in a different
    # order on each run and `hard_negatives[:6000]` selected a different subset.
    # A reproducibility check caught this: the reported balanced accuracies moved
    # by about 0.2 points between runs. Sorting fixes the order without changing
    # what is sampled from.
    by_token: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for cik, names in sorted(groups.items()):
        for name in sorted(names):
            for token in sorted(tokens(name)):
                if len(token) > 3:
                    by_token[token].append((cik, name))

    hard_negatives: list[Pair] = []
    for token, entries in sorted(by_token.items()):
        if len(entries) < 2 or len(entries) > 400:
            continue
        rng.shuffle(entries)
        for i in range(min(len(entries) - 1, 6)):
            cik_a, name_a = entries[i]
            cik_b, name_b = entries[i + 1]
            if cik_a == cik_b:
                continue
            if combined(name_a, name_b) >= 0.50:
                hard_negatives.append(Pair(name_a, name_b, False, "negative_hard"))

    rng.shuffle(hard_negatives)
    pairs.extend(hard_negatives[:6000])

    # Sorted for the same reason: `rng.sample` over a list whose order varies per
    # process is not reproducible even with a fixed seed.
    all_names = [(cik, n) for cik, names in sorted(groups.items()) for n in sorted(names)]
    easy = 0
    target_easy = min(6000, len(pairs))
    while easy < target_easy and len(all_names) > 2:
        (cik_a, name_a), (cik_b, name_b) = rng.sample(all_names, 2)
        if cik_a == cik_b:
            continue
        pairs.append(Pair(name_a, name_b, False, "negative_easy"))
        easy += 1

    return pairs


def evaluate(pairs: list[Pair], threshold: float = 0.75) -> dict:
    """Accuracy overall and per stratum, plus the best achievable threshold."""
    by_stratum: dict[str, Counter] = defaultdict(Counter)
    scores: list[tuple[float, bool]] = []

    for pair in pairs:
        score = combined(pair.name_a, pair.name_b)
        predicted = score >= threshold
        scores.append((score, pair.same_entity))
        outcome = "correct" if predicted == pair.same_entity else "wrong"
        by_stratum[pair.stratum][outcome] += 1

    # Sweep the threshold to give the method its best shot, so a negative result
    # cannot be blamed on a badly chosen cut-off.
    best = {"threshold": threshold, "balanced_accuracy": 0.0}
    for candidate in [i / 100 for i in range(30, 100, 2)]:
        tp = sum(1 for s, y in scores if y and s >= candidate)
        fn = sum(1 for s, y in scores if y and s < candidate)
        tn = sum(1 for s, y in scores if not y and s < candidate)
        fp = sum(1 for s, y in scores if not y and s >= candidate)
        sens = tp / (tp + fn) if tp + fn else 0.0
        spec = tn / (tn + fp) if tn + fp else 0.0
        balanced = (sens + spec) / 2
        if balanced > best["balanced_accuracy"]:
            best = {
                "threshold": candidate,
                "balanced_accuracy": balanced,
                "sensitivity": sens,
                "specificity": spec,
            }

    strata = {}
    for stratum, counts in by_stratum.items():
        n = sum(counts.values())
        strata[stratum] = {
            "n": n,
            "accuracy": counts["correct"] / n if n else 0.0,
        }

    return {
        "n_pairs": len(pairs),
        "threshold_used": threshold,
        "strata": strata,
        "best_threshold": best,
    }


def examples(pairs: list[Pair], stratum: str, n: int = 8) -> list[tuple[str, str, float]]:
    out = []
    for pair in pairs:
        if pair.stratum != stratum:
            continue
        out.append((pair.name_a, pair.name_b, round(combined(pair.name_a, pair.name_b), 3)))
        if len(out) >= n:
            break
    return out


def report(results: dict, pairs: list[Pair]) -> str:
    lines = [
        "",
        "  EXP-005 — is private-market entity resolution hard?",
        "  " + "=" * 68,
        f"  pairs: {results['n_pairs']}   ground truth: SEC CIK",
        f"  matcher: max(token-set Jaccard, sequence ratio), suffixes stripped",
        "",
        f"  at threshold {results['threshold_used']}:",
    ]
    order = ["positive_easy", "positive_hard", "negative_easy", "negative_hard"]
    for stratum in order:
        info = results["strata"].get(stratum)
        if not info:
            continue
        lines.append(
            f"    {stratum:<16} n={info['n']:<6} accuracy {info['accuracy']:>6.1%}"
        )

    best = results["best_threshold"]
    lines += [
        "",
        f"  best achievable threshold {best['threshold']:.2f}: "
        f"balanced accuracy {best['balanced_accuracy']:.1%} "
        f"(sensitivity {best.get('sensitivity', 0):.1%}, "
        f"specificity {best.get('specificity', 0):.1%})",
    ]

    hard_neg = results["strata"].get("negative_hard", {}).get("accuracy", 0.0)
    lines += [
        "",
        "  hard negatives — different companies, similar names:",
    ]
    for a, b, score in examples(pairs, "negative_hard"):
        lines.append(f"    {score:.2f}  {a[:44]:<46} | {b[:44]}")

    lines += ["", "  hard positives — same company, dissimilar names:"]
    for a, b, score in examples(pairs, "positive_hard"):
        lines.append(f"    {score:.2f}  {a[:44]:<46} | {b[:44]}")

    solved = hard_neg >= 0.95
    lines += [
        "",
        "  " + "-" * 68,
        f"  hard-negative accuracy {hard_neg:.1%} — "
        f"{'problem already solved, H3 dies' if solved else 'not solved by standard matching'}",
    ]
    return "\n".join(lines)


def main() -> None:
    groups = load_name_groups()
    if not groups:
        print("  no Form D name data available")
        return

    multi = sum(1 for names in groups.values() if len(names) > 1)
    print(f"  {len(groups)} CIKs, {multi} with more than one name variant")

    pairs = build_pairs(groups)
    print(f"  built {len(pairs)} labelled pairs")

    results = evaluate(pairs)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(report(results, pairs))


if __name__ == "__main__":
    main()
