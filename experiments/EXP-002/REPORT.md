# EXP-002 — Tail lift of point-in-time SEC information

**Date:** 2026-07-28
**Status:** complete; 2023 locked test not touched
**Scripts:** `code/tail_lift.py`, `code/exp002_tail_lift.py`
**Artefacts:** `config.json`, `results.json`

## Question

EXP-001D established that issuer filing history transports as baseline
information, raising ROC-AUC from 0.5930 to 0.6551. An AUC of 0.65 reads as
modest, and modest is how it has been reported.

But ROC-AUC averages over all pairs, and an analyst does not act on the median
company. They act on the slice they have capacity to examine. This experiment
therefore measures a different quantity:

```text
lift(q) = P(outcome = 1 | feature in top q) / P(outcome = 1)
```

Under independence, lift(q) = 1 at every q. The question is whether information
that looks unremarkable on average is sharply informative at the extreme, and
whether that sharpness survives on a company-disjoint later cohort.

## Design

| Element | Value |
|---|---|
| Development cohort | issuers with 2021 anchor, one row each: **4,059** |
| Validation cohort | issuers with 2022 anchor, CIK-disjoint: **2,947** |
| Outcome | subsequent non-amendment Form D notice within 18 months |
| Base rate | 27.1% development, 21.2% validation |
| Removed from validation | 1,018 rows whose issuer also appears in 2021 |
| Thresholds | q ∈ {0.30, 0.20, 0.10, 0.05} |
| Uncertainty | bootstrap interval on the lift, 500 resamples, seed 20260728 |
| Multiplicity | Benjamini-Hochberg across all 60 feature-by-threshold tests |
| Locked 2023 test | **not accessed** |

Every lift is reported next to the feature's ROC-AUC, so the gap between average
and tail behaviour is visible rather than asserted.

## A correction made during execution

The first run split the cohort by anchor year and reported a lift of 2.15x that
transported. The disjointness assertion then failed: **846 CIKs appeared in both
years**, because an issuer can file in 2021 and again in 2022. The same company's
filing history was present on both sides of the split, which inflates any
transport claim. 1,018 validation rows were affected.

Note also that the validation base rate falls to 21.2% after the correction,
against 27.1% in development. Removing repeat filers removes issuers that are
disproportionately likely to file again, so the two cohorts are not
distributionally identical. Lift is a ratio to each cohort's own base rate, which
absorbs the level difference, but the cohorts should not be treated as exchangeable.

Issuers present in 2021 were removed from validation, and each cohort was reduced
to one row per issuer. Removing them from development instead would have
discarded exactly the richer-history cases that carry the signal, biasing the
scan; removing them from validation costs sample but keeps the test honest.

After the correction the transported lift is **1.45x, not 2.15x**. The original
figure is not reported as a result.

## Development scan (2021)

Surviving FDR correction across 60 tests:

| Feature | AUC | lift q=0.30 | lift q=0.10 | lift q=0.05 | monotone |
|---|---:|---:|---:|---:|:--:|
| known_filing_count | 0.61 | 1.29x | 1.55x | **1.73x** | yes |
| known_new_notice_count | 0.61 | 1.30x | 1.51x | **1.66x** | yes |
| known_equity_filing_count | 0.58 | 1.24x | 1.44x | **1.55x** | yes |
| known_amendment_count | 0.56 | 1.21x | 1.41x | **1.53x** | yes |
| prior_notice_count | 0.59 | 1.28x | 1.43x | **1.53x** | yes |
| issuer_observed_age_days | 0.57 | 1.17x | 1.13x | 1.24x | no |

Flagged as tail-only signals — weak on average, enriched at the extreme:
`prior_notice_count`, `known_amendment_count`, `known_equity_filing_count`.

Monotonicity matters more than a single significant threshold. A genuine tail
effect should strengthen as the slice narrows; one lucky slice should not. Five
features show monotone lift across all four thresholds.

### Features that carry no tail signal

Deal-size terms of the anchor filing are uninformative or inverted:

| Feature | AUC | lift q=0.05 |
|---|---:|---:|
| total_offering_amount | 0.50 | 0.58x |
| total_amount_sold | 0.50 | 0.56x |
| latest_known_amount_sold | 0.52 | 0.56x |
| investor_count | 0.52 | 1.04x |
| filing_lag_days | 0.47 | 0.82x |

