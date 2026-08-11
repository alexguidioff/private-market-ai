"""EXP-001A: learned cost-aware acquisition on synthetic temporal cohorts."""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

ACTIONS = ("technical", "founder_research", "public_attention", "licensed")
POLICIES = ("none", "random", "cheapest", "most_predictive",
            "uncertainty_reduction", "cost_aware_voi", "oracle")
TRAIN_YEARS = (2016, 2017, 2018)
VALIDATION_YEAR, TEST_YEAR = 2019, 2020
C_GRID = (0.1, 1.0, 10.0)
TP, FP, FN, TN = 1.0, -0.45, -0.85, 0.0
DEFAULT_SEED = 20260721
SIGNAL_STATES = np.asarray(list(product((0.0, 1.0), repeat=len(ACTIONS))))


def sigmoid(value):
    return 1.0 / (1.0 + np.exp(-np.clip(value, -30.0, 30.0)))


def decision_value(probability):
    act = probability * TP + (1.0 - probability) * FP
    stop = probability * FN + (1.0 - probability) * TN
    return np.maximum(act, stop), act >= stop


def fit_logistic(x, y, c_value=1.0):
    return LogisticRegression(C=c_value, max_iter=1000, solver="lbfgs").fit(x, y)


def make_world(rng):
    return {
        "intercept": float(rng.uniform(-1.4, -0.4)),
        "base_beta": rng.normal(0.0, 0.65, 3),
        "signal_beta": rng.uniform(0.6, 1.8, len(ACTIONS)) * rng.choice((-1.0, 1.0), len(ACTIONS)),
        "signal_intercept": rng.normal(0.0, 0.5, len(ACTIONS)),
        "signal_base_beta": rng.normal(0.0, 0.7, (len(ACTIONS), 3)),
        "costs": rng.uniform(0.015, 0.16, len(ACTIONS)),
    }
def generate(world, n_per_year, rng):
    years = np.repeat(np.arange(2016, 2021), n_per_year)
    base = rng.normal(0.0, 1.0, (len(years), 3))
    base[:, 1] += 0.12 * (years - 2016)
    signal_probability = sigmoid(world["signal_intercept"] + base @ world["signal_base_beta"].T)
    signals = rng.binomial(1, signal_probability)
    outcome_probability = sigmoid(world["intercept"] + base @ world["base_beta"] + signals @ world["signal_beta"])
    outcome = rng.binomial(1, outcome_probability)
    return years, base, signal_probability, signals, outcome


def outcome_features(base, signals, known_action=None):
    masked = np.zeros_like(signals, dtype=float)
    indicators = np.zeros_like(signals, dtype=float)
    if known_action is not None:
        masked[:, known_action] = signals[:, known_action]
        indicators[:, known_action] = 1.0
    return np.column_stack((base, masked, indicators))


def tune_outcome_models(years, base, signals, outcome):
    train = np.isin(years, TRAIN_YEARS)
    validation = years == VALIDATION_YEAR
    models, validation_auc = [], []
    for action in [None, *range(len(ACTIONS))]:
        features = outcome_features(base, signals, action)
        candidates = []
        for c_value in C_GRID:
            fitted = fit_logistic(features[train], outcome[train], c_value)
            probability = fitted.predict_proba(features[validation])[:, 1]
            candidates.append((roc_auc_score(outcome[validation], probability), fitted))
        auc, fitted = max(candidates, key=lambda item: item[0])
        validation_auc.append(float(auc))
        models.append(fitted)
    return models[0], models[1:], np.asarray(validation_auc[1:])


def fit_signal_models(years, base, signals):
    train = np.isin(years, TRAIN_YEARS)
    return [fit_logistic(base[train], signals[train, action]) for action in range(len(ACTIONS))]


