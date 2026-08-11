"""EXP-001C: exploratory cost-aware acquisition of point-in-time SEC issuer history.

The base model sees anchor-only fields. The acquired model additionally sees issuer-history fields.
Out-of-fold training gains teach a base-state meta-policy where acquisition may be worthwhile.
Costs are normalized assumptions pending buyer elicitation; this is not confirmatory P1 evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import log_loss
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline

import p1_real_baseline as baseline


def model_config(config: dict, include_history: bool) -> dict:
    numeric = list(config["base_numeric_features"])
    if include_history:
        numeric += config["history_numeric_features"]
    return {
        "seed": config["seed"],
        "categorical_features": config["base_categorical_features"],
        "numeric_features": numeric,
        "signed_log1p_features": [
            column for column in config["signed_log1p_features"] if column in numeric
        ],
    }


def tune_model(features, target, train_mask, validation_mask, config, include_history):
    local = model_config(config, include_history)
    scores, models = {}, {}
    for c_value in config["model_selection"]["c_grid"]:
        model = baseline.logistic_pipeline(local, c_value)
        model.fit(features.loc[train_mask], target[train_mask])
        probability = model.predict_proba(features.loc[validation_mask])[:, 1]
        scores[str(c_value)] = float(log_loss(target[validation_mask], probability, labels=[0, 1]))
        models[c_value] = model
    selected = min(models, key=lambda value: scores[str(value)])
    return selected, models[selected], scores


def cross_fitted_probabilities(features, target, train_indices, config, include_history, c_value):
    local = model_config(config, include_history)
    output = np.full(len(target), np.nan)
    splitter = StratifiedKFold(
        n_splits=config["cross_fit_folds"], shuffle=True, random_state=config["seed"]
    )
    local_y = target[train_indices]
    for fit_local, predict_local in splitter.split(train_indices, local_y):
        fit_indices = train_indices[fit_local]
        predict_indices = train_indices[predict_local]
        model = baseline.logistic_pipeline(local, c_value)
        model.fit(features.loc[fit_indices], target[fit_indices])
        output[predict_indices] = model.predict_proba(features.loc[predict_indices])[:, 1]
    if np.isnan(output[train_indices]).any():
        raise AssertionError("Incomplete cross-fitted probabilities")
    return output


def entropy(probability):
    p = np.clip(np.asarray(probability), 1e-12, 1 - 1e-12)
    return -(p * np.log(p) + (1 - p) * np.log(1 - p))


def expected_decision_value(probability, utility):
    act = probability * utility["tp"] + (1 - probability) * utility["fp"]
    stop = probability * utility["fn"] + (1 - probability) * utility["tn"]
    return np.maximum(act, stop)


def gain_target(y, base_probability, full_probability, utility):
    base_action = baseline.optimal_decision(base_probability, utility)
    full_action = baseline.optimal_decision(full_probability, utility)
    base_value = baseline.realised_utility(y, base_action, utility)
    full_value = baseline.realised_utility(y, full_action, utility)
    return full_value - base_value


def meta_features(data, base_probability, base_columns):
    matrix = data[base_columns].copy()
    numeric = matrix.select_dtypes(include=[np.number]).columns
    matrix[numeric] = matrix[numeric].replace([np.inf, -np.inf], np.nan).fillna(0)
    matrix = matrix[numeric]
    extra = np.column_stack([
        base_probability,
        np.abs(base_probability - 0.5),
        entropy(base_probability),
    ])
    return np.column_stack([matrix.to_numpy(dtype=float), extra])


def fit_gain_model(meta_train, gain):
    return Pipeline([
        ("scale", baseline.StandardScaler()),
        ("ridge", Ridge(alpha=10.0)),
    ]).fit(meta_train, gain)


def policy_actions(policy, expected_gain, uncertainty_gain, validation_lift, cost, rng):
    count = len(expected_gain)
    if policy == "none":
        return np.zeros(count, dtype=bool)
    if policy == "random":
        return rng.random(count) < 0.5
    if policy == "cheapest":
        return np.ones(count, dtype=bool)
    if policy == "most_predictive":
        return np.full(count, validation_lift > 0)
    if policy == "uncertainty_reduction":
        return uncertainty_gain > 0
    if policy == "cost_aware_voi":
        return expected_gain > cost
    raise ValueError(policy)


def evaluate_policy(y, base_probability, full_probability, acquire, utility, cost):
    probability = np.where(acquire, full_probability, base_probability)
    action = baseline.optimal_decision(probability, utility)
    values = baseline.realised_utility(y, action, utility) - acquire.astype(float) * cost
    return values, float(np.mean(acquire)), float(np.mean(action))


def paired_ci(candidate, comparator, seed, draws):
    return baseline.paired_bootstrap(candidate, comparator, seed, draws)


def run(args):
    config = baseline.load_config(args.config)
    audit_config = {
        "categorical_features": config["base_categorical_features"],
        "numeric_features": config["base_numeric_features"] + config["history_numeric_features"],
    }
    data = baseline.load_and_audit(args.input, audit_config)
    target = data[config["target"]].astype(int).to_numpy()
    train = data["split"].eq("train").to_numpy()
    validation = data["split"].eq("validation").to_numpy()
    test = data["split"].eq("test").to_numpy()
    train_indices = np.flatnonzero(train)

    all_columns = config["base_categorical_features"] + config["base_numeric_features"] + config["history_numeric_features"]
    features = data[all_columns]
    base_c, base_model, base_scores = tune_model(features, target, train, validation, config, False)
    full_c, full_model, full_scores = tune_model(features, target, train, validation, config, True)
    base_probability = base_model.predict_proba(features)[:, 1]
    full_probability = full_model.predict_proba(features)[:, 1]
    oof_base = cross_fitted_probabilities(features, target, train_indices, config, False, base_c)
    oof_full = cross_fitted_probabilities(features, target, train_indices, config, True, full_c)

    base_columns = [column for column in config["base_numeric_features"] if column in data]
    meta_all = meta_features(data, base_probability, base_columns)
    meta_train = meta_features(data.loc[train].reset_index(drop=True), oof_base[train_indices], base_columns)
    validation_lift = float(
        log_loss(target[validation], base_probability[validation], labels=[0, 1])
        - log_loss(target[validation], full_probability[validation], labels=[0, 1])
    )
    train_uncertainty_gain = entropy(oof_base[train_indices]) - entropy(oof_full[train_indices])
    uncertainty_model = fit_gain_model(meta_train, train_uncertainty_gain)
    expected_uncertainty_gain = uncertainty_model.predict(meta_all[test])

    result = {
        "experiment": config["experiment"], "scope": config["scope"],
        "selected_c": {"anchor_only": base_c, "anchor_plus_history": full_c},
        "validation_log_loss": {
            "anchor_only": float(log_loss(target[validation], base_probability[validation], labels=[0, 1])),
            "anchor_plus_history": float(log_loss(target[validation], full_probability[validation], labels=[0, 1])),
            "history_lift": validation_lift,
            "candidate_scores": {"anchor_only": base_scores, "anchor_plus_history": full_scores},
        },
        "test_predictive": {
            "anchor_only": baseline.predictive_metrics(target[test], base_probability[test]),
            "anchor_plus_history": baseline.predictive_metrics(target[test], full_probability[test]),
        },
        "cost_results": {},
    }

    rng = np.random.default_rng(config["seed"])
    for utility_index, (utility_name, utility) in enumerate(config["utility_grid"].items()):
        train_gain = gain_target(
            target[train_indices], oof_base[train_indices], oof_full[train_indices], utility
        )
        gain_model = fit_gain_model(meta_train, train_gain)
        expected_gain = gain_model.predict(meta_all[test])
        result["cost_results"][utility_name] = {}
        for cost_index, cost in enumerate(config["normalized_cost_grid"]):
            policy_values, policy_meta = {}, {}
            for policy in config["policies"]:
                acquire = policy_actions(
                    policy, expected_gain, expected_uncertainty_gain, validation_lift, cost, rng
                )
                values, acquire_rate, act_rate = evaluate_policy(
                    target[test], base_probability[test], full_probability[test],
                    acquire, utility, cost,
                )
                policy_values[policy] = values
                policy_meta[policy] = {
                    "mean_ndv": float(np.mean(values)),
                    "acquisition_rate": acquire_rate,
                    "act_rate": act_rate,
                }
            comparators = [policy for policy in config["policies"] if policy != "cost_aware_voi"]
            strongest = max(comparators, key=lambda name: policy_meta[name]["mean_ndv"])
            comparison = paired_ci(
                policy_values["cost_aware_voi"], policy_values[strongest],
                config["seed"] + utility_index * 100 + cost_index,
                config["bootstrap_draws"],
            )
            result["cost_results"][utility_name][str(cost)] = {
                "policies": policy_meta,
                "strongest_non_voi": strongest,
                "cost_aware_delta": comparison,
                "exploratory_gate_pass": bool(
                    comparison["mean_delta"] > 0 and comparison["ci_95"][0] > 0
                ),
            }

    result["hashes"] = {
        "input_sha256": baseline.sha256(args.input),
        "config_sha256": baseline.sha256(args.config),
        "script_sha256": baseline.sha256(Path(__file__)),
    }
    result["claim_boundary"] = (
        "Exploratory single-block SEC-history acquisition with assumed normalized costs; not buyer-elicited or confirmatory."
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(
        "datasets/processed/sec_form_d_v2/p1_first_anchor_model_ready.csv"))
    parser.add_argument("--config", type=Path, default=Path("experiments/EXP-001C/config.json"))
    parser.add_argument("--output", type=Path, default=Path("experiments/EXP-001C/results.json"))
    args = parser.parse_args()
    result = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    compact = {
        "validation_log_loss": result["validation_log_loss"],
        "test_predictive": result["test_predictive"],
        "summary": {
            utility: {
                cost: {
                    "strongest": values["strongest_non_voi"],
                    "delta": values["cost_aware_delta"],
                    "pass": values["exploratory_gate_pass"],
                    "cost_aware": values["policies"]["cost_aware_voi"],
                }
                for cost, values in costs.items()
            }
            for utility, costs in result["cost_results"].items()
        },
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