The inversion is interpretable rather than noise: issuers raising the largest
amounts in a single offering are *less* likely to file again soon, while issuers
with a long history of repeated filings keep filing. Direction is consistent
across thresholds and across both cohorts.

## Transport to the company-disjoint 2022 cohort (q = 0.05)

| Feature | dev lift | test lift | test 95% CI | transports |
|---|---:|---:|---|:--:|
| known_amendment_count | 1.53x | **1.77x** | [1.36, 2.15] | yes |
| known_filing_count | 1.73x | **1.45x** | [1.18, 1.92] | yes |
| known_new_notice_count | 1.66x | **1.45x** | [1.12, 1.89] | yes |
| known_equity_filing_count | 1.55x | **1.45x** | [1.12, 1.84] | yes |
| prior_notice_count | 1.53x | 1.32x | [0.99, 1.76] | no — CI touches 1.0 |
| issuer_observed_age_days | 1.24x | 1.19x | [0.91, 1.57] | no |
| total_offering_amount | 0.58x | 1.00x | [0.67, 1.33] | no |

Four features transport with intervals excluding 1.0. The strongest,
`known_amendment_count`, is *higher* out of sample; the others attenuate, which
is the expected direction when a threshold was chosen on development data.

## Findings

1. **Average metrics understate tail-concentrated information.** The same block
   that yields ROC-AUC 0.61 concentrates a 1.45x enrichment in its top 5%. Both
   numbers describe the same data; they answer different questions.

2. **The signal is issuer history, not deal size.** Counts of prior filings,
   amendments and equity filings carry the tail lift. Offering and sale amounts
   carry none, and invert in the development cohort.

3. **The effect transports across a company-disjoint boundary**, at reduced
   magnitude, for four of fifteen candidate features.

4. **Monotonicity strengthens the claim.** Five features show lift rising as the
   slice narrows, which is harder to produce by chance than one significant cell.

## Relation to EXP-001C

This does not contradict EXP-001C, and must not be read as rescuing it.

```text
EXP-001C:  a learned selective policy paying to acquire SEC history
           passed 0 of 15 declared utility-by-cost gates
           -> do not pay selectively for this block

EXP-002:   the same block, already present, concentrates 1.45x lift in its
           top 5% and transports to a disjoint cohort
           -> the block belongs in the baseline state
```

§8.2 of the working paper drew this distinction between baseline information and
acquisition actions. EXP-002 quantifies the baseline side with a metric matched
to the decision, where EXP-001D used an average one. Neither result licenses a
claim that cost-aware VoI improves real venture decisions.

## Threats to validity

**Construct.** The outcome remains a subsequent non-amendment Form D notice: a
weak regulatory event, not a priced round, not Series A, not company success. A
lift of 1.45x is a lift on *that* event.

**Mechanical component.** An issuer that has filed repeatedly is, by
construction, an issuer that files. Part of the lift reflects persistence of
filing behaviour rather than any economic property of the company. This
experiment does not separate the two, and the effect should be assumed largely
mechanical until a design distinguishes them.

**Selection.** The cohort is technology-related primary Form D issuers, not a
verified venture-backed population.

**Threshold selection.** Thresholds were declared before the scan, but the
transport check reports q = 0.05 because that is where development lift peaked.
The attenuation from 1.73x to 1.45x is consistent with mild selection.

**Multiplicity.** FDR control is applied, but 60 tests on 15 correlated features
leaves the effective number of independent tests unknown.

**No causal claim.** These are associations in observational data.

**One-time use.** The 2022 cohort has now been used for this comparison. Reusing
it for further threshold selection would invalidate its role.

## What would strengthen this

1. Separate the mechanical component: condition on filing count and ask whether
   any feature adds tail lift *within* history strata.
2. A qualitatively different information block, per the §9 future protocol.
3. Elicited buyer utilities, so lift can be converted into decision value rather
   than left as an enrichment ratio.
4. A stronger outcome than the weak proxy, requiring the human adjudication in
   `datasets/P1_OPEN_SOURCE_LABEL_PLAN.md`.

## Reproduction

```bash
python code/exp002_tail_lift.py
```

Deterministic given the seed. Artefacts in `experiments/EXP-002/`.
