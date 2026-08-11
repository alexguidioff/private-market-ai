"""EXP-009 — A calibrated null for slice estimates, and the objection to change-targeting.

Two jobs, in the order the agenda requires
------------------------------------------
**Part A — the precondition.** EXP-008 overturned EXP-007 by comparing one real
ordering against *one* random ordering. That was enough to show the previous
conclusion was unsafe, and not enough to establish a threshold. Here a few hundred
random orderings are drawn so that any future slice-restricted claim can be checked
against a calibrated null instead of a single comparison point. The agenda records
this as the thing to do before building anything else on slice estimates.

**Part B — test the objection before the hypothesis.** EXP-008 closed with a
hypothesis: gain concentrates where the base and acquired models disagree, and
disagreement needs the block but not the outcome, so predicting *whether the action
changes* might reopen targeting without reopening the per-case gain model EXP-005
closed. The objection stated alongside it was that knowing the action changes says
nothing about the *direction* of the change, and direction is exactly what EXP-005
found unpredictable.

The objection is testable directly and cheaply, so it goes first. Decompose

    E[gain] = P(action changes) x E[gain | action changes]

If the second term is near zero, or flips sign across utilities in a way that cannot
be estimated in advance, then P(change) is useless as a targeting signal however well
it is predicted, and the hypothesis dies without any modelling. If instead the second
term is stably signed under a given utility, then P(change) *is* a sufficient
targeting signal, and it is a genuinely easier quantity to predict than per-case
gain: it does not require knowing whether the change helps.

Discipline carried over from the falsification clause
-----------------------------------------------------
P1's clause forbids substituting a prediction metric for a decision metric. So a
good AUC on the change indicator settles nothing on its own. The final test is
Net Decision Value against the strongest non-VoI baseline, with the same
paired-bootstrap machinery and the same declared margin EXP-005 used.

    N_NULL          = 400   random orderings for the calibrated null
    CHANGE_MARGIN   = 0.005 learned-policy margin, identical to EXP-005's
    SIGNAL_FLOOR    = 0.05  AUC above 0.55 for the change model to count as
                            predictable at all
    DECISION_FLOOR  = 0.55  same thing, stated as an AUC

Declared before running, so the outcome cannot be reinterpreted afterwards:

* I expect E[gain | change] to be **positive under `balanced`** (EXP-005 reported
  13.1% helped against 7.3% hurt, so roughly 64% of changes help) and **negative
  under `false_positive_averse`** (5.6% against 7.8%, roughly 42%). That is a sign
  flip with the payoff matrix, which does *not* kill the hypothesis, because the
  utility is chosen by the investor and known before acquiring. It would kill it only
  if the sign were unstable *within* a utility.
* I expect the change indicator to be **more predictable than per-case gain**, since
  it discards the direction. Whether it is predictable *enough* to win on NDV is the
  open question and I do not have a prediction.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parent))

import p1_real_baseline as baseline  # noqa: E402
import p1_sec_history_acquisition as acq  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-009"

N_NULL = 400
CHANGE_MARGIN = 0.005
DECISION_FLOOR = 0.55
SLICES = (0.05, 0.10, 0.20)


# --------------------------------------------------------------------------
# Part A — calibrated null for slice-restricted estimates
# --------------------------------------------------------------------------

def calibrated_null(gain: np.ndarray, seed: int, n_null: int = N_NULL) -> dict:
    """Distribution of top-slice divergence under random orderings.

    Each draw is an independent arbitrary ordering of the same cases, so the spread
    describes how far a slice mean strays from the cohort mean for no reason at all.
    Any real ordering has to clear this to mean anything.
    """
    rng = np.random.default_rng(seed)
    n = len(gain)
    cohort_mean = float(np.mean(gain))

    out = {}
    for fraction in SLICES:
        k = max(1, int(round(fraction * n)))
        divergences = np.empty(n_null)
        for draw in range(n_null):
            order = rng.permutation(n)[:k]
            divergences[draw] = float(np.mean(gain[order]) - cohort_mean)
        magnitudes = np.sort(np.abs(divergences))
        out[f"{fraction:.2f}"] = {
            "n_slice": int(k),
            "n_null": int(n_null),
            "null_sd": float(np.std(divergences)),
            "null_abs_median": float(magnitudes[len(magnitudes) // 2]),
            "null_abs_p95": float(magnitudes[int(0.95 * len(magnitudes))]),
            "null_abs_max": float(magnitudes[-1]),
        }
    return out


def check_against_null(
    gain: np.ndarray, score: np.ndarray, null: dict
) -> dict:
    """Does an ordering's slice divergence clear the calibrated null?"""
    n = len(gain)
    cohort_mean = float(np.mean(gain))
    out = {}
    for fraction in SLICES:
        key = f"{fraction:.2f}"
        k = max(1, int(round(fraction * n)))
        idx = np.argsort(-score)[:k]
        divergence = float(np.mean(gain[idx]) - cohort_mean)
        threshold = null[key]["null_abs_p95"]
        out[key] = {
            "divergence": divergence,
            "null_p95": threshold,
            "clears_null": bool(abs(divergence) > threshold),
        }
    return out


