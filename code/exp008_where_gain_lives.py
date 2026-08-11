"""EXP-008 — Where in the pipeline is information actually worth buying?

The question EXP-007 raised and could not answer
------------------------------------------------
EXP-007 found that under `balanced` the mean per-case gain rises monotonically as
the slice of the pipeline widens: +0.0054, +0.0055, +0.0082, +0.0104, +0.0284 for the
top 5, 10, 20, 50 and 100%. That was read as "information is worth most where the
base model is least confident", and recorded in the agenda as a hypothesis.

**That reading does not follow from the evidence, and this experiment exists because
of the gap.** The slices are nested and ranked by predicted probability descending.
The top of that ranking is confident-positive, but the *bottom* is
confident-negative, and the middle is where the model is unsure. Widening a slice
from the top therefore mixes in the uncertain middle and then the confident-negative
bottom at the same time. A monotone rise is consistent with at least two very
different pictures, and nested slices cannot separate them.

Two rival hypotheses, declared before running
---------------------------------------------
    H-uncertainty  gain peaks in the middle of the probability range and is small at
                   both extremes. Information pays where the model is genuinely
                   unsure. This is the reading the agenda recorded.

    H-descending   gain rises steadily as predicted probability falls, so it is
                   largest in the bottom decile. Information pays on the cases the
                   model is confidently negative about — a different claim, and a
                   less comfortable one, because those are the deals a fund
                   discards without diligence.

I do not know which holds. The decile profile below distinguishes them directly,
which nested slices cannot. Declaring both, and declaring that I cannot predict the
answer, is the point: EXP-007's monotonicity was over-interpreted once already.

Second question: is the divergence a property of the gain, or of one ranking?
-----------------------------------------------------------------------------
EXP-007 used a single pipeline ordering. If the top-slice estimate diverges from the
cohort under *every* plausible ordering, the divergence is a property of how gain is
distributed. If it diverges only under the probability ranking, it is a property of
that ranking, and the P5 conclusion would be narrower than EXP-007 stated.

Four orderings plus a control, all computable before buying the block:

    base probability, descending       EXP-007's, the model's own view
    base uncertainty, most-unsure first  what H-uncertainty implies you should do
    offering size, descending          a real practitioner triage: work big deals first
    investor count, descending         a second real triage: work crowded deals first
    random                             control; any apparent divergence here is noise

Declared rules
--------------
    DECILES        = 10 bins of the base probability
    MONOTONE_TEST    Spearman between decile rank and decile mean gain, with a
                     permutation null over case-to-decile assignment
    PEAK_MARGIN    = 0.010  a middle-versus-extremes contrast must clear this to
                            support H-uncertainty, the same margin used in EXP-005
                            and EXP-007
    MIN_BIN_N      = 30

No bin count, ranking or margin is changed after seeing a result. `random` is
included precisely so that the size of a null divergence is visible on the same
table as the real ones.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import p1_real_baseline as baseline  # noqa: E402
import p1_sec_history_acquisition as acq  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-008"

DECILES = 10
PEAK_MARGIN = 0.010
MIN_BIN_N = 30
BOOTSTRAP_DRAWS = 4000
PERMUTATIONS = 4000
SLICES = (0.05, 0.10, 0.20)


def interval(values: np.ndarray, alpha: float = 0.05) -> tuple[float, float]:
    if len(values) == 0:
        return (float("nan"), float("nan"))
    ordered = np.sort(values)
    return (
        float(ordered[int((alpha / 2) * len(ordered))]),
        float(ordered[min(len(ordered) - 1, int((1 - alpha / 2) * len(ordered)))]),
    )


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0

    def ranks(values: np.ndarray) -> np.ndarray:
        order = np.argsort(values)
        out = np.empty(len(values), dtype=float)
        out[order] = np.arange(len(values), dtype=float)
        return out

    return float(np.corrcoef(ranks(a), ranks(b))[0, 1])


def decile_profile(gain: np.ndarray, score: np.ndarray, seed: int) -> dict:
    """Mean gain per decile of the score, with intervals and a monotonicity test.

    Bins are equal-count rather than equal-width, so no bin is starved by the
    shape of the probability distribution.
    """
    rng = np.random.default_rng(seed)
    order = np.argsort(score)
    bins = np.array_split(order, DECILES)

    rows = []
    for index, members in enumerate(bins):
        values = gain[members]
        draws = np.array(
            [
                np.mean(values[rng.integers(0, len(values), len(values))])
                for _ in range(1000)
            ]
        )
        lo, hi = interval(draws)
        rows.append(
            {
                "decile": index + 1,
                "n": int(len(members)),
                "score_low": float(np.min(score[members])),
                "score_high": float(np.max(score[members])),
                "mean_gain": float(np.mean(values)),
                "ci": [lo, hi],
                "share_nonzero": float(np.mean(values != 0)),
            }
        )

    means = np.array([r["mean_gain"] for r in rows])
    indices = np.arange(1, DECILES + 1, dtype=float)
    rho = spearman(indices, means)

    # Permutation null: reassign cases to deciles at random, keeping bin sizes.
    # This asks whether any monotone pattern at all is present, without assuming
    # a functional form.
    null_rho = []
    sizes = [r["n"] for r in rows]
    for _ in range(PERMUTATIONS):
        shuffled = rng.permutation(gain)
        start = 0
        permuted_means = []
        for size in sizes:
            permuted_means.append(np.mean(shuffled[start : start + size]))
            start += size
        null_rho.append(abs(spearman(indices, np.array(permuted_means))))
    p_monotone = (np.sum(np.array(null_rho) >= abs(rho)) + 1) / (PERMUTATIONS + 1)

    # Middle-versus-extremes contrast: the discriminating statistic between the
    # two declared hypotheses.
    middle = means[3:7].mean()
    extremes = np.concatenate([means[:2], means[-2:]]).mean()
    bottom = means[:2].mean()
    top = means[-2:].mean()

    if middle - extremes >= PEAK_MARGIN:
        shape = "peaked_in_middle_supports_H_uncertainty"
    elif rho <= -0.6 and bottom - top >= PEAK_MARGIN:
        shape = "rises_toward_low_probability_supports_H_descending"
    elif rho >= 0.6 and top - bottom >= PEAK_MARGIN:
        shape = "rises_toward_high_probability_neither_hypothesis"
    else:
        shape = "no_clear_shape"

    return {
        "rows": rows,
        "spearman_decile_vs_mean": rho,
        "p_monotone": float(p_monotone),
        "middle_mean": float(middle),
        "extremes_mean": float(extremes),
        "middle_minus_extremes": float(middle - extremes),
        "bottom_two_deciles": float(bottom),
        "top_two_deciles": float(top),
        "shape": shape,
    }


def ranking_divergence(
    gain: np.ndarray, score: np.ndarray, seed: int, draws: int = BOOTSTRAP_DRAWS
) -> dict:
    """Top-slice mean gain versus cohort mean, for one pipeline ordering."""
    rng = np.random.default_rng(seed)
    n = len(gain)
    out = {}
    for fraction in SLICES:
        k = max(1, int(round(fraction * n)))
        differences = []
        for _ in range(draws):
            pick = rng.integers(0, n, n)
            g = gain[pick]
            s = score[pick]
            idx = np.argsort(-s)[:k]
            differences.append(float(np.mean(g[idx]) - np.mean(g)))
        idx = np.argsort(-score)[:k]
        lo, hi = interval(np.array(differences))
        out[f"{fraction:.2f}"] = {
            "n": int(k),
            "slice_mean": float(np.mean(gain[idx])),
            "difference": float(np.mean(gain[idx]) - np.mean(gain)),
            "difference_ci": [lo, hi],
            "diverges": not (lo <= 0.0 <= hi),
        }
    return out


def analyse(args) -> dict:
    config = baseline.load_config(args.config)
    audit_config = {
        "categorical_features": config["base_categorical_features"],
        "numeric_features": config["base_numeric_features"]
        + config["history_numeric_features"],
    }
    data = baseline.load_and_audit(args.input, audit_config)
    target = data[config["target"]].astype(int).to_numpy()
    train = data["split"].eq("train").to_numpy()
    validation = data["split"].eq("validation").to_numpy()
    test = data["split"].eq("test").to_numpy()

    all_columns = (
        config["base_categorical_features"]
        + config["base_numeric_features"]
        + config["history_numeric_features"]
    )
    features = data[all_columns]

    _, base_model, _ = acq.tune_model(
        features, target, train, validation, config, False
    )
    _, full_model, _ = acq.tune_model(
        features, target, train, validation, config, True
    )
    base_probability = base_model.predict_proba(features)[:, 1]
    full_probability = full_model.predict_proba(features)[:, 1]

    y_test = target[test]
    base_p = base_probability[test]
    full_p = full_probability[test]
    test_frame = data.loc[test].reset_index(drop=True)

    rng = np.random.default_rng(config["seed"])

    def column(name: str) -> np.ndarray:
        values = test_frame[name].astype(float).to_numpy()
        return np.nan_to_num(values, nan=float(np.nanmin(values)) - 1.0)

    rankings = {
        "base probability (EXP-007)": base_p,
        "base uncertainty, unsure first": -np.abs(base_p - 0.5),
        "offering size": column("total_offering_amount"),
        "investor count": column("investor_count"),
        "random (control)": rng.random(len(y_test)),
    }

    findings: dict = {
        "n_test": int(len(y_test)),
        "base_rate": float(np.mean(y_test)),
        "declared": {
            "hypotheses": {
                "H_uncertainty": "gain peaks mid-probability; small at both extremes",
                "H_descending": "gain rises as probability falls; largest in bottom decile",
            },
            "deciles": DECILES,
            "peak_margin": PEAK_MARGIN,
            "slices": list(SLICES),
            "note": "both hypotheses and all rankings fixed before running; "
            "EXP-007's monotonicity was consistent with either",
        },
        "utilities": {},
    }

    for utility_name, utility in config["utility_grid"].items():
        gain = acq.gain_target(y_test, base_p, full_p, utility)
        entry = {
            "cohort_mean": float(np.mean(gain)),
            "cohort_sd": float(np.std(gain)),
            "profile": decile_profile(gain, base_p, config["seed"]),
            "rankings": {
                name: ranking_divergence(gain, score, config["seed"])
                for name, score in rankings.items()
            },
        }
        findings["utilities"][utility_name] = entry

    shapes = {
        name: entry["profile"]["shape"]
        for name, entry in findings["utilities"].items()
    }
    control_diverges = sum(
        1
        for entry in findings["utilities"].values()
        for s in entry["rankings"]["random (control)"].values()
        if s["diverges"]
    )
    real_diverges = sum(
        1
        for entry in findings["utilities"].values()
        for name, slices in entry["rankings"].items()
        if name != "random (control)"
        for s in slices.values()
        if s["diverges"]
    )
    findings["summary"] = {
        "shapes": shapes,
        "control_divergences": control_diverges,
        "real_divergences": real_diverges,
        "real_cells": 3 * (len(rankings) - 1) * len(SLICES),
    }
    return findings


def report(findings: dict) -> str:
    lines = [
        "",
        "  EXP-008 — where in the pipeline is information worth buying?",
        "  " + "=" * 76,
        f"  test cases {findings['n_test']}, base rate {findings['base_rate']:.1%}",
        "  declared rivals: H-uncertainty (peak mid-probability) vs "
        "H-descending (rises as p falls)",
        "",
    ]

    for utility_name, entry in findings["utilities"].items():
        profile = entry["profile"]
        lines.append(
            f"  {utility_name}: cohort mean {entry['cohort_mean']:+.4f}"
        )
        lines.append(
            "    decile  n    p range              mean gain             nonzero"
        )
        for row in profile["rows"]:
            lo, hi = row["ci"]
            lines.append(
                f"      {row['decile']:>2}  {row['n']:>4}  "
                f"{row['score_low']:.3f}-{row['score_high']:.3f}   "
                f"{row['mean_gain']:+.4f} [{lo:+.4f},{hi:+.4f}]   "
                f"{row['share_nonzero']:>5.1%}"
            )
        lines.append(
            f"    spearman(decile, mean gain) "
            f"{profile['spearman_decile_vs_mean']:+.3f}  "
            f"p={profile['p_monotone']:.3f}"
        )
        lines.append(
            f"    middle four {profile['middle_mean']:+.4f} vs extremes "
            f"{profile['extremes_mean']:+.4f}  "
            f"gap {profile['middle_minus_extremes']:+.4f}"
        )
        lines.append(
            f"    bottom two deciles {profile['bottom_two_deciles']:+.4f}, "
            f"top two {profile['top_two_deciles']:+.4f}"
        )
        lines.append(f"    shape: {profile['shape']}")
        lines.append("")

    lines.append("  does the top slice diverge from the cohort under every ordering?")
    for utility_name, entry in findings["utilities"].items():
        lines.append(f"    {utility_name}")
        for name, slices in entry["rankings"].items():
            marks = "  ".join(
                f"{k}: {v['difference']:+.4f}"
                + ("*" if v["diverges"] else " ")
                for k, v in slices.items()
            )
            lines.append(f"      {name:<32} {marks}")
        lines.append("")

    summary = findings["summary"]
    lines += [
        "  " + "=" * 76,
        "  * = bootstrap interval on (slice mean - cohort mean) excludes zero",
        f"  divergences: {summary['real_divergences']}/{summary['real_cells']} "
        f"real orderings, {summary['control_divergences']}/9 under the random control",
        "  shapes: "
        + ", ".join(f"{k} -> {v}" for k, v in summary["shapes"].items()),
    ]
    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "datasets" / "processed" / "sec_form_d_v2"
        / "p1_first_anchor_model_ready.csv",
    )
    parser.add_argument(
        "--config", type=Path, default=ROOT / "experiments" / "EXP-001C" / "config.json"
    )
    args = parser.parse_args()

    findings = analyse(args)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(report(findings))


if __name__ == "__main__":
    main()
