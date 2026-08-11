"""EXP-011 — Do the tools the market actually uses close the EXP-006 gap?

EXP-006 reported a string ceiling of 81.1% balanced accuracy on 13,773 SEC-CIK
labelled pairs, with hard positives at 0-11%. It also recorded the objection that
had to be tested next, in its own words: whether a stronger baseline with blocking
plus probabilistic matching, Splink-style, closes the gap. Until that is run, the
ceiling is a ceiling on *my* seven matchers, not on the state of the art.

This experiment runs the real tools.

Two directions, both required for the comparison to mean anything:

A. **Market tools on our data** — Splink (the open-source standard for
   probabilistic record linkage, Fellegi-Sunter with EM) and the Fellegi-Sunter
   ECM classifier plus a supervised classifier from `recordlinkage`.

B. **Our method on their data** — the same suffix-stripping token matcher run on
   FEBRL, a standard record-linkage benchmark bundled with `recordlinkage`, so the
   claim "our matcher is reasonable" is tested outside the dataset that produced it.

Two methodological corrections to EXP-006, both of which should reduce the
headline number rather than flatter it:

1. **Train/test split.** EXP-006 swept the threshold on the same pairs it scored,
   so 81.1% is an *in-sample* figure. Every method here selects its threshold or
   fits its parameters on a train half and is scored on a held-out test half.
   The in-sample number is also reported so the two are comparable.
2. **Blocking counts against recall.** Splink only scores pairs its blocking rules
   generate. Pairs it never proposes are counted as predicted non-matches, because
   that is what happens in production. Blocking coverage is reported separately.

`dedupe` is absent deliberately: it needs a C++ toolchain to build affinegap,
PyLBFGS and dedupe-Levenshtein-search, which was not available on this machine.
The Fellegi-Sunter ECM classifier stands in for the same supervised/probabilistic
family. Installing dedupe remains an open item.
"""

from __future__ import annotations

import json
import random
import sys
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path

warnings.filterwarnings("ignore")

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd  # noqa: E402

