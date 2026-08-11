# Status Memo — P0 execution baseline

**Updated:** 2026-07-22 · **Level:** NORTH STAR · **Canonical sequence:** `../programme.yaml`

**Project direction:** `PROJECT_DIRECTION.md` explains what has been built, the next empirical gates,
and why the current MVP is a research/evidence MVP rather than a fundraising-ready startup product.

## Mission and active claim
We build the scientific foundations of **Decision Intelligence for Private Capital Markets**.
The active flagship is **P1: Cost-Aware Value of Information for VC Diligence**. Representation,
ontology and the synthetic harness are enabling assets, not standalone headline papers.

## Evidence maturity
| Item | State | Evidence | Next gate |
|---|---|---|---|
| Foundational WI2026 study | M4-accepted | `../papers/README.md` | publication/replication |
| P1 VoI | M2 real one-block falsified + synthetic conditional | `../experiments/EXP-001C/REPORT.md`; `../experiments/EXP-001A/REPORT.md` | buyer utility/cost elicitation + PiT-safe external block/new test cohort |
| P2 Decision Quality | M1 | `Research_Agenda.md` | operational label protocol |
| P3 Human-AI committee | M1 | `Research_Agenda.md` | subjects/partner/protocol |
| Product wedge | B0 | `product/P1_Buyer_Discovery.md` | 10 qualified interviews |

## P0 deliverables
- [x] Canonical programme and maturity manifest (`../programme.yaml`).
- [x] Formal state/action/utility/cost/NDV definition (`Theory.md`).
- [x] Narrow provisional cohort and preregisterable protocol.
- [x] PiT data contract and leakage rules.
- [x] Executable decision-object schema separated from prediction/belief.
- [x] Baselines, primary metric and falsification gate.
- [x] Dependency-free synthetic ground-truth smoke test.
- [x] Learned-policy EXP-001A with temporal split, paired world bootstrap, oracle and cost sensitivity.
  Verdict: conditional—main/high-cost pass, independent-seed/low-cost fail.
- [x] Evidence register and narrow buyer-discovery script.
- [x] SEC source access, all 62 quarters, mixed date formats, coverage, label windows, privacy
  minimization and class balance audited (`../datasets/P1_DATASET_CARD.md`).
- [x] Run an AI-assisted double-review pilot on 20 issuers (`../datasets/P1_GOLD_PILOT_REPORT.md`):
  75% exact agreement. Project-owner acceptance yields Layer-A labels of 9 positive, 4
  no-public-evidence and 7 unknown; original disagreements remain preserved.
- [x] Accept the pilot for method development without independent human source review. It is not a
  publication-grade human gold set; Layer B and extension to the remaining 180 remain open.
- [x] Complete real-data EXP-001B (`../experiments/EXP-001B/REPORT.md`): logistic temporal baseline
  improves weak-proxy test ROC-AUC from 0.50 to 0.6485 and log loss from 0.6041 to 0.5828. Utility
  gain is positive only under the balanced assumed matrix; asymmetric scenarios are inconclusive.
- [x] Test SEC issuer history as the first acquisition block (`../experiments/EXP-001C/REPORT.md`):
  predictive lift is real but small (test ROC-AUC 0.6261 → 0.6485); the cost-aware policy beats no
  strongest baseline in 0/15 utility×cost scenarios. Exploratory VoI gate fails.
- [x] Audit SBIR/STTR as a qualitatively different candidate block on development/validation only
  (`../datasets/P1_SBIR_BLOCK_AUDIT.md`): 622/10,550 exact name+state candidates (5.90%), but the
  public-availability timestamp is not defensible from the current backfilled dump. Data gate fails;
  no VoI experiment was run and 2020 remained excluded.
- [x] Audit USPTO/PatentsView operational access (`../datasets/P1_USPTO_BLOCK_AUDIT.md`):
  publication semantics and schemas are suitable, but ODP product metadata/files require a personal
  API key and returned 401/403 anonymously. No credentials, data extraction or entity matching used.
- [x] Prepare a company-disjoint future temporal cohort (`../datasets/P1_FUTURE_COHORT_LOCK.md`):
  2,369 development issuers (2021), 2,243 validation issuers (2022) and 914 process-locked test
  issuers (2023), with zero CIK overlap against the historical cohort. Outcome copies are masked
  outside a hashed local vault; 1,704 incomplete panel windows are censored.
- [x] Complete EXP-001D (`../experiments/EXP-001D/REPORT.md`) without opening 2023: select
  regularization inside 2021 and evaluate temporal transport once on 2022. Anchor+SEC-history reaches
  ROC-AUC 0.6551 and log loss 0.4681; its utility gain over anchor-only is robust only under the
  balanced assumed matrix. This freezes SEC history into the baseline state; it is not a VoI test.
- [x] Complete the internal P1 evidence draft (`../papers/P1_Cost_Aware_VoI_Working_Paper.md`):
  integrate EXP-001A/B/C/D, source-gate failures, threats to validity, future locked protocol,
  reproducibility and ethics. The 2023 outcomes remain closed; formal literature review and
  venue-specific submission work remain open.
- [x] Defer buyer interviews until PhD or institutional-partner access is available. Continue
  scientific development with a complete preregistered utility/cost assumption grid; do not claim
  that those scenarios represent buyer economics.
- [x] Audit SEC Form C as a second-block candidate on the future development/validation cohort
  (`../datasets/P1_FORMC_BLOCK_AUDIT.md`): exact CIK and filing-date semantics pass, but only 52/2,369
  development issuers (2.20%) and 57/2,243 validation issuers (2.54%) have a Form C known by decision
  time. The 100-case development coverage gate fails; no outcome model or VoI policy was run.
- [ ] Identify a qualitatively different block with safe identity/PiT semantics. SBIR fails the
  temporal gate, Form C fails coverage, and USPTO/PatentsView is access-gated pending a
  project-owner-provisioned account.
- [ ] Before opening the 2023 vault, freeze source, entity resolution, features, policies,
  utility/cost grid, sensitivities, success criterion and analysis-script hash.
- [ ] Conduct buyer utility/cost elicitation and 10 qualified interviews when partner access exists;
  this remains required for buyer-realistic and commercial claims, not for assumption-bound research.

## Active decision
The implemented v1 population is US technology-related primary Form D issuers, not a verified
software-startup or seed cohort. Decision time is 12 months after filing availability; the weak
outcome is a later non-amendment Form D within 18 months. The model-ready file has 12,381 unique
issuers (8,455 train / 2,095 validation / 1,831 test) and point-in-time issuer-history features.
This supports reproducible method development; VC-specific claims require gold-set validation and
at least one defensible external information block.

## Do not build yet
No GNN, foundation model, agentic DD, portfolio VoI or private-market OS work before P1 passes its
data, utility and evaluation gates. See `P0_EXECUTION_PLAN.md` for remaining actions.
