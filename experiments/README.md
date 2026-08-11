# Experiments

Log of experiments. One folder or entry per experiment.

## Template
```
# EXP-<id> — <short title>

- **Date:**
- **Hypothesis:**
- **Setup:** (data, features, model, split)
- **Metrics:** (R², MAE, ranking metrics, ...)
- **Result:**
- **Interpretation (SHAP / feature importance):**
- **Decision / next step:**
```

## Index
| ID | Title | Date | Status | Key result |
|---|---|---|---|---|
| P0-SMOKE | Synthetic oracle / NDV plumbing | 2026-07-21 | implemented | Oracle dominates fixed baselines by construction; not empirical evidence |
| EXP-001A | Learned cost-aware VoI, synthetic temporal cohorts | 2026-07-21 | completed — conditional | Main +0.00277 NDV passes; independent seed and low-cost robustness fail |
| EXP-001 | Learned cost-aware VoI on locked PiT cohort | | blocked by label/data gates | |