# --------------------------------------------------------------------------
# Part B — the objection, then the hypothesis
# --------------------------------------------------------------------------

def decompose(
    y: np.ndarray,
    base_probability: np.ndarray,
    full_probability: np.ndarray,
    utility: dict,
) -> dict:
    """Split expected gain into how often the action changes and what a change is worth.

    This is the objection test. If a change is worth nothing on average, no amount of
    predicting changes helps.
    """
    base_action = baseline.optimal_decision(base_probability, utility)
    full_action = baseline.optimal_decision(full_probability, utility)
    changed = base_action != full_action
    gain = acq.gain_target(y, base_probability, full_probability, utility)

    share = float(np.mean(changed))
    if changed.sum() < 5:
        return {
            "share_changed": share,
            "n_changed": int(changed.sum()),
            "insufficient": True,
        }

    changed_gain = gain[changed]
    rng = np.random.default_rng(20260729)
    draws = np.array(
        [
            np.mean(changed_gain[rng.integers(0, len(changed_gain), len(changed_gain))])
            for _ in range(2000)
        ]
    )
    ordered = np.sort(draws)
    return {
        "share_changed": share,
        "n_changed": int(changed.sum()),
        "mean_gain_given_change": float(np.mean(changed_gain)),
        "ci": [
            float(ordered[int(0.025 * len(ordered))]),
            float(ordered[int(0.975 * len(ordered))]),
        ],
        "share_helped_given_change": float(np.mean(changed_gain > 0)),
        "sd_gain_given_change": float(np.std(changed_gain)),
        "product_check": float(share * np.mean(changed_gain)),
        "cohort_mean_gain": float(np.mean(gain)),
        "insufficient": False,
    }


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
    train_indices = np.flatnonzero(train)

    all_columns = (
        config["base_categorical_features"]
        + config["base_numeric_features"]
        + config["history_numeric_features"]
    )
    features = data[all_columns]

    base_c, base_model, _ = acq.tune_model(
        features, target, train, validation, config, False
    )
    full_c, full_model, _ = acq.tune_model(
        features, target, train, validation, config, True
    )
    base_probability = base_model.predict_proba(features)[:, 1]
    full_probability = full_model.predict_proba(features)[:, 1]
    oof_base = acq.cross_fitted_probabilities(
        features, target, train_indices, config, False, base_c
    )
    oof_full = acq.cross_fitted_probabilities(
        features, target, train_indices, config, True, full_c
    )

    base_columns = [c for c in config["base_numeric_features"] if c in data]
    meta_all = acq.meta_features(data, base_probability, base_columns)
    meta_train = acq.meta_features(
        data.loc[train].reset_index(drop=True), oof_base[train_indices], base_columns
    )

    y_test = target[test]
    base_p = base_probability[test]
    full_p = full_probability[test]
    test_frame = data.loc[test].reset_index(drop=True)

    rng = np.random.default_rng(config["seed"])
    findings: dict = {
        "n_test": int(len(y_test)),
        "declared": {
            "n_null": N_NULL,
            "change_margin": CHANGE_MARGIN,
            "decision_floor": DECISION_FLOOR,
            "expectation": "E[gain|change] positive under balanced, negative under "
            "false_positive_averse; change indicator more predictable than per-case "
            "gain; no prediction on whether it wins on NDV",
            "discipline": "NDV against the strongest non-VoI baseline decides; a good "
            "AUC on the change indicator settles nothing on its own",
        },
        "utilities": {},
    }

    def column(name: str) -> np.ndarray:
        values = test_frame[name].astype(float).to_numpy()
        return np.nan_to_num(values, nan=float(np.nanmin(values)) - 1.0)

    real_orderings = {
        "base probability": base_p,
        "offering size": column("total_offering_amount"),
        "investor count": column("investor_count"),
    }

    validation_lift = float(
        np.mean(
            acq.entropy(base_probability[validation]) - acq.entropy(full_probability[validation])
        )
    )

    for utility_name, utility in config["utility_grid"].items():
        gain = acq.gain_target(y_test, base_p, full_p, utility)

        # Part A
        null = calibrated_null(gain, config["seed"])
        against = {
            name: check_against_null(gain, score, null)
            for name, score in real_orderings.items()
        }

        # Part B, objection first
        objection = decompose(y_test, base_p, full_p, utility)

        # Part B, hypothesis: predict the change indicator from base state only
        train_base_action = baseline.optimal_decision(oof_base[train_indices], utility)
        train_full_action = baseline.optimal_decision(oof_full[train_indices], utility)
        train_changed = (train_base_action != train_full_action).astype(float)

        test_base_action = baseline.optimal_decision(base_p, utility)
        test_full_action = baseline.optimal_decision(full_p, utility)
        test_changed = (test_base_action != test_full_action).astype(int)

        entry: dict = {
            "calibrated_null": null,
            "real_orderings": against,
            "objection": objection,
            "change_model": None,
            "policy": None,
        }

        if 0 < train_changed.sum() < len(train_changed) and 0 < test_changed.sum():
            change_model = acq.fit_gain_model(meta_train, train_changed)
            predicted_change = change_model.predict(meta_all[test])
            auc = (
                float(roc_auc_score(test_changed, predicted_change))
                if 0 < test_changed.sum() < len(test_changed)
                else None
            )

            # Population value of a change, estimated on train only.
            train_gain = acq.gain_target(
                target[train_indices], oof_base[train_indices], oof_full[train_indices],
                utility,
            )
            changed_mask = train_changed.astype(bool)
            value_of_change = (
                float(np.mean(train_gain[changed_mask])) if changed_mask.any() else 0.0
            )
            expected_gain = predicted_change * value_of_change

            entry["change_model"] = {
                "auc": float(auc) if auc is not None else None,
                "train_share_changed": float(np.mean(train_changed)),
                "test_share_changed": float(np.mean(test_changed)),
                "value_of_change_from_train": value_of_change,
                "predictable": bool(auc is not None and auc >= DECISION_FLOOR),
            }

            costs = {}
            for cost in config["normalized_cost_grid"]:
                values: dict[str, np.ndarray] = {}
                for policy in config["policies"]:
                    if policy == "cost_aware_voi":
                        continue
                    acquire = acq.policy_actions(
                        policy, np.zeros(len(y_test)), np.zeros(len(y_test)),
                        validation_lift, cost, rng,
                    )
                    vals, _, _ = acq.evaluate_policy(
                        y_test, base_p, full_p, acquire, utility, cost
                    )
                    values[policy] = vals

                change_acquire = expected_gain > cost
                change_values, _, _ = acq.evaluate_policy(
                    y_test, base_p, full_p, change_acquire, utility, cost
                )
                values["change_targeting"] = change_values

                comparators = [k for k in values if k != "change_targeting"]
                strongest = max(comparators, key=lambda k: float(np.mean(values[k])))
                advantage = float(
                    np.mean(values["change_targeting"]) - np.mean(values[strongest])
                )
                delta = baseline.paired_bootstrap(
                    values["change_targeting"], values[strongest],
                    config["seed"], config["bootstrap_draws"],
                )
                costs[str(cost)] = {
                    "strongest_non_voi": strongest,
                    "acquisition_rate": float(np.mean(change_acquire)),
                    "advantage": advantage,
                    "delta_ci": delta["ci_95"],
                    "wins": bool(
                        advantage > CHANGE_MARGIN and delta["ci_95"][0] > 0.0
                    ),
                }
            entry["policy"] = costs

        findings["utilities"][utility_name] = entry

    wins = sum(
        1
        for u in findings["utilities"].values()
        if u["policy"]
        for c in u["policy"].values()
        if c["wins"]
    )
    cells = sum(1 for u in findings["utilities"].values() if u["policy"]) * len(
        config["normalized_cost_grid"]
    )
    clears = sum(
        1
        for u in findings["utilities"].values()
        for o in u["real_orderings"].values()
        for s in o.values()
        if s["clears_null"]
    )
    total_slices = sum(
        len(o) for u in findings["utilities"].values() for o in u["real_orderings"].values()
    )
    findings["summary"] = {
        "policy_wins": wins,
        "policy_cells": cells,
        "orderings_clearing_null": clears,
        "ordering_slices_tested": total_slices,
    }
    return findings


