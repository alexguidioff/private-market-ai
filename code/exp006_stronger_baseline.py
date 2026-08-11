"""EXP-006 — Does a stronger matcher close the gap EXP-005 found?

EXP-005 reported 73.3% accuracy on hard negatives with `max(Jaccard, sequence
ratio)` after stripping legal suffixes, and 0% on hard positives. Before treating
that as a real gap, the obvious objection has to be tested: the matcher was
simple, and suffix stripping itself caused some false merges ("GOBI INVESTMENT
PARTNERS LP" and "GOBI INVESTMENT FUND LTD." became identical). A stronger
baseline might close it, in which case H3 collapses.

So this runs progressively stronger matchers on the same pairs:

1. **No suffix stripping** — tests whether stripping caused the false merges.
2. **Weighted tokens (IDF)** — rare tokens carry identity, common ones do not.
   "Barrington" distinguishes; "Holdings" does not. This is the single most
   effective classical improvement and the core of what probabilistic matchers do.
3. **Head-token agreement** — company identity concentrates in the leading
   distinctive word.
4. **Character n-grams** — robust to spelling and word-order variation.
5. **Combined, threshold-swept** — every signal, given its best cut-off.

Then the same question is asked of the *hard positives*, where no string method
can plausibly work, to test whether the failure there is intrinsic.

Finally, the informative test: does adding **non-name evidence already present in
the filings** (state, industry, address, filing timeline) separate the cases that
strings cannot? That is the claim worth checking, because that evidence is what a
point-in-time pipeline produces and what an offshore analyst is paid to look up
by hand.
"""

from __future__ import annotations

import json
import math
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp005_entity_resolution import (  # noqa: E402
    LEGAL_SUFFIXES,
    Pair,
    build_pairs,
    normalise,
    sequence_ratio,
    token_set_ratio,
    tokens,
)

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "datasets" / "processed" / "sec_form_d" / "formd.sqlite"
OUT = ROOT / "experiments" / "EXP-006"


# --------------------------------------------------------------------------
# stronger string matchers
# --------------------------------------------------------------------------

def build_idf(groups: dict[str, set[str]]) -> dict[str, float]:
    """Inverse document frequency over issuer-name tokens.

    This is what makes "Barrington" count and "Holdings" not, without hand-listing
    which words are generic. It is also the mechanism inside probabilistic record
    linkage, so it stands in for that class of method.
    """
    frequency: Counter = Counter()
    total = 0
    for names in groups.values():
        for name in names:
            total += 1
            for token in set(normalise(name).split()):
                frequency[token] += 1
    return {
        token: math.log(total / count)
        for token, count in frequency.items()
        if count > 0
    }


def weighted_jaccard(a: str, b: str, idf: dict[str, float]) -> float:
    ta = set(normalise(a).split())
    tb = set(normalise(b).split())
    if not ta or not tb:
        return 0.0
    shared = sum(idf.get(t, 1.0) for t in ta & tb)
    union = sum(idf.get(t, 1.0) for t in ta | tb)
    return shared / union if union else 0.0


def head_token(name: str) -> str:
    """First identity-bearing word, which usually carries the brand."""
    for token in normalise(name).split():
        if token not in LEGAL_SUFFIXES and len(token) > 2:
            return token
    parts = normalise(name).split()
    return parts[0] if parts else ""


def ngram_similarity(a: str, b: str, n: int = 3) -> float:
    def grams(text: str) -> set[str]:
        clean = normalise(text).replace(" ", "")
        return {clean[i:i + n] for i in range(max(0, len(clean) - n + 1))}

    ga, gb = grams(a), grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


# --------------------------------------------------------------------------
# non-name evidence
# --------------------------------------------------------------------------

@dataclass
class Attributes:
    state: str = ""
    industry: str = ""
    entity_type: str = ""
    first_seen: str = ""
    last_seen: str = ""