def expected_action_values(base, base_model, action_models, signal_models):
    blank = np.zeros((len(base), len(ACTIONS)))
    base_probability = base_model.predict_proba(outcome_features(base, blank))[:, 1]
    base_value, _ = decision_value(base_probability)
    entropy = lambda p: -(p*np.log(np.clip(p, 1e-12, 1.0)) + (1-p)*np.log(np.clip(1-p, 1e-12, 1.0)))
    values, reductions = [], []
    for action, (outcome_model, signal_model) in enumerate(zip(action_models, signal_models)):
        signal_probability = signal_model.predict_proba(base)[:, 1]
        zero = blank.copy()
        one = blank.copy(); one[:, action] = 1.0
        p_zero = outcome_model.predict_proba(outcome_features(base, zero, action))[:, 1]
        p_one = outcome_model.predict_proba(outcome_features(base, one, action))[:, 1]
        value_zero, _ = decision_value(p_zero); value_one, _ = decision_value(p_one)
        values.append((1-signal_probability)*value_zero + signal_probability*value_one)
        reductions.append(entropy(base_probability) - ((1-signal_probability)*entropy(p_zero) + signal_probability*entropy(p_one)))
    return base_value, np.column_stack(values), np.column_stack(reductions)
def select_actions(policy, base_value, values, reductions, costs, lifts, rng):
    count = len(base_value)
    if policy == "none":
        return np.full(count, -1)
    if policy == "random":
        return rng.integers(-1, len(ACTIONS), count)
    if policy == "cheapest":
        return np.full(count, int(np.argmin(costs)))
    if policy == "most_predictive":
        return np.full(count, int(np.argmax(lifts)))
    if policy == "uncertainty_reduction":
        return np.argmax(reductions, axis=1)
    net = values - costs
    candidate = np.argmax(net, axis=1)
    return np.where(np.max(net, axis=1) > base_value, candidate, -1)


def oracle_actions(base, signal_probability, world):
    joint = np.prod(np.where(SIGNAL_STATES[None, :, :] == 1,
                             signal_probability[:, None, :],
                             1-signal_probability[:, None, :]), axis=2)
    state_effect = SIGNAL_STATES @ world["signal_beta"]
    full_probability = sigmoid(world["intercept"] + (base @ world["base_beta"])[:, None] + state_effect[None, :])
    base_probability = np.sum(joint * full_probability, axis=1)
    base_value, _ = decision_value(base_probability)
    action_values = []
    for action in range(len(ACTIONS)):
        probability_if_zero = np.sum(joint * full_probability * (SIGNAL_STATES[None, :, action] == 0), axis=1) / np.clip(1-signal_probability[:, action], 1e-12, 1)
        probability_if_one = np.sum(joint * full_probability * (SIGNAL_STATES[None, :, action] == 1), axis=1) / np.clip(signal_probability[:, action], 1e-12, 1)
        value_if_zero, _ = decision_value(probability_if_zero)
        value_if_one, _ = decision_value(probability_if_one)
        action_values.append((1-signal_probability[:, action])*value_if_zero + signal_probability[:, action]*value_if_one - world["costs"][action])
    action_values = np.column_stack(action_values)
    candidate = np.argmax(action_values, axis=1)
    return np.where(np.max(action_values, axis=1) > base_value, candidate, -1)


def realised_ndv(base, signals, outcome, actions, base_model, action_models, costs):
    blank = np.zeros_like(signals, dtype=float)
    probability = base_model.predict_proba(outcome_features(base, blank))[:, 1]
    paid = np.zeros(len(outcome))
    for action, fitted in enumerate(action_models):
        selected = actions == action
        if selected.any():
            probability[selected] = fitted.predict_proba(outcome_features(base[selected], signals[selected], action))[:, 1]
            paid[selected] = costs[action]
    _, act = decision_value(probability)
    payoff = np.where(act, np.where(outcome == 1, TP, FP), np.where(outcome == 1, FN, TN))
    return payoff - paid


def oracle_realised_ndv(base, signal_probability, signals, outcome, actions, world):
    state_effect = SIGNAL_STATES @ world["signal_beta"]
    full_probability = sigmoid(world["intercept"] + (base @ world["base_beta"])[:, None] + state_effect[None, :])
    joint = np.prod(np.where(SIGNAL_STATES[None, :, :] == 1,
                             signal_probability[:, None, :],
                             1-signal_probability[:, None, :]), axis=2)
    probability = np.sum(joint * full_probability, axis=1)
    paid = np.zeros(len(outcome))
    for action in range(len(ACTIONS)):
        selected = actions == action
        if not selected.any():
            continue
        state_match = SIGNAL_STATES[:, action][None, :] == signals[selected, action][:, None]
        conditional_weight = joint[selected] * state_match
        normalizer = np.clip(np.sum(conditional_weight, axis=1), 1e-12, None)
        probability[selected] = np.sum(conditional_weight * full_probability[selected], axis=1) / normalizer
        paid[selected] = world["costs"][action]
    _, act = decision_value(probability)
    payoff = np.where(act, np.where(outcome == 1, TP, FP), np.where(outcome == 1, FN, TN))
    return payoff - paid
