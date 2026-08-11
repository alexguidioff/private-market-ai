# P0 Execution Plan — from programme to testable P1

**Started:** 2026-07-21 · **Authority:** `programme.yaml` · **Owner:** Alessandro Guidi

P0 here means the execution phase, not the completed foundational study (`F0`). Its exit condition is
a frozen, auditable design ready for data acquisition and a learned-policy experiment.

| Workstream | Deliverable | Status | Exit evidence |
|---|---|---|---|
| programme coherence | canonical sequence and maturity | done | `programme.yaml` |
| formal problem | state, action, utility, cost, NDV | done | `Theory.md`; P1 protocol |
| narrow cohort | population, time, decision and outcome | SEC v1 implemented; strong-label scope open | `datasets/P1_DATASET_CARD.md` |
| PiT contract | timestamps, leakage and entity resolution | SEC v1 passed; external matching open | `datasets/P1_DATA_CONTRACT.md` |
| object model | belief/acquisition/decision separation | done-design | `schemas/p1-decision.schema.json` |
| evaluation | baselines, metrics and falsification | done-design | P1 protocol §§7–10 |
| synthetic test | deterministic ground-truth plumbing | done | `code/p0_synthetic_voi.py` |
| evidence discipline | M/B stages and unknowns | done | `docs/EVIDENCE_REGISTER.md` |
| buyer discovery | one buyer/workflow/interview gate | done-design | `docs/product/P1_Buyer_Discovery.md` |
| legacy synchronization | remove conflicting active roadmap | in progress | README/status/F11/roadmap aligned |

## Remaining P0 gates before EXP-001
1. **Data-access gate:** audit SEC Form D coverage and candidate public sources on a small sample;
   document rights, timestamps, class balance, censoring and source snapshots.
2. **Cohort gate:** accept or version the provisional cohort without inspecting locked outcomes.
3. **Utility gate:** elicit cost/payoff ranges from qualified buyers or freeze transparent bounds.
4. **Protocol freeze:** hash the analysis plan, split and policy definitions before test execution.
5. **Buyer gate:** run 10 qualified interviews; fewer than 5 top-three rankings means pivot.

P0 does not claim the policy works. It defines what evidence would demonstrate or falsify that claim.
