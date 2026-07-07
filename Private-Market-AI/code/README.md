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

## Public GitHub repo checklist
- [ ] README with problem, dataset description, method, results
- [ ] Reproducible environment (`requirements.txt` / `pyproject.toml`)
- [ ] No secrets, no licensed data
- [ ] Clear license