from exp005_entity_resolution import (  # noqa: E402
    Pair,
    build_pairs,
    combined,
    load_name_groups,
    normalise,
    tokens,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-011"
SEED = 20260730
STRATA = ("positive_easy", "positive_hard", "negative_easy", "negative_hard")


# ---------------------------------------------------------------------------
# shared evaluation
# ---------------------------------------------------------------------------

def split_pairs(pairs: list[Pair]) -> tuple[list[Pair], list[Pair]]:
    """Stratified half/half split, so threshold choice cannot see the test set."""
    rng = random.Random(SEED)
    by_stratum: dict[str, list[Pair]] = defaultdict(list)
    for p in pairs:
        by_stratum[p.stratum].append(p)
    train, test = [], []
    for stratum in sorted(by_stratum):
        group = by_stratum[stratum][:]
        rng.shuffle(group)
        cut = len(group) // 2
        train.extend(group[:cut])
        test.extend(group[cut:])
    return train, test


def pick_threshold(scored: list[tuple[float, bool]]) -> float:
    """Threshold maximising balanced accuracy, chosen on TRAIN only."""
    best_t, best_b = 0.5, -1.0
    for i in range(1, 100):
        t = i / 100
        tp = sum(1 for s, y in scored if y and s >= t)
        fn = sum(1 for s, y in scored if y and s < t)
        tn = sum(1 for s, y in scored if not y and s < t)
        fp = sum(1 for s, y in scored if not y and s >= t)
        sens = tp / (tp + fn) if tp + fn else 0.0
        spec = tn / (tn + fp) if tn + fp else 0.0
        b = (sens + spec) / 2
        if b > best_b:
            best_b, best_t = b, t
    return best_t


def score_at(scored: list[tuple[float, bool]], threshold: float) -> dict:
    tp = sum(1 for s, y in scored if y and s >= threshold)
    fn = sum(1 for s, y in scored if y and s < threshold)
    tn = sum(1 for s, y in scored if not y and s < threshold)
    fp = sum(1 for s, y in scored if not y and s >= threshold)
    sens = tp / (tp + fn) if tp + fn else 0.0
    spec = tn / (tn + fp) if tn + fp else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    f1 = 2 * precision * sens / (precision + sens) if precision + sens else 0.0
    return {
        "balanced_accuracy": (sens + spec) / 2,
        "sensitivity": sens,
        "specificity": spec,
        "precision": precision,
        "f1": f1,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
    }


def evaluate(
    name: str,
    train: list[Pair],
    test: list[Pair],
    scores_train: list[float],
    scores_test: list[float],
    elapsed: float,
) -> dict:
    from sklearn.metrics import average_precision_score, roc_auc_score

    st = list(zip(scores_train, [p.same_entity for p in train]))
    se = list(zip(scores_test, [p.same_entity for p in test]))
    threshold = pick_threshold(st)

    y_test = [p.same_entity for p in test]
    # Threshold-free and stratum-free, so immune to the stratification
    # circularity documented in the module docstring.
    try:
        auc = roc_auc_score(y_test, scores_test)
        ap = average_precision_score(y_test, scores_test)
    except Exception:
        auc, ap = float("nan"), float("nan")

    out = {
        "method": name,
        "threshold_from_train": threshold,
        "in_sample_train": score_at(st, threshold),
        "out_of_sample_test": score_at(se, threshold),
        "oracle_threshold_on_test": score_at(se, pick_threshold(se)),
        "roc_auc_test": auc,
        "average_precision_test": ap,
        "seconds": round(elapsed, 2),
        "strata_test": {},
    }
    for stratum in STRATA:
        subset = [(s, p.same_entity) for s, p in zip(scores_test, test)
                  if p.stratum == stratum]
        if not subset:
            continue
        correct = sum(1 for s, y in subset if (s >= threshold) == y)
        out["strata_test"][stratum] = {
            "n": len(subset),
            "accuracy": correct / len(subset),
        }
    return out


# ---------------------------------------------------------------------------
# A1. our own baseline, with the split applied
# ---------------------------------------------------------------------------

def run_ours(train: list[Pair], test: list[Pair]) -> dict:
    t0 = time.time()
    st = [combined(p.name_a, p.name_b) for p in train]
    se = [combined(p.name_a, p.name_b) for p in test]
    return evaluate("ours_string_combined", train, test, st, se, time.time() - t0)


# ---------------------------------------------------------------------------
# A2. Splink
# ---------------------------------------------------------------------------

def build_records(pairs: list[Pair]) -> tuple[pd.DataFrame, dict[str, int]]:
    """One record per distinct name string, which is what a linkage tool sees."""
    names = sorted({p.name_a for p in pairs} | {p.name_b for p in pairs})
    index = {n: i for i, n in enumerate(names)}
    rows = []
    for n, i in index.items():
        toks = sorted(tokens(n))
        rows.append({
            "unique_id": i,
            "name_norm": normalise(n),
            "first_token": toks[0] if toks else "",
            "last_token": toks[-1] if toks else "",
            "n_tokens": len(toks),
        })
    return pd.DataFrame(rows), index


def run_splink(train: list[Pair], test: list[Pair]) -> dict:
    import splink.comparison_library as cl
    from splink import DuckDBAPI, Linker, SettingsCreator, block_on

    t0 = time.time()
    allp = train + test
    df, index = build_records(allp)

    settings = SettingsCreator(
        link_type="dedupe_only",
        comparisons=[
            cl.JaroWinklerAtThresholds("name_norm", [0.95, 0.88, 0.8, 0.7]),
            cl.ExactMatch("first_token"),
            cl.ExactMatch("last_token"),
        ],
        blocking_rules_to_generate_predictions=[
            block_on("first_token"),
            block_on("last_token"),
            block_on("n_tokens", "first_token"),
        ],
        retain_intermediate_calculation_columns=False,
    )

    linker = Linker(df, settings, db_api=DuckDBAPI())
    linker.training.estimate_u_using_random_sampling(max_pairs=2_000_000, seed=SEED)
    for rule in (block_on("first_token"), block_on("last_token")):
        try:
            linker.training.estimate_parameters_using_expectation_maximisation(rule)
        except Exception as exc:  # EM can fail to converge on a block
            print(f"    splink EM skipped for a rule: {type(exc).__name__}")

    preds = linker.inference.predict().as_pandas_dataframe()
    lookup: dict[tuple[int, int], float] = {}
    for a, b, p in zip(preds["unique_id_l"], preds["unique_id_r"],
                       preds["match_probability"]):
        key = (int(a), int(b)) if int(a) < int(b) else (int(b), int(a))
        lookup[key] = max(lookup.get(key, 0.0), float(p))

    def score(pair: Pair) -> float:
        ia, ib = index[pair.name_a], index[pair.name_b]
        if ia == ib:
            return 1.0
        key = (ia, ib) if ia < ib else (ib, ia)
        # Not proposed by blocking means not a match in production.
        return lookup.get(key, 0.0)

    st = [score(p) for p in train]
    se = [score(p) for p in test]
    result = evaluate("splink_4", train, test, st, se, time.time() - t0)

    proposed = sum(1 for p in allp
                   if (lambda ia, ib: (min(ia, ib), max(ia, ib)) in lookup)
                   (index[p.name_a], index[p.name_b]))
    result["blocking_coverage_all_pairs"] = proposed / len(allp)
    result["blocking_coverage_by_stratum"] = {}
    for stratum in STRATA:
        sub = [p for p in allp if p.stratum == stratum]
        if not sub:
            continue
        hit = sum(1 for p in sub
                  if (min(index[p.name_a], index[p.name_b]),
                      max(index[p.name_a], index[p.name_b])) in lookup)
        result["blocking_coverage_by_stratum"][stratum] = hit / len(sub)
    result["n_candidate_pairs_generated"] = int(len(preds))
    return result


# ---------------------------------------------------------------------------
# A3. recordlinkage — Fellegi-Sunter ECM (unsupervised) and supervised LR
# ---------------------------------------------------------------------------

def comparison_vectors(pairs: list[Pair]) -> pd.DataFrame:
    import recordlinkage as rl

    left = pd.DataFrame({
        "name_norm": [normalise(p.name_a) for p in pairs],
        "first_token": [(sorted(tokens(p.name_a)) or [""])[0] for p in pairs],
        "last_token": [(sorted(tokens(p.name_a)) or [""])[-1] for p in pairs],
    })
    right = pd.DataFrame({
        "name_norm": [normalise(p.name_b) for p in pairs],
        "first_token": [(sorted(tokens(p.name_b)) or [""])[0] for p in pairs],
        "last_token": [(sorted(tokens(p.name_b)) or [""])[-1] for p in pairs],
    })
    left.index.name = "a"
    right.index.name = "b"
    idx = pd.MultiIndex.from_arrays([left.index, right.index])

    compare = rl.Compare()
    compare.string("name_norm", "name_norm", method="jarowinkler",
                   threshold=None, label="jw")
    compare.string("name_norm", "name_norm", method="levenshtein",
                   threshold=None, label="lev")
    compare.exact("first_token", "first_token", label="first")
    compare.exact("last_token", "last_token", label="last")
    return compare.compute(idx, left, right)


def run_recordlinkage(train: list[Pair], test: list[Pair]) -> list[dict]:
    import recordlinkage as rl

    results = []
    vt = comparison_vectors(train)
    ve = comparison_vectors(test)

    # Fellegi-Sunter ECM: unsupervised, the classical probabilistic method.
    try:
        t0 = time.time()
        ecm = rl.ECMClassifier(binarize=0.85)
        ecm.fit(vt)
        st = list(ecm.prob(vt))
        se = list(ecm.prob(ve))
        results.append(evaluate("recordlinkage_fellegi_sunter_ecm",
                                train, test, st, se, time.time() - t0))
    except Exception as exc:
        print(f"    ECM failed: {type(exc).__name__}: {exc}")

    # Supervised logistic regression on the same comparison vectors. This is the
    # strongest classical option and it gets to see the labels, so it is the
    # upper end of the family rather than a like-for-like baseline.
    try:
        t0 = time.time()
        lr = rl.LogisticRegressionClassifier()
        # recordlinkage wants the index of the matching pairs, not a boolean Series.
        match_index = vt.index[[p.same_entity for p in train]]
        lr.fit(vt, match_index)
        st = list(lr.prob(vt))
        se = list(lr.prob(ve))
        results.append(evaluate("recordlinkage_logistic_supervised",
                                train, test, st, se, time.time() - t0))
    except Exception as exc:
        print(f"    LR failed: {type(exc).__name__}: {exc}")

    return results


# ---------------------------------------------------------------------------
# B. our method on a standard benchmark
# ---------------------------------------------------------------------------

def run_on_febrl() -> dict:
    """Our name matcher on FEBRL, a standard record-linkage benchmark.

    FEBRL is synthetic person records, not companies. That is the point: it tests
    whether the matcher is reasonable outside the data that produced it. A weak
    result here narrows the claim to company entities rather than refuting it.
    """
    import recordlinkage as rl
    from recordlinkage.datasets import load_febrl4

    dfa, dfb, links = load_febrl4(return_links=True)

    def name_of(df: pd.DataFrame) -> pd.Series:
        return (df["given_name"].fillna("") + " " + df["surname"].fillna("")).str.strip()

    name_a, name_b = name_of(dfa), name_of(dfb)

    # Blocking, otherwise the candidate set is 25 million pairs.
    indexer = rl.Index()
    indexer.block("given_name")
    indexer.block("surname")
    candidates = indexer.index(dfa, dfb)

    truth = set(map(tuple, links.to_frame(index=False).values)) if hasattr(
        links, "to_frame") else set(links)

    rng = random.Random(SEED)
    cand = list(candidates)
    rng.shuffle(cand)
    cand = cand[:40_000]

    # Stratified exactly as build_pairs does on our data: a positive whose names
    # barely resemble each other is "hard". Without this the pos_hard column is
    # not comparable across the two datasets, which is the whole point of running
    # the same matcher on both.
    pairs: list[Pair] = []
    for a, b in cand:
        na, nb = str(name_a.get(a, "")), str(name_b.get(b, ""))
        same = (a, b) in truth
        similarity = combined(na, nb)
        if same:
            stratum = "positive_hard" if similarity < 0.60 else "positive_easy"
        else:
            stratum = "negative_hard" if similarity >= 0.50 else "negative_easy"
        pairs.append(Pair(na, nb, same, stratum))

    train, test = split_pairs(pairs)
    t0 = time.time()
    st = [combined(p.name_a, p.name_b) for p in train]
    se = [combined(p.name_a, p.name_b) for p in test]
    ours = evaluate("ours_on_febrl", train, test, st, se, time.time() - t0)
    ours["n_pairs"] = len(pairs)
    ours["positive_rate"] = sum(1 for p in pairs if p.same_entity) / len(pairs)

    rl_results = []
    try:
        vt, ve = comparison_vectors(train), comparison_vectors(test)
        t0 = time.time()
        lr = rl.LogisticRegressionClassifier()
        lr.fit(vt, vt.index[[p.same_entity for p in train]])
        rl_results.append(evaluate("recordlinkage_logistic_on_febrl", train, test,
                                   list(lr.prob(vt)), list(lr.prob(ve)),
                                   time.time() - t0))
    except Exception as exc:
        print(f"    FEBRL LR failed: {type(exc).__name__}: {exc}")

    return {"ours": ours, "baselines": rl_results}


# ---------------------------------------------------------------------------

def table(rows: list[dict]) -> str:
    lines = [
        "",
        f"  {'method':<36} {'bal':>7} {'AUC':>7} {'AP':>7} {'f1':>6} "
        f"{'pos_hard':>9} {'neg_hard':>9} {'sec':>6}",
        "  " + "-" * 94,
    ]
    for r in rows:
        s = r.get("strata_test", {})
        lines.append(
            f"  {r['method']:<36} "
            f"{r['out_of_sample_test']['balanced_accuracy']:>6.1%} "
            f"{r.get('roc_auc_test', float('nan')):>7.3f} "
            f"{r.get('average_precision_test', float('nan')):>7.3f} "
            f"{r['out_of_sample_test']['f1']:>6.3f} "
            f"{s.get('positive_hard', {}).get('accuracy', float('nan')):>8.1%} "
            f"{s.get('negative_hard', {}).get('accuracy', float('nan')):>8.1%} "
            f"{r['seconds']:>6.1f}"
        )
    lines.append("  bal/pos_hard/neg_hard are out-of-sample; AUC and AP are "
                 "threshold-free and stratum-free.")
    return "\n".join(lines)


def main() -> None:
    groups = load_name_groups()
    if not groups:
        print("  no Form D name data")
        return
    pairs = build_pairs(groups)
    train, test = split_pairs(pairs)
    print(f"  {len(pairs)} pairs -> {len(train)} train / {len(test)} test")
    print("  strata:", dict(Counter(p.stratum for p in pairs)))

    rows = [run_ours(train, test)]

    print("  running splink ...")
    try:
        rows.append(run_splink(train, test))
    except Exception as exc:
        print(f"    splink failed: {type(exc).__name__}: {exc}")

    print("  running recordlinkage ...")
    try:
        rows.extend(run_recordlinkage(train, test))
    except Exception as exc:
        print(f"    recordlinkage failed: {type(exc).__name__}: {exc}")

    print("  running our matcher on FEBRL ...")
    febrl = None
    try:
        febrl = run_on_febrl()
    except Exception as exc:
        print(f"    FEBRL failed: {type(exc).__name__}: {exc}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(
        json.dumps({"our_data": rows, "their_data_febrl": febrl}, indent=2,
                   default=str),
        encoding="utf-8",
    )

    print("\n  A. market tools on OUR data (SEC CIK ground truth)")
    print(table(rows))

    splink_row = next((r for r in rows if r["method"] == "splink_4"), None)
    if splink_row:
        print(f"\n  splink candidate pairs generated: "
              f"{splink_row['n_candidate_pairs_generated']:,}")
        print(f"  splink blocking coverage of our labelled pairs: "
              f"{splink_row['blocking_coverage_all_pairs']:.1%}")
        for k, v in splink_row["blocking_coverage_by_stratum"].items():
            print(f"    {k:<16} {v:>6.1%}")

    if febrl:
        print("\n  B. OUR matcher on THEIR data (FEBRL4, standard benchmark)")
        print(table([febrl["ours"]] + febrl["baselines"]))
        print(f"\n  febrl pairs {febrl['ours']['n_pairs']:,}, "
              f"positive rate {febrl['ours']['positive_rate']:.2%}")

    print(f"\n  written {OUT / 'results.json'}")


if __name__ == "__main__":
    main()