def evaluate_world(world_id, n_per_year, seed, cost_scale=1.0):
    rng = np.random.default_rng(seed + 1009*world_id)
    world = make_world(rng)
    world["costs"] = world["costs"] * cost_scale
    years, base, signal_probability, signals, outcome = generate(world, n_per_year, rng)
    base_model, action_models, lifts = tune_outcome_models(years, base, signals, outcome)
    signal_models = fit_signal_models(years, base, signals)
    test = years == TEST_YEAR
    base_value, values, reductions = expected_action_values(base[test], base_model, action_models, signal_models)
    scores, rates = {}, {}
    for policy in POLICIES:
        if policy == "oracle":
            actions = oracle_actions(base[test], signal_probability[test], world)
            scores[policy] = oracle_realised_ndv(base[test], signal_probability[test], signals[test],
                                                  outcome[test], actions, world)
        else:
            actions = select_actions(policy, base_value, values, reductions,
                                     world["costs"], lifts, rng)
            scores[policy] = realised_ndv(base[test], signals[test], outcome[test], actions,
                                          base_model, action_models, world["costs"])
        rates[policy] = float(np.mean(actions >= 0))
    return scores, rates


def bootstrap_delta(candidate, comparator, rng, draws=1000):
    delta = candidate - comparator
    samples = np.mean(delta[rng.integers(0, len(delta), (draws, len(delta)))], axis=1)
    return np.quantile(samples, (0.025, 0.975))


def run(worlds, n_per_year, seed, cost_scale=1.0):
    world_means = {policy: [] for policy in POLICIES}
    rates = {policy: [] for policy in POLICIES}
    for world_id in range(worlds):
        world_scores, world_rates = evaluate_world(world_id, n_per_year, seed, cost_scale)
        for policy in POLICIES:
            world_means[policy].append(float(np.mean(world_scores[policy])))
            rates[policy].append(world_rates[policy])
    means = {policy: float(np.mean(values)) for policy, values in world_means.items()}
    comparators = [policy for policy in POLICIES if policy not in ("cost_aware_voi", "oracle")]
    strongest = max(comparators, key=means.get)
    candidate = np.asarray(world_means["cost_aware_voi"])
    comparator = np.asarray(world_means[strongest])
    delta = means["cost_aware_voi"] - means[strongest]
    ci = bootstrap_delta(candidate, comparator, np.random.default_rng(seed+999999))
    return {
        "experiment": "EXP-001A", "scope": "synthetic learned-policy test; no market-realism claim",
        "seed": seed, "worlds": worlds, "n_per_year": n_per_year, "cost_scale": cost_scale,
        "test_observations": worlds*n_per_year,
        "split": {"train": list(TRAIN_YEARS), "validation": VALIDATION_YEAR, "test": TEST_YEAR},
        "mean_ndv": {policy: round(means[policy], 6) for policy in POLICIES},
        "mean_acquisition_rate": {policy: round(float(np.mean(rates[policy])), 6) for policy in POLICIES},
        "strongest_non_voi_baseline": strongest, "paired_delta": round(delta, 6),
        "paired_bootstrap_95_ci": [round(float(value), 6) for value in ci],
        "synthetic_gate_pass": bool(delta > 0 and ci[0] > 0),
    }
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worlds", type=int, default=100)
    parser.add_argument("--n-per-year", type=int, default=250)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--cost-scale", type=float, default=1.0)
    parser.add_argument("--output", type=Path, default=Path("experiments/EXP-001A/results.json"))
    args = parser.parse_args()
    result = run(args.worlds, args.n_per_year, args.seed, args.cost_scale)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
