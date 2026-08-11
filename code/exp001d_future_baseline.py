"""EXP-001D: 2021-to-2022 baseline transport without opening the 2023 vault."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import log_loss
from sklearn.model_selection import StratifiedKFold

import p1_real_baseline as baseline
import p1_sec_history_acquisition as history

EXPECTED_SPLITS = {"future_train": 2369, "future_validation": 2243, "locked_test": 914}


def load_data(path: Path, config: dict, feature_config: dict) -> pd.DataFrame:
    data = pd.read_csv(path, dtype={"cik": str})
    features = (
        feature_config["base_categorical_features"]
        + feature_config["base_numeric_features"]
        + feature_config["history_numeric_features"]
    )
    required = {"accession_number", "cik", "split", config["target"], *features}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if data["split"].value_counts().to_dict() != EXPECTED_SPLITS:
        raise AssertionError("Unexpected future split counts")
    if data["cik"].duplicated().any() or data["accession_number"].duplicated().any():
        raise AssertionError("Future cohort is not company/accession unique")
    locked = data["split"].eq(config["locked_split"])
    if not data.loc[locked, config["target"]].isna().all():
        raise AssertionError("Locked outcomes are visible")
    usable = data["split"].isin([config["development_split"], config["evaluation_split"]])
    if data.loc[usable, config["target"]].isna().any():
        raise AssertionError("Development/evaluation outcomes are missing")
    return data

def tune_within_development(features, target, model_config, config):
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=config["seed"])
    scores = {}
    for c_value in config["selection"]["c_grid"]:
        fold_scores = []
        for fit_idx, score_idx in splitter.split(features, target):
            model = baseline.logistic_pipeline(model_config, c_value)
            model.fit(features.iloc[fit_idx], target[fit_idx])
            probability = model.predict_proba(features.iloc[score_idx])[:, 1]
            fold_scores.append(log_loss(target[score_idx], probability, labels=[0, 1]))
        scores[str(c_value)] = float(np.mean(fold_scores))
    selected = min(config["selection"]["c_grid"], key=lambda value: scores[str(value)])
    model = baseline.logistic_pipeline(model_config, selected)
    model.fit(features, target)
    return selected, model, scores


def evaluate(target, probability, config):
    metrics = baseline.predictive_metrics(target, probability)
    utility, arrays = baseline.utility_metrics(target, probability, config["utility_grid"])
    metrics["utility"] = utility
    metrics["calibration_bins"] = baseline.calibration_bins(target, probability)
    return metrics, arrays


def run(args) -> dict:
    config = baseline.load_config(args.config)
    feature_config = baseline.load_config(args.feature_config)
    data = load_data(args.input, config, feature_config)
    development = data["split"].eq(config["development_split"])
    evaluation = data["split"].eq(config["evaluation_split"])
    y_dev = data.loc[development, config["target"]].astype(int).to_numpy()
    y_eval = data.loc[evaluation, config["target"]].astype(int).to_numpy()

    base_config = history.model_config(feature_config, include_history=False)
    full_config = history.model_config(feature_config, include_history=True)
    base_columns = base_config["categorical_features"] + base_config["numeric_features"]
    full_columns = full_config["categorical_features"] + full_config["numeric_features"]
    selected_base, base_model, base_cv = tune_within_development(
        data.loc[development, base_columns], y_dev, base_config, config
    )
    selected_full, full_model, full_cv = tune_within_development(
        data.loc[development, full_columns], y_dev, full_config, config
    )
    prior = np.full(len(y_eval), y_dev.mean())
    base_probability = base_model.predict_proba(data.loc[evaluation, base_columns])[:, 1]
    full_probability = full_model.predict_proba(data.loc[evaluation, full_columns])[:, 1]

    results = {
        "experiment": config["experiment"],
        "scope": config["scope"],
        "claim_boundary": config["claim_boundary"],
        "utility_status": config["utility_status"],
        "split_counts": EXPECTED_SPLITS,
        "locked_test_accessed": False,
        "selected_c": {"anchor_only": selected_base, "anchor_plus_sec_history": selected_full},
        "development_cv_log_loss": {"anchor_only": base_cv, "anchor_plus_sec_history": full_cv},
        "evaluation": {},
        "paired_utility_deltas": {},
        "hashes": {
            "config_sha256": baseline.sha256(args.config),
            "input_sha256": baseline.sha256(args.input),
            "script_sha256": baseline.sha256(Path(__file__)),
        },
    }
    arrays = {}
    for name, probability in {
        "development_prior": prior,
        "anchor_only": base_probability,
        "anchor_plus_sec_history": full_probability,
    }.items():
        results["evaluation"][name], arrays[name] = evaluate(y_eval, probability, config)
    for scenario in config["utility_grid"]:
        results["paired_utility_deltas"][scenario] = {
            "full_minus_anchor": baseline.paired_bootstrap(
                arrays["anchor_plus_sec_history"][scenario], arrays["anchor_only"][scenario],
                config["seed"], config["bootstrap_draws"],
            ),
            "full_minus_prior": baseline.paired_bootstrap(
                arrays["anchor_plus_sec_history"][scenario], arrays["development_prior"][scenario],
                config["seed"] + 1, config["bootstrap_draws"],
            ),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=Path,
        default=Path("datasets/processed/sec_form_d_future_2021_2023/p1_first_anchor_model_ready.csv"),
    )
    parser.add_argument("--config", type=Path, default=Path("experiments/EXP-001D/config.json"))
    parser.add_argument(
        "--feature-config", type=Path, default=Path("experiments/EXP-001C/config.json")
    )
    parser.add_argument("--output", type=Path, default=Path("experiments/EXP-001D/results.json"))
    results = run(parser.parse_args())
    summary = {
        "experiment": results["experiment"],
        "locked_test_accessed": results["locked_test_accessed"],
        "selected_c": results["selected_c"],
        "evaluation": {
            name: {
                key: value for key, value in metrics.items()
                if key in {"n", "positive_rate", "roc_auc", "average_precision", "log_loss", "brier"}
            }
            for name, metrics in results["evaluation"].items()
        },
        "paired_utility_deltas": results["paired_utility_deltas"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