def report(findings: dict) -> str:
    lines = [
        "",
        "  EXP-009 — calibrated null for slices, and change-targeting",
        "  " + "=" * 76,
        f"  test cases {findings['n_test']}, "
        f"{findings['declared']['n_null']} random orderings per utility",
        "",
        "  PART A — how far does a slice mean stray for no reason?",
    ]
    for utility_name, entry in findings["utilities"].items():
        lines.append(f"    {utility_name}")
        for fraction, null in entry["calibrated_null"].items():
            lines.append(
                f"      top {fraction}  n={null['n_slice']:<5} "
                f"null sd {null['null_sd']:.4f}  "
                f"|divergence| median {null['null_abs_median']:.4f}  "
                f"p95 {null['null_abs_p95']:.4f}  max {null['null_abs_max']:.4f}"
            )
        for name, slices in entry["real_orderings"].items():
            marks = "  ".join(
                f"{k}: {v['divergence']:+.4f}" + ("*" if v["clears_null"] else " ")
                for k, v in slices.items()
            )
            lines.append(f"      {name:<20} {marks}")
        lines.append("")

    lines.append("  PART B — the objection: is a decision change worth anything?")
    for utility_name, entry in findings["utilities"].items():
        objection = entry["objection"]
        if objection.get("insufficient"):
            lines.append(f"    {utility_name}: too few changes to measure")
            continue
        lo, hi = objection["ci"]
        lines.append(
            f"    {utility_name}: action changes on "
            f"{objection['share_changed']:.1%} of cases (n={objection['n_changed']})"
        )
        lines.append(
            f"      E[gain | change] {objection['mean_gain_given_change']:+.4f} "
            f"[{lo:+.4f}, {hi:+.4f}]   "
            f"helped {objection['share_helped_given_change']:.1%} of changes"
        )
        lines.append(
            f"      product check {objection['product_check']:+.4f} vs "
            f"cohort mean {objection['cohort_mean_gain']:+.4f}"
        )
    lines.append("")

    lines.append("  PART B — the hypothesis: predict the change, then act on it")
    for utility_name, entry in findings["utilities"].items():
        model = entry["change_model"]
        if not model:
            lines.append(f"    {utility_name}: not estimable")
            continue
        auc = model["auc"]
        auc_text = f"{auc:.3f}" if auc is not None else "n/a"
        lines.append(f"    {utility_name}: change-indicator AUC {auc_text}")
        lines.append(
            f"      train share changed {model['train_share_changed']:.1%}, "
            f"test {model['test_share_changed']:.1%}, "
            f"value of a change (train) {model['value_of_change_from_train']:+.4f}"
        )
        if entry["policy"]:
            for cost, cell in entry["policy"].items():
                lo, hi = cell["delta_ci"][0], cell["delta_ci"][1]
                flag = " WIN" if cell["wins"] else ""
                lines.append(
                    f"        cost {cost:<5} acquires "
                    f"{cell['acquisition_rate']:.1%}  vs {cell['strongest_non_voi']:<6} "
                    f"{cell['advantage']:+.4f} [{lo:+.4f}, {hi:+.4f}]{flag}"
                )
        lines.append("")

    summary = findings["summary"]
    lines += [
        "  " + "=" * 76,
        f"  orderings clearing the calibrated null: "
        f"{summary['orderings_clearing_null']}/{summary['ordering_slices_tested']}",
        f"  change-targeting wins on NDV: "
        f"{summary['policy_wins']}/{summary['policy_cells']} cells",
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
