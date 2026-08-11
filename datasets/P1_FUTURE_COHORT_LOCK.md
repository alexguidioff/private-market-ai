# P1 Future Temporal Cohort Lock

**Prepared:** 2026-07-21 · **Status:** process-locked; outcomes not inspected

## Purpose
This cohort provides a company-disjoint temporal evaluation after repeated inspection of the 2020
split. It remains a weak Form-D-outcome benchmark, not a startup-success or VC-round benchmark.

## Construction
- Official SEC Form D archives: 2008 Q1–2026 Q1; 2026 Q2 was not yet available.
- Candidate anchors: 2021–2023 technology-related primary issuers.
- Decision time: filing availability plus 12 months.
- Label horizon: following 18 months.
- Conservative label-coverage cutoff: 2025-12-31, three months before the latest archive boundary, to
  accommodate late-quarter records that can appear in the next SEC release.
- Incomplete windows: 1,704 panel rows censored and excluded from model-ready data.
- Every CIK present in the 2016–2020 model-ready cohort is excluded: 2,568 candidate rows removed.

## Frozen non-outcome counts
- Independent model-ready issuers: **5,526**.
- Development 2021: **2,369**.
- Validation 2022: **2,243**.
- Locked test 2023: **914**.
- CIK overlap with the historical model-ready cohort: **0**.

## Outcome isolation
The 914 test labels exist only in local, git-ignored `p1_locked_test_labels.csv`. They are null in the
model-ready file, enriched panel, source cohort CSV and SQLite cohort table. Test features are stored
separately. The pipeline refuses an unblinded future run and preserves an existing vault when its
keys match; key drift raises an error.

## Hashes
- Locked labels vault: `5be4e514a16acd402dff2c2faa16a58a412eb499983e3e481b850102bce15c08`
- Locked test features: `f1293f8d33c4b45742539c1d0653ae7a95d545aabfac7f8138664597046fd7ca`
- Builder script: `7739ca47e8e590d1c2fb9981fabd6c6e36a1227ceb3695777f0b1b513b88977c`
- Enrichment/lock script: `92255ad4f34c49df214b1fcbdf4fa611c44aeb99e1e49bd0460ecb715b88133b`

## Permitted work before test opening
Development and model selection may use 2021 and 2022 only. Utility and cost must remain a complete,
predeclared assumption grid while buyer interviews are unavailable. The 2023 vault must remain closed
until source, entity-resolution, feature set, policies, utility/cost grid, sensitivity analyses,
success criterion and analysis-script hash are frozen.

Without buyer elicitation, a later test can establish robustness across declared utility assumptions;
it cannot establish that those utilities represent real VC economics or support product-market-fit
claims.