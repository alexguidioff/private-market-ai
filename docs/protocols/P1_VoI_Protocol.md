# P1 Protocol — Cost-Aware Value of Information

**Version:** 0.1-P0 · **Status:** design freeze candidate · **Date:** 2026-07-21
**Authority:** `programme.yaml` defines naming and sequence; this file defines the P1 experiment.

## 1. Claim and unit of analysis
P1 tests whether a cost-aware information-acquisition policy improves **Net Decision Value (NDV)**
over simple non-VoI policies. The unit is one company at one fixed decision time; repeated rows or
later snapshots of the same company cannot cross train/test boundaries.

## 2. Implemented real-data cohort v1
- US primary issuers with a non-amendment Form D anchor in 2016–2020.
- Technology-related categories: Other Technology, Computers, Telecommunications, Business Services.
- Pooled funds and business-combination offerings are excluded.
- This is not yet a verified software/startup/seed/venture-backed population.
- Public availability is `filing_time`; decision time `t` is exactly 12 months later.
- Observed weak label: same CIK files a later non-amendment Form D in `(t, t + 18 months]`.
- The label is a subsequent exempt-offering notice, not priced institutional Series A or success.
- Model-ready data use the first eligible anchor per CIK: train 2016–2018, validation 2019, test 2020.

The complete SEC archive 2008 Q1–2023 Q2 supplies pre-anchor history and fully observed label windows.
The core passed access, completeness, temporal and leakage checks; see `../../datasets/P1_DATASET_CARD.md`.
A manually reviewed entity/round gold set is still required before making VC-specific claims. Its
open-only annotation protocol, schema and deterministic 200-issuer review queue are defined in
`../../datasets/P1_OPEN_SOURCE_LABEL_PLAN.md`; balancing uses the weak proxy for sampling only and
reviewers remain blinded to it.

## 3. Formal decision problem
Let `theta` be the latent follow-on-ready state, `I_t` the observable/public information state,
`D={continue_diligence, stop}`, and `A` the set of information-acquisition actions plus `none`.
For action `a`, observation `X_a` arrives with total cost `C(a)`.

`NDV(a|I_t) = E[max_d E[U(d,theta)|I_t,X_a] | I_t] - C(a)`.

`NetVoI(a|I_t) = NDV(a|I_t) - max_d E[U(d,theta)|I_t]`.
The policy chooses the positive-NetVoI action with greatest expected NDV, otherwise `none`.

## 4. Utility freeze before outcome access
The payoff matrix must be elicited from target buyers or reported as a sensitivity grid. It includes
analyst cost, direct spend, delay cost, false-negative opportunity cost and false-positive diligence
cost. No utility may be tuned on the held-out test outcomes.
## 5. Information actions and cost
The efficient baseline state now includes legally reproducible anchor fields and SEC issuer history
available at `t`; EXP-001C found that history predictive but did not establish selective-acquisition
value. The next action must add qualitatively different information. SBIR/STTR awards were audited on
2016–2019 only: exact company-name+state matching found 622/10,550 candidates, but the current dump
lacks a defensible first-publication timestamp, so the block failed the data gate and was not tested.
USPTO/PatentsView pre-grant publications remain conditional on ODP access/version freeze and audited
assignee resolution. SEC Form C passes exact-CIK identity and filing-date availability checks, but
only 52/2,369 development issuers have a disclosure known by decision time; its predeclared coverage
gate fails and it must not be modelled. OpenAlex remains blocked until reviewed founder-author
identity exists.
`C(a)` combines direct spend, loaded analyst time, delay and strategic/opportunity cost. Acquisition
can change the deal process; sensitivity analysis must include passive-query and intervention costs.

## 6. Splits and leakage controls
- Development: seed cohorts 2016–2018; validation: 2019; locked test: 2020.
- If sample size is insufficient, change years before inspecting test results and version the protocol.
- Group by canonical company and related filings; fit entity resolution and preprocessing on development.
- Enforce `available_time <= decision_time`; labels and post-cutoff revisions remain isolated.
- Report censoring and competing events rather than treating every non-follow-on as failure.

## 7. Preregistered baselines
1. `none`: decide from the initial information state.
2. `random`: acquire one eligible block uniformly.
3. `cheapest`: acquire the lowest total-cost block.
4. `most_predictive`: acquire the block with highest validation-only predictive lift, ignoring cost.
5. `uncertainty_reduction`: maximize expected entropy reduction, ignoring utility and cost.
6. `cost_aware_voi`: proposed learned policy.
7. `oracle`: synthetic data only; upper bound with access to the true DGP.

## 8. Outcomes and metrics
Primary: mean per-deal NDV of the final decision minus acquisition cost. Secondary: regret to the
oracle, acquisition ranking agreement, decision accuracy/utility, total cost, calibration, abstention,
subgroup/regime results and bootstrap confidence intervals. Predictive AUC is diagnostic, not the
success criterion.