def load_attributes_per_filing() -> dict[tuple[str, str], Attributes]:
    """Attributes keyed by (cik, name) — deliberately NOT by CIK alone.

    The first version of this experiment keyed attributes by CIK and reported
    100% attribute agreement on same-entity pairs. That was circular: a positive
    pair is *defined* as two names sharing a CIK, so looking attributes up by CIK
    returns the same record twice and agreement is guaranteed. The label was the
    lookup key. Verified directly: 1770/1770 positive pairs resolved to one CIK.

    Keying by (cik, name) means each side of a pair is described by the filings
    that actually carried that name string, which is the information a matcher
    would really have — it sees two records, not two identities.
    """
    if not DB.exists():
        return {}
    conn = sqlite3.connect(DB)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(filings)").fetchall()]
    lookup = {c.lower(): c for c in cols}

    needed = {
        "cik": lookup.get("cik"),
        "name": lookup.get("entityname"),
        "state": lookup.get("stateorcountry"),
        "industry": lookup.get("industrygrouptype"),
        "entity_type": lookup.get("entitytype"),
        "time": lookup.get("filing_time"),
    }
    if not needed["cik"] or not needed["name"]:
        conn.close()
        return {}

    select = ", ".join(c for c in needed.values() if c)
    rows = conn.execute(f"SELECT {select} FROM filings").fetchall()
    conn.close()

    keys = [k for k, v in needed.items() if v]
    out: dict[tuple[str, str], Attributes] = {}
    times: dict[tuple[str, str], list[str]] = defaultdict(list)

    for row in rows:
        record = dict(zip(keys, row))
        cik = str(record.get("cik") or "")
        name = str(record.get("name") or "").strip()
        if not cik or not name:
            continue
        key = (cik, name)
        attributes = out.setdefault(key, Attributes())
        attributes.state = attributes.state or str(record.get("state") or "")
        attributes.industry = attributes.industry or str(record.get("industry") or "")
        attributes.entity_type = attributes.entity_type or str(
            record.get("entity_type") or ""
        )
        if record.get("time"):
            times[key].append(str(record["time"]))

    for key, stamps in times.items():
        if key in out and stamps:
            out[key].first_seen = min(stamps)
            out[key].last_seen = max(stamps)
    return out


def name_to_cik(groups: dict[str, set[str]]) -> dict[str, str]:
    """Map a name string back to a CIK, only where the name is unambiguous."""
    owners: dict[str, set[str]] = defaultdict(set)
    for cik, names in groups.items():
        for name in names:
            owners[name].add(cik)
    return {name: next(iter(ciks)) for name, ciks in owners.items() if len(ciks) == 1}


def attribute_agreement(
    a: str,
    b: str,
    mapping: dict[str, str],
    attributes: dict[tuple[str, str], Attributes],
) -> dict[str, int] | None:
    """Do the non-name attributes of the two *records* agree?

    Each side is described by the filings that carried its own name string, so a
    same-entity pair is not guaranteed to agree — which is what makes this a test
    rather than a tautology.
    """
    cik_a, cik_b = mapping.get(a), mapping.get(b)
    if not cik_a or not cik_b:
        return None
    attr_a = attributes.get((cik_a, a))
    attr_b = attributes.get((cik_b, b))
    if attr_a is None or attr_b is None:
        return None

    def agree(x: str, y: str) -> int | None:
        if not x or not y:
            return None
        return int(x == y)

    fields = {
        "state": agree(attr_a.state, attr_b.state),
        "industry": agree(attr_a.industry, attr_b.industry),
        "entity_type": agree(attr_a.entity_type, attr_b.entity_type),
    }
    usable = {k: v for k, v in fields.items() if v is not None}
    return usable or None


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------

def sweep(scores: list[tuple[float, bool]]) -> dict:
    best = {"threshold": 0.0, "balanced": 0.0, "sensitivity": 0.0, "specificity": 0.0}
    for candidate in [i / 100 for i in range(5, 100, 1)]:
        tp = sum(1 for s, y in scores if y and s >= candidate)
        fn = sum(1 for s, y in scores if y and s < candidate)
        tn = sum(1 for s, y in scores if not y and s < candidate)
        fp = sum(1 for s, y in scores if not y and s >= candidate)
        sens = tp / (tp + fn) if tp + fn else 0.0
        spec = tn / (tn + fp) if tn + fp else 0.0
        balanced = (sens + spec) / 2
        if balanced > best["balanced"]:
            best = {
                "threshold": candidate,
                "balanced": balanced,
                "sensitivity": sens,
                "specificity": spec,
            }
    return best


def evaluate_matchers(pairs: list[Pair], idf: dict[str, float]) -> dict:
    matchers = {
        "jaccard_suffix_stripped": lambda a, b: token_set_ratio(a, b),
        "jaccard_suffix_kept": lambda a, b: (
            len(set(normalise(a).split()) & set(normalise(b).split()))
            / max(1, len(set(normalise(a).split()) | set(normalise(b).split())))
        ),
        "sequence_ratio": sequence_ratio,
        "char_3gram": ngram_similarity,
        "idf_weighted": lambda a, b: weighted_jaccard(a, b, idf),
        "idf_and_head": lambda a, b: (
            weighted_jaccard(a, b, idf) * (1.0 if head_token(a) == head_token(b) else 0.55)
        ),
        "best_of_all": lambda a, b: max(
            weighted_jaccard(a, b, idf), ngram_similarity(a, b), sequence_ratio(a, b)
        ),
    }

    results = {}
    for name, fn in matchers.items():
        scores = [(fn(p.name_a, p.name_b), p.same_entity) for p in pairs]
        best = sweep(scores)

        per_stratum = {}
        for stratum in ("positive_easy", "positive_hard", "negative_easy", "negative_hard"):
            subset = [
                (fn(p.name_a, p.name_b), p.same_entity)
                for p in pairs if p.stratum == stratum
            ]
            if not subset:
                continue
            correct = sum(
                1 for s, y in subset if (s >= best["threshold"]) == y
            )
            per_stratum[stratum] = {
                "n": len(subset),
                "accuracy": correct / len(subset),
            }

        results[name] = {"best": best, "strata": per_stratum}
    return results


