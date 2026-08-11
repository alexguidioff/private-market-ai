# Code

Clean, shareable code and pipeline documentation for the research program.

> **No proprietary data.** Commit only code, synthetic/sample data, and documentation.

## Suggested layout (as the project grows)
```
code/
├── data/           # loaders, connectors (no raw proprietary data)
├── features/       # feature engineering
├── models/         # training, evaluation
├── pipeline/       # end-to-end orchestration
├── notebooks/      # exploration
└── README.md
```

## Pipeline (thesis baseline)
```
Data ingestion (PitchBook + GEM)
  → Cleaning & feature engineering
    → Model training (Random Forest, benchmarks)
      → Temporal validation
        → Explainability (SHAP, feature importance)
          → Results & reporting
```

## P0 executable vertical slice
- `p0_synthetic_voi.py` is a dependency-free smoke test for the NDV metric and policy interface.
- Run once with `python code\p0_synthetic_voi.py` from the repository root.
- It uses an exact synthetic oracle; it does **not** establish learned-policy performance or market realism.
- P1 will add estimated policies only after the data, utility and protocol gates pass.

## P1 learned-policy benchmark
- `exp001a.py` implements temporal train/validation/test splits, learned belief/signal models,
  preregistered baselines, a hidden-DGP oracle and paired world-level bootstrap inference.
- Exact results and negative replications are frozen in `../experiments/EXP-001A/REPORT.md`.
- Environment used: Python 3.13.2, NumPy 2.4.5, scikit-learn 1.8.0.
- The result is synthetic and conditional; it is not evidence of private-market performance.

## Public GitHub repo checklist
- [ ] README with problem, dataset description, method, results
- [ ] Reproducible environment (`requirements.txt` / `pyproject.toml`)
- [x] No secrets, no licensed data in the P0 harness
- [ ] Clear license
