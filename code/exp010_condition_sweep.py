"""EXP-010 — Does the §8.6 condition hold as a mechanism, or only on our cohort?

What this test is for
---------------------
EXP-009 produced P1's central claim: selective value of information requires the
*direction* of a decision change to be predictable, not merely its *incidence*.
That claim rests on one information block, one cohort and one weak outcome proxy,
and a second real block is blocked on four independent source gates. So the largest
threat to the paper's contribution cannot currently be addressed with real data.

It can be addressed with a mechanism test. In synthetic worlds the hidden truth is
ours to set, so the two quantities the condition is about can be varied
independently and the boundary between them mapped.

The tension the condition implies, stated as a hypothesis
--------------------------------------------------------
Predicting the direction of a decision change requires anticipating what the
acquired block will say. But if the base state already anticipates the block, the
block adds little, so there is little to win. The condition therefore implies
something stronger than "selection failed on our data":

    There is no region in which the direction of a change is predictable AND the
    prize for acquiring is large. Predictability and prize trade off against each
    other by construction.

Two knobs are swept because the condition names both.

* ``lam`` scales how strongly base features predict the acquirable signal. High
  ``lam`` means the base state anticipates the block, so direction should become
  predictable and the prize should shrink.
* ``base_strength`` scales how much the base features explain the outcome. §8.6's
  structural argument is that per-case gain is the base model's residual, so the
  condition should bind hardest where base accuracy is modest and the prize should
  shrink where it is high.

The falsification gate, declared before running
-----------------------------------------------
This experiment can refute the paper's central claim, which is why it is worth
running rather than a confirmation exercise.

    §8.6 is REFUTED at a grid cell if the learned selective policy beats the
    strongest non-VoI baseline by more than REFUTE_MARGIN with a paired bootstrap
    interval over worlds excluding zero, while corr(predicted, realised gain)
    exceeds SIGNAL_FLOOR.

    REFUTE_MARGIN = 0.010   same units and value as EXP-005's oracle margin
    SIGNAL_FLOOR  = 0.05    same as EXP-005's declared signal floor

If any cell refutes, the condition is wrong as stated and §8.6 must be narrowed or
withdrawn. A single refuting cell is sufficient: the claim is universal in form.

Declared expectations, so a correct prediction can be told from a fitted story
-----------------------------------------------------------------------------
* corr(predicted, realised gain) rises monotonically with ``lam``.
* The prize — share of cases where acquiring changes the decision, and mean
  realised gain — falls with ``lam``, and also falls as ``base_strength`` rises.
* The learned advantage stays below the margin everywhere, being small at low
  ``lam`` because the selector is blind and small at high ``lam`` because there is
  nothing to select for.
* I do not predict the shape in between. If a middle region shows both a usable
  correlation and a real prize, the condition is refuted and that is the result.

Honest limits, before any number is produced
--------------------------------------------
This is a synthetic mechanism test with a correctly specified model class: the
generator is logistic and so is the learner. Real data offers no such guarantee, so
a pass here supports the condition's internal logic and does **not** establish that
it holds for a qualitatively different real block. It is evidence about the
mechanism, not a substitute for the second block.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-010"

# Utility matrix reproduced from EXP-001A so the units are comparable.
TP, FP, FN, TN = 1.0, -0.45, -0.85, 0.0

N_BASE = 3
TRAIN_YEARS = (2016, 2017, 2018)
VALIDATION_YEAR, TEST_YEAR = 2019, 2020

LAM_GRID = (0.0, 0.5, 1.0, 1.5, 2.5)
BASE_STRENGTH_GRID = (0.3, 0.65, 1.2)
COST_GRID = (0.0, 0.02)

WORLDS_PER_CELL = 40
N_PER_YEAR = 300
FOLDS = 3

REFUTE_MARGIN = 0.010
SIGNAL_FLOOR = 0.05
BOOTSTRAP_DRAWS = 2000
SEED = 20260729


def sigmoid(value):
    return 1.0 / (1.0 + np.exp(-np.clip(value, -30.0, 30.0)))


def optimal_action(probability):
    """Utility-maximising binary action under the declared payoff matrix."""
    act = probability * TP + (1.0 - probability) * FP
    stop = probability * FN + (1.0 - probability) * TN
    return act >= stop


def realised_utility(y, action):
    return np.where(
        action,
        np.where(y == 1, TP, FP),
        np.where(y == 1, FN, TN),
    )


def entropy(probability):
    p = np.clip(probability, 1e-9, 1 - 1e-9)
    return -(p * np.log(p) + (1 - p) * np.log(1 - p))


# --------------------------------------------------------------------------
# world generation: the hidden truth is set here and nowhere else
# --------------------------------------------------------------------------

def make_world(rng, lam: float, base_strength: float) -> dict:
    return {
        "intercept": float(rng.uniform(-1.2, -0.6)),
        "base_beta": rng.normal(0.0, base_strength, N_BASE),
        "signal_beta": float(rng.choice((-1.0, 1.0)) * rng.uniform(1.0, 1.8)),
        "signal_intercept": float(rng.normal(0.0, 0.5)),
        # The swept knob: how much the base state anticipates the acquirable block.
        "signal_base_beta": rng.normal(0.0, lam, N_BASE),
    }


def generate(world: dict, rng):
    years = np.repeat(np.arange(2016, 2021), N_PER_YEAR)
    base = rng.normal(0.0, 1.0, (len(years), N_BASE))
    signal_probability = sigmoid(
        world["signal_intercept"] + base @ world["signal_base_beta"]
    )
    signal = rng.binomial(1, signal_probability)
    outcome_probability = sigmoid(
        world["intercept"] + base @ world["base_beta"] + signal * world["signal_beta"]
    )
    outcome = rng.binomial(1, outcome_probability)
    return years, base, signal.astype(float), outcome


# --------------------------------------------------------------------------
# one world
# --------------------------------------------------------------------------

def evaluate_world(world: dict, rng) -> dict | None:
    years, base, signal, y = generate(world, rng)
    train = np.isin(years, TRAIN_YEARS)
    test = years == TEST_YEAR

    if len(np.unique(y[train])) < 2 or len(np.unique(y[test])) < 2:
        return None

    full_features = np.column_stack((base, signal))

    def fit(x, target):
        return LogisticRegression(C=1.0, max_iter=1000, solver="lbfgs").fit(x, target)

    base_model = fit(base[train], y[train])
    full_model = fit(full_features[train], y[train])

    p_base = base_model.predict_proba(base)[:, 1]
    p_full = full_model.predict_proba(full_features)[:, 1]

    # Cross-fitted probabilities on train, so the gain model is not fitted to its
    # own in-sample predictions.
    oof_base = np.zeros(len(y))
    oof_full = np.zeros(len(y))
    train_idx = np.flatnonzero(train)
    rng.shuffle(train_idx)
    for fold in np.array_split(train_idx, FOLDS):
        rest = np.setdiff1d(train_idx, fold)
        if len(np.unique(y[rest])) < 2:
            return None
        oof_base[fold] = fit(base[rest], y[rest]).predict_proba(base[fold])[:, 1]
        oof_full[fold] = fit(full_features[rest], y[rest]).predict_proba(
            full_features[fold]
        )[:, 1]

    def gain_of(y_slice, pb, pf):
        return realised_utility(y_slice, optimal_action(pf)) - realised_utility(
            y_slice, optimal_action(pb)
        )

    train_gain = gain_of(y[train_idx], oof_base[train_idx], oof_full[train_idx])
    test_gain = gain_of(y[test], p_base[test], p_full[test])

    def meta(x, probability):
        return np.column_stack((x, probability, entropy(probability)))

    gain_model = Ridge(alpha=1.0).fit(
        meta(base[train_idx], oof_base[train_idx]), train_gain
    )
    predicted_gain = gain_model.predict(meta(base[test], p_base[test]))

    correlation = 0.0
    if np.std(predicted_gain) > 1e-12 and np.std(test_gain) > 1e-12:
        correlation = float(np.corrcoef(predicted_gain, test_gain)[0, 1])

    y_test = y[test]
    result = {
        "base_auc": float(roc_auc_score(y_test, p_base[test])),
        "full_auc": float(roc_auc_score(y_test, p_full[test])),
        "share_changed": float(np.mean(test_gain != 0)),
        "mean_gain": float(np.mean(test_gain)),
        "correlation": correlation,
        "costs": {},
    }

    random_draw = rng.random(len(y_test)) < 0.5
    for cost in COST_GRID:
        def ndv(acquire):
            probability = np.where(acquire, p_full[test], p_base[test])
            return realised_utility(y_test, optimal_action(probability)) - cost * acquire

        baselines = {
            "none": ndv(np.zeros(len(y_test), dtype=bool)),
            "always": ndv(np.ones(len(y_test), dtype=bool)),
            "random": ndv(random_draw),
        }
        learned = ndv(predicted_gain > cost)
        oracle = ndv(test_gain > cost)

        strongest = max(baselines, key=lambda k: float(np.mean(baselines[k])))
        result["costs"][str(cost)] = {
            "strongest": strongest,
            "learned_advantage": float(np.mean(learned) - np.mean(baselines[strongest])),
            "oracle_advantage": float(np.mean(oracle) - np.mean(baselines[strongest])),
            "acquisition_rate": float(np.mean(predicted_gain > cost)),
        }
    return result


# --------------------------------------------------------------------------
# the sweep
# --------------------------------------------------------------------------

def bootstrap_mean_ci(values: list[float], seed: int) -> tuple[float, float, float]:
    array = np.asarray(values, dtype=float)
    if len(array) < 5:
        return (float(np.mean(array)), float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    draws = np.array(
        [np.mean(array[rng.integers(0, len(array), len(array))]) for _ in range(BOOTSTRAP_DRAWS)]
    )
    ordered = np.sort(draws)
    return (
        float(np.mean(array)),
        float(ordered[int(0.025 * len(ordered))]),
        float(ordered[int(0.975 * len(ordered))]),
    )


def run() -> dict:
    findings: dict = {
        "declared": {
            "lam_grid": list(LAM_GRID),
            "base_strength_grid": list(BASE_STRENGTH_GRID),
            "cost_grid": list(COST_GRID),
            "worlds_per_cell": WORLDS_PER_CELL,
            "refute_margin": REFUTE_MARGIN,
            "signal_floor": SIGNAL_FLOOR,
            "gate": "a cell refutes §8.6 if learned advantage > refute_margin with "
            "a paired bootstrap interval over worlds excluding zero AND "
            "correlation > signal_floor",
            "expectations": "correlation rises with lam; prize falls with lam and "
            "with base_strength; learned advantage stays below margin everywhere; "
            "no prediction made for the middle region",
        },
        "cells": [],
    }

    for base_strength in BASE_STRENGTH_GRID:
        for lam in LAM_GRID:
            rng = np.random.default_rng(
                SEED + int(1000 * lam) + int(100 * base_strength)
            )
            worlds = []
            for _ in range(WORLDS_PER_CELL):
                world = make_world(rng, lam, base_strength)
                outcome = evaluate_world(world, rng)
                if outcome is not None:
                    worlds.append(outcome)
            if len(worlds) < 10:
                continue

            cell = {
                "lam": lam,
                "base_strength": base_strength,
                "n_worlds": len(worlds),
                "base_auc": float(np.mean([w["base_auc"] for w in worlds])),
                "full_auc": float(np.mean([w["full_auc"] for w in worlds])),
                "share_changed": float(np.mean([w["share_changed"] for w in worlds])),
                "mean_gain": float(np.mean([w["mean_gain"] for w in worlds])),
                "costs": {},
            }
            corr_mean, corr_lo, corr_hi = bootstrap_mean_ci(
                [w["correlation"] for w in worlds], SEED
            )
            cell["correlation"] = corr_mean
            cell["correlation_ci"] = [corr_lo, corr_hi]

            for cost in COST_GRID:
                key = str(cost)
                advantages = [w["costs"][key]["learned_advantage"] for w in worlds]
                mean, lo, hi = bootstrap_mean_ci(advantages, SEED + 1)
                oracle = float(
                    np.mean([w["costs"][key]["oracle_advantage"] for w in worlds])
                )
                refutes = bool(
                    mean > REFUTE_MARGIN and lo > 0.0 and corr_mean > SIGNAL_FLOOR
                )
                cell["costs"][key] = {
                    "learned_advantage": mean,
                    "ci": [lo, hi],
                    "oracle_advantage": oracle,
                    "acquisition_rate": float(
                        np.mean([w["costs"][key]["acquisition_rate"] for w in worlds])
                    ),
                    "refutes_condition": refutes,
                }
            findings["cells"].append(cell)

    refuting = [
        (c["lam"], c["base_strength"], cost)
        for c in findings["cells"]
        for cost, entry in c["costs"].items()
        if entry["refutes_condition"]
    ]
    findings["summary"] = {
        "cells": len(findings["cells"]),
        "tests": len(findings["cells"]) * len(COST_GRID),
        "refuting_cells": refuting,
        "condition_survives": len(refuting) == 0,
    }
    return findings


def report(findings: dict) -> str:
    lines = [
        "",
        "  EXP-010 — is the §8.6 condition a mechanism or a cohort artefact?",
        "  " + "=" * 78,
        f"  {findings['declared']['worlds_per_cell']} synthetic worlds per cell; "
        f"lam = how much the base state anticipates the acquirable block",
        f"  gate: a cell refutes the condition if learned advantage > "
        f"{REFUTE_MARGIN} with interval excluding zero AND corr > {SIGNAL_FLOOR}",
        "",
        "   base_str   lam   base_auc  changed   prize      corr            "
        "learned adv (cost 0.0)      verdict",
    ]
    for cell in findings["cells"]:
        entry = cell["costs"]["0.0"]
        lo, hi = entry["ci"]
        clo, chi = cell["correlation_ci"]
        verdict = "REFUTES" if entry["refutes_condition"] else "consistent"
        lines.append(
            f"     {cell['base_strength']:>5.2f}  {cell['lam']:>4.1f}   "
            f"{cell['base_auc']:.3f}    {cell['share_changed']:>5.1%}  "
            f"{cell['mean_gain']:+.4f}  "
            f"{cell['correlation']:+.3f} [{clo:+.3f},{chi:+.3f}]  "
            f"{entry['learned_advantage']:+.4f} [{lo:+.4f},{hi:+.4f}]   {verdict}"
        )

    lines += ["", "  oracle advantage, to confirm a prize existed at all:"]
    for cell in findings["cells"]:
        lines.append(
            f"     base_str {cell['base_strength']:.2f}  lam {cell['lam']:.1f}   "
            f"oracle {cell['costs']['0.0']['oracle_advantage']:+.4f}   "
            f"acquires {cell['costs']['0.0']['acquisition_rate']:.1%}"
        )

    summary = findings["summary"]
    lines += [
        "",
        "  " + "=" * 78,
        f"  cells {summary['cells']}, tests {summary['tests']}, "
        f"refuting {len(summary['refuting_cells'])}",
    ]
    if summary["condition_survives"]:
        lines += [
            "  The condition survives the sweep. Predictability of direction and the",
            "  prize for acquiring trade off against each other across the whole grid,",
            "  so no region supports a selective policy. This is mechanism evidence",
            "  for §8.6 and not a substitute for a second real information block.",
        ]
    else:
        lines += [
            "  REFUTED. At least one region admits both a usable selection signal and",
            "  a real prize, so the condition as stated in §8.6 is wrong and must be",
            f"  narrowed or withdrawn. Refuting cells: {summary['refuting_cells']}",
        ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    findings = run()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(report(findings))


if __name__ == "__main__":
    main()
