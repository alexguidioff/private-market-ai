"""EXP-007 — Does the population-level acquisition estimate survive inside the top slice?

The compounding caution logged under P5, made measurable
--------------------------------------------------------
Two earlier results point in opposite directions and the agenda records that they
compound rather than cancel.

EXP-005 established that per-case value of information is not selectable in this
regime: gain is heterogeneous (nonzero on 20.4% of cases under `balanced`) but
unpredictable from the base state (Pearson +0.015). What *is* estimable is the
population mean gain, and it changes sign with the utility (+0.028 balanced,
-0.008 false-positive-averse). P5 was promoted on exactly that basis: a budgeted
pipeline needs the population trade-off, not the per-case one.

EXP-002 established that average and tail behaviour diverge materially on this same
cohort: SEC issuer history gives ROC-AUC 0.61 while concentrating 1.45x enrichment
in the top 5%. A budgeted fund only ever works the top slice of its pipeline.

Put together, the P5 formulation rests on a quantity measured over the whole cohort
while the decision it informs is taken inside a small slice of it. If the mean gain
inside the slice differs from the cohort mean — in magnitude or, worse, in sign —
then the estimate P5 was promoted on does not reach the decision it was promoted
for. This experiment measures whether it does.

What is and is not being asked
------------------------------
This is not another attempt at selective acquisition. EXP-005 closed that, and the
agenda records that work on the per-case gain model has stopped. Here every case
inside the slice gets the same decision; the only question is whether the number
used to make that one decision is stable when computed on the slice a budget
actually reaches.

Ranking the pipeline. A fund with limited attention works its most promising deals
first, and with no extra information the ranking available at the decision time is
the base model's own score. That ranking is used here. It is a modelling choice and
an alternative is reported alongside: ranking by the acquired model's score would
require the block first and so cannot define who to buy it for.

Thresholds and rules, declared before running
---------------------------------------------
    SLICES           = 0.05, 0.10, 0.20, 0.50, 1.00
    SIGN_STABILITY   the slice mean must share the cohort mean's sign
    TRANSFER_MARGIN  = 0.010  in normalised NDV units, the same margin EXP-005 used
    MIN_SLICE_N      = 30     below this the slice estimate is reported as void
                              rather than negative, because a mean on fewer cases
                              cannot distinguish drift from noise

Verdict rule: the cohort estimate transfers if, for every slice with at least
MIN_SLICE_N cases, the slice mean shares the cohort sign *and* the bootstrap
interval on (slice mean - cohort mean) contains zero. Any slice failing either
condition means P5 must estimate inside the slice.

Declared expectation, so it can be wrong on the record: the top slice of a
probability ranking is where the base model is already confident, and gain is
nonzero only where acquiring changes the action. Confident cases are the hardest to
move, so the slice mean is expected to be *smaller* in magnitude than the cohort
mean, possibly to the point of changing sign under a utility whose cohort mean is
already near zero.
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
OUT = ROOT / "experiments" / "EXP-007"

SLICES = (0.05, 0.10, 0.20, 0.50, 1.00)
TRANSFER_MARGIN = 0.010
MIN_SLICE_N = 30
BOOTSTRAP_DRAWS = 4000


def slice_indices(score: np.ndarray, fraction: float) -> np.ndarray:
    """Indices of the top `fraction` of cases by score, descending."""
    k = max(1, int(round(fraction * len(score))))
    return np.argsort(-score)[:k]


def bootstrap_slice_vs_cohort(
    gain: np.ndarray,
    score: np.ndarray,
    fraction: float,
    seed: int,
    draws: int = BOOTSTRAP_DRAWS,
) -> dict:
    """Interval on the slice mean and on (slice mean - cohort mean).

    Both quantities are recomputed inside each resample, including the ranking, so
    the interval accounts for the fact that slice membership is itself estimated
    rather than given. Resampling the cases and then reusing a fixed slice would
    understate the uncertainty exactly where the slice is smallest.
    """
    rng = np.random.default_rng(seed)
    n = len(gain)

    slice_means: list[float] = []
    differences: list[float] = []
    for _ in range(draws):
        draw = rng.integers(0, n, n)
        g = gain[draw]
        s = score[draw]
        idx = slice_indices(s, fraction)
        if len(idx) < 2:
            continue
        slice_mean = float(np.mean(g[idx]))
        slice_means.append(slice_mean)
        differences.append(slice_mean - float(np.mean(g)))

    def interval(values: list[float]) -> tuple[float, float]:
        if not values:
            return (float("nan"), float("nan"))
        ordered = np.sort(np.asarray(values))
        return (
            float(ordered[int(0.025 * len(ordered))]),
            float(ordered[min(len(ordered) - 1, int(0.975 * len(ordered)))]),
        )

    idx = slice_indices(score, fraction)
    return {
        "fraction": fraction,
        "n": int(len(idx)),
        "slice_mean": float(np.mean(gain[idx])),
        "slice_mean_ci": interval(slice_means),
        "difference": float(np.mean(gain[idx]) - np.mean(gain)),
        "difference_ci": interval(differences),
        "share_nonzero": float(np.mean(gain[idx] != 0)),
        "share_positive": float(np.mean(gain[idx] > 0)),
        "share_negative": float(np.mean(gain[idx] < 0)),
    }


def classify(entry: dict, cohort_mean: float) -> str:
    """Does this slice's estimate agree with the cohort's?"""
    if entry["n"] < MIN_SLICE_N:
        return "void_too_few"
    lo, hi = entry["difference_ci"]
    same_sign = np.sign(entry["slice_mean"]) == np.sign(cohort_mean) or cohort_mean == 0
    contains_zero = lo <= 0.0 <= hi
    if not same_sign:
        return "sign_flip"
    if not contains_zero and abs(entry["difference"]) >= TRANSFER_MARGIN:
        return "magnitude_shift"
    return "transfers"


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

    # Same two models as EXP-001C and EXP-005, so this describes those experiments
    # rather than a variant.
    _, base_model, _ = acq.tune_model(
        features, target, train, validation, config, False
    )
    _, full_model, _ = acq.tune_model(
        features, target, train, validation, config, True
    )
    base_probability = base_model.predict_proba(features)[:, 1]
    full_probability = full_model.predict_proba(features)[:, 1]

    y_test = target[test]
    base_p_test = base_probability[test]
    full_p_test = full_probability[test]

    findings: dict = {
        "n_test": int(len(y_test)),
        "base_rate": float(np.mean(y_test)),
        "ranking": "base model predicted probability, descending",
        "thresholds": {
            "slices": list(SLICES),
            "transfer_margin": TRANSFER_MARGIN,
            "min_slice_n": MIN_SLICE_N,
            "declared": "before running; no slice or margin adjusted afterwards",
        },
        "utilities": {},
    }

    for utility_name, utility in config["utility_grid"].items():
        realised_gain = acq.gain_target(y_test, base_p_test, full_p_test, utility)
        cohort_mean = float(np.mean(realised_gain))

        entry = {
            "cohort_mean": cohort_mean,
            "cohort_sd": float(np.std(realised_gain)),
            "slices": [],
            "cost_decisions": {},
        }

        for fraction in SLICES:
            result = bootstrap_slice_vs_cohort(
                realised_gain, base_p_test, fraction, config["seed"]
            )
            result["verdict"] = classify(result, cohort_mean)
            entry["slices"].append(result)

        # The decision-relevant form: at each declared cost, does the all-or-nothing
        # answer computed on the cohort match the one computed inside the slice?
        for cost in config["normalized_cost_grid"]:
            cohort_acquire = cohort_mean > cost
            per_slice = {}
            for result in entry["slices"]:
                if result["n"] < MIN_SLICE_N:
                    per_slice[f"{result['fraction']:.2f}"] = "void"
                    continue
                slice_acquire = result["slice_mean"] > cost
                per_slice[f"{result['fraction']:.2f}"] = (
                    "agrees" if slice_acquire == cohort_acquire else "DISAGREES"
                )
            entry["cost_decisions"][str(cost)] = {
                "cohort_decision": "acquire" if cohort_acquire else "do_not_acquire",
                "slices": per_slice,
            }

        findings["utilities"][utility_name] = entry

    verdicts = [
        s["verdict"]
        for u in findings["utilities"].values()
        for s in u["slices"]
        if s["verdict"] != "void_too_few"
    ]
    disagreements = sum(
        1
        for u in findings["utilities"].values()
        for c in u["cost_decisions"].values()
        for v in c["slices"].values()
        if v == "DISAGREES"
    )
    findings["summary"] = {
        "slices_evaluated": len(verdicts),
        "transfers": sum(1 for v in verdicts if v == "transfers"),
        "sign_flips": sum(1 for v in verdicts if v == "sign_flip"),
        "magnitude_shifts": sum(1 for v in verdicts if v == "magnitude_shift"),
        "voided_for_size": sum(
            1
            for u in findings["utilities"].values()
            for s in u["slices"]
            if s["verdict"] == "void_too_few"
        ),
        "cost_decision_disagreements": disagreements,
    }
    return findings


def report(findings: dict) -> str:
    lines = [
        "",
        "  EXP-007 — does the cohort-level acquisition estimate reach the top slice?",
        "  " + "=" * 76,
        f"  test cases {findings['n_test']}, base rate {findings['base_rate']:.1%}",
        f"  pipeline ranking: {findings['ranking']}",
        f"  declared: slices {findings['thresholds']['slices']}, "
        f"transfer margin {findings['thresholds']['transfer_margin']}, "
        f"minimum slice n {findings['thresholds']['min_slice_n']}",
        "",
    ]

    for utility_name, entry in findings["utilities"].items():
        lines.append(
            f"  {utility_name}: cohort mean gain {entry['cohort_mean']:+.4f} "
            f"(sd {entry['cohort_sd']:.4f})"
        )
        lines.append(
            "    slice     n    mean gain            vs cohort            verdict"
        )
        for s in entry["slices"]:
            lo, hi = s["slice_mean_ci"]
            dlo, dhi = s["difference_ci"]
            lines.append(
                f"    {s['fraction']:>5.0%} {s['n']:>5}  "
                f"{s['slice_mean']:+.4f} [{lo:+.4f},{hi:+.4f}]  "
                f"{s['difference']:+.4f} [{dlo:+.4f},{dhi:+.4f}]  "
                f"{s['verdict']}"
            )
        lines.append("")

    lines.append("  all-or-nothing decision, cohort estimate vs slice estimate:")
    for utility_name, entry in findings["utilities"].items():
        for cost, decision in entry["cost_decisions"].items():
            marks = " ".join(
                f"{k}:{v}" for k, v in decision["slices"].items()
            )
            lines.append(
                f"    {utility_name:<24} cost {cost:<5} "
                f"cohort says {decision['cohort_decision']:<16} {marks}"
            )
    lines.append("")

    summary = findings["summary"]
    lines += [
        "  " + "=" * 76,
        f"  slices evaluated {summary['slices_evaluated']}, "
        f"transfers {summary['transfers']}, "
        f"sign flips {summary['sign_flips']}, "
        f"magnitude shifts {summary['magnitude_shifts']}, "
        f"voided for size {summary['voided_for_size']}",
        f"  all-or-nothing decision disagreements: "
        f"{summary['cost_decision_disagreements']}",
    ]

    if summary["sign_flips"] or summary["magnitude_shifts"]:
        lines += [
            "",
            "  The cohort estimate does not reach the slice a budget works. P5 cannot",
            "  inherit EXP-005's population mean and must estimate inside the top-k,",
            "  which is where the sample is smallest — the compounding caution is real",
            "  and now quantified rather than anticipated.",
        ]
    elif summary["transfers"] and not summary["sign_flips"]:
        lines += [
            "",
            "  The cohort estimate survives restriction to the slice. P5 may use the",
            "  population-level trade-off, and the compounding caution logged in the",
            "  agenda is resolved in P5's favour on this cohort and this block.",
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
