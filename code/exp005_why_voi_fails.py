"""EXP-005 — Why does the cost-aware acquisition policy fail its gates?

EXP-001C reported that a learned selective policy passes 0 of 15 declared
utility-by-cost scenarios against the strongest non-VoI baseline. Three
explanations were carried forward without being separated:

    (a) the utility model is misspecified
    (b) the cost regime is one where acquisition genuinely does not pay
    (c) the structural conditions licensing adaptive greedy acquisition fail

**Explanation (c) is void in this design, and that should have been noticed
earlier.** Adaptive submodularity (Golovin & Krause) licenses near-optimality of
adaptive *greedy* selection over a *sequence* of tests. EXP-001C acquires a single
block under a binary decision. With one item there is no sequence, greedy is
trivially optimal given a correct gain estimate, and submodularity has nothing to
say. Carrying (c) as a live hypothesis was a category error.

The correct third candidate is about the *selection signal*:

    (c') either the per-case gain does not vary (nothing to select on), or its
         variation is not predictable from the base state (the selector is noise)

Selective acquisition can only beat all-or-nothing when **both** conditions hold:
gain is heterogeneous, and that heterogeneity is predictable. Those are separately
measurable.

The decisive instrument: an **oracle policy** that acquires iff the *realised*
per-case gain exceeds cost. It is not implementable — it uses the outcome — but it
is the ceiling on any selective policy. It splits the diagnosis cleanly:

* oracle barely beats the best baseline  → no selective policy can win here. The
  failure is in the problem (utility / cost regime), not in the model. Improving
  the gain model is wasted effort.
* oracle beats it clearly, learned policy does not  → the failure is the gain
  model. The problem admits a winning policy; this one cannot find it.

Thresholds declared before running, in the same normalised units as NDV:

    ORACLE_MARGIN   = 0.010   oracle advantage below this ⇒ problem-side failure
    LEARNED_MARGIN  = 0.005   learned advantage above this ⇒ not a failure at all
    SIGNAL_FLOOR    = 0.05    |corr(predicted, realised gain)| below this ⇒ no signal

No cost or utility value is adjusted after seeing any result.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import log_loss

sys.path.insert(0, str(Path(__file__).resolve().parent))

import p1_real_baseline as baseline  # noqa: E402
import p1_sec_history_acquisition as acq  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-005"

ORACLE_MARGIN = 0.010
LEARNED_MARGIN = 0.005
SIGNAL_FLOOR = 0.05


def oracle_actions(realised_gain: np.ndarray, cost: float) -> np.ndarray:
    """Acquire exactly where the realised gain exceeds the cost.

    Uses the outcome, so it is not a policy. It is the least upper bound on what
    any selective policy could achieve at this cost.
    """
    return realised_gain > cost


def gain_heterogeneity(realised_gain: np.ndarray) -> dict:
    """Is there anything to select on at all?

    If every case has the same gain, the optimal policy is all-or-nothing and a
    selective policy cannot beat it by construction — no model would help.
    """
    nonzero = realised_gain != 0
    return {
        "n": int(len(realised_gain)),
        "mean": float(np.mean(realised_gain)),
        "sd": float(np.std(realised_gain)),
        "share_nonzero": float(np.mean(nonzero)),
        "share_positive": float(np.mean(realised_gain > 0)),
        "share_negative": float(np.mean(realised_gain < 0)),
        "max": float(np.max(realised_gain)),
        "min": float(np.min(realised_gain)),
    }


def signal_strength(predicted: np.ndarray, realised: np.ndarray) -> dict:
    """Does the meta-model's predicted gain track the realised gain?"""
    if np.std(predicted) < 1e-12 or np.std(realised) < 1e-12:
        return {"pearson": 0.0, "spearman": 0.0, "degenerate": True}

    pearson = float(np.corrcoef(predicted, realised)[0, 1])

    def ranks(values: np.ndarray) -> np.ndarray:
        order = np.argsort(values)
        out = np.empty(len(values), dtype=float)
        out[order] = np.arange(len(values), dtype=float)
        return out

    spearman = float(np.corrcoef(ranks(predicted), ranks(realised))[0, 1])
    return {"pearson": pearson, "spearman": spearman, "degenerate": False}