## 9. Synthetic ground-truth test
The P0 harness samples many worlds with hidden signal accuracies and costs. It verifies metric and
policy plumbing by showing that the cost-aware **oracle** weakly dominates fixed baselines per world.
This is not evidence that a learned policy works or that the simulator resembles VC markets. P1 must
replace oracle quantities with development-data estimates and evaluate once on the locked test set.

## 10. Success, falsification and fallback
P1 passes only if `cost_aware_voi` exceeds every non-VoI baseline on mean test NDV, its uncertainty
interval excludes zero for the strongest baseline comparison, and the conclusion survives the
preregistered cost/private-information sensitivity ranges. Otherwise the flagship claim **pivots**;
report prediction/calibration findings without relabelling them as VoI success.

## 12. EXP-001B real-data baseline

EXP-001B freezes a reproducible predictive and zero-acquisition decision baseline before any external
information block is added. It uses the implemented feature allowlist, train 2016–2018, validation
2019 for logistic regularization selection by log loss, and test 2020 once. It reports ROC-AUC and
average precision only as diagnostics, proper scoring rules (log loss and Brier), calibration,
zero-cost utility over a declared assumption grid and paired bootstrap deltas versus a prior-only
dummy.

This experiment is **not** the P1 VoI test: there is no acquisition action or acquisition cost yet.
The utility grid in `../../experiments/EXP-001B/config.json` is exploratory, not buyer-elicited. The
owner-accepted 20-case Layer-A pilot is used only for sensitivity bounds, never training, prevalence
or untouched gold-test claims. Full results: `../../experiments/EXP-001B/REPORT.md`.

## 13. EXP-001C first real acquisition block

The first exploratory action treats retrieval/analysis of point-in-time SEC issuer history as one
block beyond anchor-only fields. It improves test prediction modestly (ROC-AUC 0.6261 to 0.6485), but
the learned cost-aware policy beats the strongest non-VoI baseline in **0 of 15** declared
utility-by-cost scenarios. The best point estimate has a bootstrap interval crossing zero.

This is a falsification for the tested block, representation, meta-policy and assumed grids; do not
tune costs post hoc. OpenAlex founder research is blocked because the privacy-minimized cohort lacks
reviewed founder identities. See `../../experiments/EXP-001C/REPORT.md`.

## 14. SBIR candidate-block audit

SBIR/STTR awards were audited only on the 2016–2019 development/validation cohort. Conservative exact
normalized company-name plus state matching produced 622 candidate matches among 10,550 issuers
(5.90%), all mapping to one source firm identifier under that rule. Of these, 350 had a proposal-award
date no later than decision time.

The block failed the data gate because proposal-award and applicant-notification dates do not prove
when a record first became publicly observable, while the current complete dump may contain later
backfill or corrections. No outcome model, utility grid or VoI policy was run; 2020 remained excluded.
See `../../datasets/P1_SBIR_BLOCK_AUDIT.md`.

## 15. Future company-disjoint temporal cohort

A separate evaluation cohort is prepared from 2021–2023 anchors after excluding every CIK in the
historical model-ready cohort. Complete-window, independent counts are 2,369 development issuers in
2021, 2,243 validation issuers in 2022 and 914 process-locked test issuers in 2023. A three-month
late-filing buffer sets label coverage end to 2025-12-31; incomplete windows are censored.

The 2023 outcomes exist only in a hashed local vault and are null in operational copies. Development
may continue without interviews using a complete predeclared assumption grid on 2021/2022. This can
test methodological robustness but not whether utility parameters represent real VC economics. See
`../../datasets/P1_FUTURE_COHORT_LOCK.md`.

## 16. Gates before opening the 2023 vault
- Data gate: rights, coverage, PiT availability, entity-resolution audit and usable outcome balance.
- Utility gate: freeze a complete bounded assumption grid; buyer-elicited scenarios are deferred and
  must remain explicitly absent from the claim.
- Protocol gate: immutable features, policies, sensitivity analyses, success criterion and script hash.
- Novel-evaluation gate: no outcome access, tuning or model selection on the 914-case vault.
- Ethics/governance gate: no prohibited collection; personal data minimized and access controlled.

## 17. EXP-001D future temporal baseline

EXP-001D selected logistic regularization by five-fold CV within 2021 and evaluated once on 2022,
without accessing 2023 outcomes. Anchor+SEC-history improves over anchor-only (2022 ROC-AUC 0.6551 vs
0.5930; log loss 0.4681 vs 0.4840). Utility improvement is robust only under the balanced assumed
matrix and remains inconclusive under both asymmetric matrices. This freezes SEC history into the
efficient baseline state; it is not an acquisition or VoI test. See
`../../experiments/EXP-001D/REPORT.md`.

No further tuning on 2022 is permitted for this baseline recipe. A new block may be developed on 2021
and evaluated once on 2022 before the complete protocol is frozen for the still-closed 2023 vault.
Buyer elicitation and 10 qualified interviews remain a later gate for external validity and commercial
claims; they are not required for assumption-bound method development or the current working paper.