def evaluate_attributes(
    pairs: list[Pair],
    mapping: dict[str, str],
    attributes: dict[tuple[str, str], Attributes],
) -> dict:
    """Do non-name attributes separate the cases strings cannot?"""
    buckets: dict[str, dict[str, list[int]]] = {}
    coverage = 0

    for pair in pairs:
        agreement = attribute_agreement(pair.name_a, pair.name_b, mapping, attributes)
        if agreement is None:
            continue
        coverage += 1
        bucket = buckets.setdefault(pair.stratum, defaultdict(list))
        for key, value in agreement.items():
            bucket[key].append(value)

    summary = {}
    for stratum, fields in buckets.items():
        summary[stratum] = {
            field: {
                "n": len(values),
                "agreement_rate": sum(values) / len(values) if values else 0.0,
            }
            for field, values in fields.items()
        }

    return {
        "coverage": coverage / len(pairs) if pairs else 0.0,
        "by_stratum": summary,
    }


def report(matcher_results: dict, attribute_results: dict) -> str:
    lines = [
        "",
        "  EXP-006 — can a stronger matcher close the EXP-005 gap?",
        "  " + "=" * 72,
        "",
        f"  {'matcher':<26} {'bal.acc':>8} {'thr':>5} "
        f"{'neg_hard':>9} {'pos_hard':>9} {'pos_easy':>9}",
        "  " + "-" * 72,
    ]
    for name, info in matcher_results.items():
        strata = info["strata"]
        lines.append(
            f"  {name:<26} {info['best']['balanced']:>7.1%} "
            f"{info['best']['threshold']:>5.2f} "
            f"{strata.get('negative_hard', {}).get('accuracy', 0):>8.1%} "
            f"{strata.get('positive_hard', {}).get('accuracy', 0):>8.1%} "
            f"{strata.get('positive_easy', {}).get('accuracy', 0):>8.1%}"
        )

    best_name = max(
        matcher_results, key=lambda k: matcher_results[k]["best"]["balanced"]
    )
    best = matcher_results[best_name]
    lines += [
        "",
        f"  strongest: {best_name} at balanced accuracy "
        f"{best['best']['balanced']:.1%}",
    ]

    lines += [
        "",
        "  non-name attribute agreement "
        f"(coverage {attribute_results['coverage']:.1%} of pairs):",
    ]
    for stratum in ("positive_easy", "positive_hard", "negative_easy", "negative_hard"):
        fields = attribute_results["by_stratum"].get(stratum)
        if not fields:
            continue
        parts = "  ".join(
            f"{field} {info['agreement_rate']:.0%}"
            for field, info in sorted(fields.items())
        )
        n = max(info["n"] for info in fields.values())
        lines.append(f"    {stratum:<16} n={n:<6} {parts}")

    # Does any attribute separate hard positives from hard negatives?
    pos = attribute_results["by_stratum"].get("positive_hard", {})
    neg = attribute_results["by_stratum"].get("negative_hard", {})
    lines += ["", "  separation on the cases strings cannot decide:"]
    separating = []
    for field in sorted(set(pos) | set(neg)):
        p = pos.get(field, {}).get("agreement_rate", 0.0)
        n = neg.get(field, {}).get("agreement_rate", 0.0)
        gap = p - n
        flag = "  <-- separates" if abs(gap) >= 0.15 else ""
        if abs(gap) >= 0.15:
            separating.append(field)
        lines.append(
            f"    {field:<14} same-entity {p:>5.0%}  different-entity {n:>5.0%}  "
            f"gap {gap:+.0%}{flag}"
        )

    lines += [
        "",
        "  " + "-" * 72,
        f"  string ceiling: {best['best']['balanced']:.1%} balanced accuracy",
        f"  attributes that separate beyond strings: "
        f"{', '.join(separating) if separating else 'none'}",
    ]
    return "\n".join(lines)


def main() -> None:
    from exp005_entity_resolution import load_name_groups

    groups = load_name_groups()
    if not groups:
        print("  no data")
        return

    pairs = build_pairs(groups)
    print(f"  {len(pairs)} pairs")

    idf = build_idf(groups)
    print(f"  idf vocabulary {len(idf)} tokens")

    matcher_results = evaluate_matchers(pairs, idf)

    attributes = load_attributes_per_filing()
    mapping = name_to_cik(groups)
    print(f"  attributes for {len(attributes)} (cik, name) records, "
          f"{len(mapping)} unambiguous name->cik entries")
    attribute_results = evaluate_attributes(pairs, mapping, attributes)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(
        json.dumps({"matchers": matcher_results, "attributes": attribute_results},
                   indent=2),
        encoding="utf-8",
    )
    print(report(matcher_results, attribute_results))


if __name__ == "__main__":
    main()