def diagnose(args) -> dict:
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

    # Reproduce EXP-001C's models exactly, so the diagnosis describes that
    # experiment rather than a variant of it.
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

    validation_lift = float(
        log_loss(target[validation], base_probability[validation], labels=[0, 1])
        - log_loss(target[validation], full_probability[validation], labels=[0, 1])
    )
    train_uncertainty_gain = acq.entropy(oof_base[train_indices]) - acq.entropy(
        oof_full[train_indices]
    )
    uncertainty_model = acq.fit_gain_model(meta_train, train_uncertainty_gain)
    expected_uncertainty_gain = uncertainty_model.predict(meta_all[test])

    y_test = target[test]
    base_p_test = base_probability[test]
    full_p_test = full_probability[test]

    rng = np.random.default_rng(config["seed"])
    findings: dict = {"utilities": {}}

    for utility_name, utility in config["utility_grid"].items():
        # Realised per-case gain on test: what acquiring is actually worth,
        # before any cost is charged.
        realised_gain = acq.gain_target(y_test, base_p_test, full_p_test, utility)

        train_gain = acq.gain_target(
            target[train_indices], oof_base[train_indices], oof_full[train_indices], utility
        )
        gain_model = acq.fit_gain_model(meta_train, train_gain)
        predicted_gain = gain_model.predict(meta_all[test])

        entry = {
            "heterogeneity": gain_heterogeneity(realised_gain),
            "signal": signal_strength(predicted_gain, realised_gain),
            "predicted_gain_sd": float(np.std(predicted_gain)),
            "costs": {},
        }

        for cost in config["normalized_cost_grid"]:
            values: dict[str, np.ndarray] = {}
            for policy in config["policies"]:
                acquire = acq.policy_actions(
                    policy, predicted_gain, expected_uncertainty_gain,
                    validation_lift, cost, rng,
                )
                vals, _, _ = acq.evaluate_policy(
                    y_test, base_p_test, full_p_test, acquire, utility, cost
                )
                values[policy] = vals

            oracle_acquire = oracle_actions(realised_gain, cost)
            oracle_values, _, _ = acq.evaluate_policy(
                y_test, base_p_test, full_p_test, oracle_acquire, utility, cost
            )
            values["oracle"] = oracle_values

            comparators = [p for p in config["policies"] if p != "cost_aware_voi"]
            strongest = max(comparators, key=lambda name: float(np.mean(values[name])))

            learned_delta = baseline.paired_bootstrap(
                values["cost_aware_voi"], values[strongest],
                config["seed"], config["bootstrap_draws"],
            )
            oracle_delta = baseline.paired_bootstrap(
                values["oracle"], values[strongest],
                config["seed"], config["bootstrap_draws"],
            )

            oracle_advantage = float(np.mean(values["oracle"]) - np.mean(values[strongest]))
            learned_advantage = float(
                np.mean(values["cost_aware_voi"]) - np.mean(values[strongest])
            )

            if oracle_advantage < ORACLE_MARGIN:
                verdict = "problem_side"      # no selective policy can win here
            elif learned_advantage > LEARNED_MARGIN:
                verdict = "policy_wins"       # not a failure at this cell
            else:
                verdict = "model_side"        # a win exists; this model cannot find it

            entry["costs"][str(cost)] = {
                "strongest_non_voi": strongest,
                "mean_ndv": {k: float(np.mean(v)) for k, v in values.items()},
                "oracle_acquisition_rate": float(np.mean(oracle_acquire)),
                "oracle_advantage": oracle_advantage,
                "oracle_delta_ci": oracle_delta,
                "learned_advantage": learned_advantage,
                "learned_delta_ci": learned_delta,
                "verdict": verdict,
            }

        findings["utilities"][utility_name] = entry

    findings["thresholds"] = {
        "oracle_margin": ORACLE_MARGIN,
        "learned_margin": LEARNED_MARGIN,
        "signal_floor": SIGNAL_FLOOR,
        "declared": "before running; no cost or utility adjusted afterwards",
    }
    findings["design_note"] = (
        "Single-block binary acquisition. Adaptive submodularity is vacuous here: it "
        "licenses adaptive greedy over a sequence of tests, and there is no sequence. "
        "Explanation (c) as originally stated is a category error."
    )
    return findings


def report(findings: dict) -> str:
    lines = [
        "",
        "  EXP-005 — why the cost-aware acquisition policy fails",
        "  " + "=" * 72,
        "  oracle = acquires iff realised gain > cost. Not a policy (uses the",
        "  outcome); it is the ceiling on any selective policy.",
        "",
    ]

    verdict_counts: dict[str, int] = {}

    for utility_name, entry in findings["utilities"].items():
        het = entry["heterogeneity"]
        sig = entry["signal"]
        lines += [
            f"  utility: {utility_name}",
            f"    per-case gain: nonzero in {het['share_nonzero']:.1%} of cases "
            f"(+{het['share_positive']:.1%} / -{het['share_negative']:.1%}), "
            f"sd {het['sd']:.4f}, mean {het['mean']:+.4f}",
            f"    gain predictability: pearson {sig['pearson']:+.3f}, "
            f"spearman {sig['spearman']:+.3f}"
            + ("  [NO SIGNAL]" if abs(sig["pearson"]) < SIGNAL_FLOOR else ""),
            f"    predicted-gain sd {entry['predicted_gain_sd']:.4f}",
            "",
            f"    {'cost':>6} {'best baseline':>22} {'oracle adv':>11} "
            f"{'learned adv':>12} {'verdict':>14}",
        ]
        for cost, cell in entry["costs"].items():
            verdict_counts[cell["verdict"]] = verdict_counts.get(cell["verdict"], 0) + 1
            lines.append(
                f"    {cost:>6} {cell['strongest_non_voi']:>22} "
                f"{cell['oracle_advantage']:>+11.4f} "
                f"{cell['learned_advantage']:>+12.4f} {cell['verdict']:>14}"
            )
        lines.append("")

    lines += ["  " + "-" * 72, "  verdict tally across all 15 cells:"]
    for verdict, count in sorted(verdict_counts.items(), key=lambda kv: -kv[1]):
        meaning = {
            "problem_side": "no selective policy can win — utility/cost regime",
            "model_side": "a win exists but the gain model cannot find it",
            "policy_wins": "the learned policy does beat the baseline",
        }[verdict]
        lines.append(f"    {verdict:>14}  {count:>2}/15   {meaning}")

    dominant = max(verdict_counts, key=lambda k: verdict_counts[k]) if verdict_counts else None
    lines += [
        "",
        "  " + "-" * 72,
        f"  dominant diagnosis: {dominant}",
        "",
        "  " + findings["design_note"],
    ]
    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=ROOT / "datasets" / "processed"
                        / "sec_form_d_v2" / "p1_first_anchor_model_ready.csv")
    parser.add_argument("--config", type=Path,
                        default=ROOT / "experiments" / "EXP-001C" / "config.json")
    args = parser.parse_args()

    findings = diagnose(args)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(report(findings))


if __name__ == "__main__":
    main()
