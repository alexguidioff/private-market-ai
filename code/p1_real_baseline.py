"""EXP-001B: real SEC weak-proxy baseline and owner-accepted pilot sensitivity.

This is an exploratory predictive/zero-acquisition decision baseline, not a Value-of-Information
test. The model is selected on 2019 and evaluated once on the 2020 temporal test split.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score, brier_score_loss, log_loss, roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

EXPECTED_SPLITS = {"train": 8455, "validation": 2095, "test": 1831}
EXPECTED_ROWS = 12381


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def signed_log1p(values):
    array = np.asarray(values, dtype=float)
    return np.sign(array) * np.log1p(np.abs(array))


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_and_audit(path: Path, config: dict) -> pd.DataFrame:
    data = pd.read_csv(path, dtype={"cik": str})
    required = {
        "accession_number", "cik", "filing_time", "decision_time", "label_window_end",
        "first_notice_after_decision", "subsequent_notice_18m", "split",
        *config["categorical_features"], *config["numeric_features"],
    }
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if len(data) != EXPECTED_ROWS or data["cik"].nunique() != EXPECTED_ROWS:
        raise AssertionError("Expected one unique CIK for each of 12,381 rows")
    if data["accession_number"].duplicated().any():
        raise AssertionError("Duplicate accession numbers")
    split_counts = data["split"].value_counts().to_dict()
    if split_counts != EXPECTED_SPLITS:
        raise AssertionError(f"Unexpected split counts: {split_counts}")

    decision = pd.to_datetime(data["decision_time"], format="mixed", errors="raise")
    end = pd.to_datetime(data["label_window_end"], format="mixed", errors="raise")
    future = pd.to_datetime(data["first_notice_after_decision"], format="mixed", errors="coerce")
    positive = data["subsequent_notice_18m"].eq(1)
    if (decision >= end).any():
        raise AssertionError("Invalid label window")
    if (positive & ((future <= decision) | (future > end) | future.isna())).any():
        raise AssertionError("Positive label violates temporal window")
    if ((~positive) & future.notna() & (future > decision) & (future <= end)).any():
        raise AssertionError("Negative row has an in-window notice")
    return data


def make_preprocessor(config: dict) -> ColumnTransformer:
    signed = set(config["signed_log1p_features"])
    plain_numeric = [column for column in config["numeric_features"] if column not in signed]
    transformers = [
        (
            "categorical",
            Pipeline([
                ("impute", SimpleImputer(strategy="constant", fill_value="__MISSING__")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]),
            config["categorical_features"],
        ),
    ]
    if plain_numeric:
        transformers.append((
            "numeric",
            Pipeline([
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
            ]),
            plain_numeric,
        ))
    transformers.append((
        "signed_log_numeric",
        Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("log", FunctionTransformer(signed_log1p, feature_names_out="one-to-one")),
            ("scale", StandardScaler()),
        ]),
        config["signed_log1p_features"],
    ))
    return ColumnTransformer(transformers)


def logistic_pipeline(config: dict, c_value: float) -> Pipeline:
    return Pipeline([
        ("preprocess", make_preprocessor(config)),
        ("model", LogisticRegression(C=c_value, max_iter=2000, random_state=config["seed"])),
    ])


def predictive_metrics(y_true, probability) -> dict:
    return {
        "n": int(len(y_true)),
        "positive_rate": float(np.mean(y_true)),
        "roc_auc": float(roc_auc_score(y_true, probability)),
        "average_precision": float(average_precision_score(y_true, probability)),
        "log_loss": float(log_loss(y_true, probability, labels=[0, 1])),
        "brier": float(brier_score_loss(y_true, probability)),
        "mean_probability": float(np.mean(probability)),
    }


def optimal_decision(probability, utility: dict) -> np.ndarray:
    act = probability * utility["tp"] + (1.0 - probability) * utility["fp"]
    stop = probability * utility["fn"] + (1.0 - probability) * utility["tn"]
    return act > stop


def realised_utility(y_true, action, utility: dict) -> np.ndarray:
    return np.where(
        action,
        np.where(y_true == 1, utility["tp"], utility["fp"]),
        np.where(y_true == 1, utility["fn"], utility["tn"]),
    ).astype(float)


def utility_metrics(y_true, probability, utility_grid: dict) -> tuple[dict, dict[str, np.ndarray]]:
    output, arrays = {}, {}
    for name, utility in utility_grid.items():
        action = optimal_decision(probability, utility)
        values = realised_utility(y_true, action, utility)
        output[name] = {
            "mean_utility": float(np.mean(values)),
            "act_rate": float(np.mean(action)),
            "decision_accuracy": float(np.mean(action == y_true)),
        }
        arrays[name] = values
    return output, arrays


def paired_bootstrap(candidate, comparator, seed: int, draws: int) -> dict:
    delta = np.asarray(candidate) - np.asarray(comparator)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(delta), size=(draws, len(delta)))
    samples = delta[indices].mean(axis=1)
    interval = np.quantile(samples, [0.025, 0.975])
    return {
        "mean_delta": float(delta.mean()),
        "ci_95": [float(interval[0]), float(interval[1])],
    }


def calibration_bins(y_true, probability, bins: int = 10) -> list[dict]:
    frame = pd.DataFrame({"y": np.asarray(y_true), "p": np.asarray(probability)})
    frame["bin"] = pd.cut(frame["p"], bins=np.linspace(0, 1, bins + 1), include_lowest=True)
    rows = []
    for interval, group in frame.groupby("bin", observed=False):
        if group.empty:
            continue
        rows.append({
            "interval": str(interval), "n": int(len(group)),
            "mean_probability": float(group["p"].mean()),
            "observed_rate": float(group["y"].mean()),
        })
    return rows


def pilot_sensitivity(data, probability, pilot_queue: Path, pilot_labels: Path, utility_grid: dict) -> dict:
    queue = pd.read_csv(pilot_queue, dtype={"cik": str})
    labels = pd.read_csv(pilot_labels)
    pilot = queue.merge(labels, on="gold_record_id", validate="one_to_one")
    prediction = pd.DataFrame({
        "anchor_accession": data["accession_number"],
        "weak_probability": probability,
        "weak_proxy_label": data["subsequent_notice_18m"],
    })
    pilot = pilot.merge(prediction, on="anchor_accession", validate="one_to_one")
    if len(pilot) != 20:
        raise AssertionError("Pilot join must contain 20 records")

    output = {"rows": 20, "label_counts": pilot["accepted_financing_event_label"].value_counts().to_dict()}
    known = pilot["accepted_financing_event_label"].ne("unknown")
    y_known = pilot.loc[known, "accepted_financing_event_label"].eq("positive").astype(int).to_numpy()
    p_known = pilot.loc[known, "weak_probability"].to_numpy()
    output["known_only"] = predictive_metrics(y_known, p_known) if len(np.unique(y_known)) == 2 else {
        "n": int(len(y_known)), "warning": "Only one class; predictive metrics undefined"
    }
    output["unknown_bounds"] = {}
    for unknown_value in (0, 1):
        y = pilot["accepted_financing_event_label"].map(
            {"positive": 1, "no_public_evidence": 0, "unknown": unknown_value}
        ).to_numpy()
        metrics = predictive_metrics(y, pilot["weak_probability"].to_numpy())
        metrics["utility"], _ = utility_metrics(y, pilot["weak_probability"].to_numpy(), utility_grid)
        output["unknown_bounds"][str(unknown_value)] = metrics
    output["claim_boundary"] = (
        "Balanced owner-accepted model-reviewed pilot; descriptive sensitivity only, no prevalence or gold-test claim."
    )
    return output


def run(args) -> dict:
    config = load_config(args.config)
    data = load_and_audit(args.input, config)
    target = data[config["target"]].astype(int).to_numpy()
    masks = {name: data["split"].eq(name).to_numpy() for name in EXPECTED_SPLITS}
    features = data[config["categorical_features"] + config["numeric_features"]]

    dummy = DummyClassifier(strategy="prior")
    dummy.fit(np.zeros((masks["train"].sum(), 1)), target[masks["train"]])
    probabilities = {
        "dummy_prior": dummy.predict_proba(np.zeros((len(data), 1)))[:, 1]
    }

    validation_scores = {}
    fitted_candidates = {}
    for c_value in config["model_selection"]["c_grid"]:
        model = logistic_pipeline(config, c_value)
        model.fit(features.loc[masks["train"]], target[masks["train"]])
        probability = model.predict_proba(features.loc[masks["validation"]])[:, 1]
        score = float(log_loss(target[masks["validation"]], probability, labels=[0, 1]))
        validation_scores[str(c_value)] = score
        fitted_candidates[c_value] = model
    selected_c = min(fitted_candidates, key=lambda value: validation_scores[str(value)])
    model = fitted_candidates[selected_c]
    probabilities["logistic_regression"] = model.predict_proba(features)[:, 1]

    results = {
        "experiment": config["experiment"], "scope": config["scope"],
        "seed": config["seed"], "target": config["target"],
        "split_counts": {name: int(mask.sum()) for name, mask in masks.items()},
        "selected_c": selected_c, "validation_log_loss_by_c": validation_scores,
        "feature_count_input": len(config["categorical_features"]) + len(config["numeric_features"]),
        "models": {},
    }
    utility_arrays = {}
    for name, probability in probabilities.items():
        results["models"][name] = {}
        utility_arrays[name] = {}
        for split in ("validation", "test"):
            mask = masks[split]
            predictive = predictive_metrics(target[mask], probability[mask])
            utility, arrays = utility_metrics(target[mask], probability[mask], config["utility_grid"])
            predictive["utility"] = utility
            predictive["calibration_bins"] = calibration_bins(target[mask], probability[mask])
            results["models"][name][split] = predictive
            utility_arrays[name][split] = arrays

    results["test_paired_utility_delta_logistic_minus_dummy"] = {
        utility_name: paired_bootstrap(
            utility_arrays["logistic_regression"]["test"][utility_name],
            utility_arrays["dummy_prior"]["test"][utility_name],
            config["seed"] + index,
            config["bootstrap_draws"],
        )
        for index, utility_name in enumerate(config["utility_grid"].keys())
    }
    results["pilot_layer_a_sensitivity"] = pilot_sensitivity(
        data, probabilities["logistic_regression"], args.pilot_queue, args.pilot_labels,
        config["utility_grid"],
    )
    results["hashes"] = {
        "input_sha256": sha256(args.input), "config_sha256": sha256(args.config),
        "script_sha256": sha256(Path(__file__)),
    }
    results["environment"] = {
        "python": platform.python_version(), "pandas": pd.__version__,
        "numpy": np.__version__, "scikit_learn": sklearn.__version__,
    }
    results["claim_boundary"] = (
        "Predictive and zero-acquisition decision baseline on a weak SEC proxy; not a VoI test and not evidence of startup success."
    )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(
        "datasets/processed/sec_form_d_v2/p1_first_anchor_model_ready.csv"))
    parser.add_argument("--config", type=Path, default=Path("experiments/EXP-001B/config.json"))
    parser.add_argument("--pilot-queue", type=Path, default=Path(
        "datasets/processed/sec_form_d_v2/gold/pilot20/pilot_annotation_queue.csv"))
    parser.add_argument("--pilot-labels", type=Path, default=Path(
        "datasets/processed/sec_form_d_v2/gold/pilot20/pilot_accepted_labels.csv"))
    parser.add_argument("--output", type=Path, default=Path("experiments/EXP-001B/results.json"))
    args = parser.parse_args()
    result = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "selected_c": result["selected_c"],
        "test": {name: values["test"] for name, values in result["models"].items()},
        "paired_utility_delta": result["test_paired_utility_delta_logistic_minus_dummy"],
        "pilot_layer_a_sensitivity": result["pilot_layer_a_sensitivity"],
    }, indent=2))


if __name__ == "__main__":
    main()
