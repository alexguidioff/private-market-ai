# EXP-001A — Learned Cost-Aware VoI on Synthetic Temporal Cohorts

**Date:** 2026-07-21 · **Status:** completed · **Verdict:** CONDITIONAL / robustness gate failed

## Question
Can a policy trained only on past synthetic cohorts choose whether and which information block to
acquire, and improve test Net Decision Value (NDV) over fixed non-VoI baselines?

## Design
- 100 randomized worlds in the main run; 250 companies per year/world.
- Train 2016–2018, model selection 2019, locked test 2020.
- Four binary acquisition blocks with hidden signal processes and heterogeneous costs.
- Learned logistic models estimate initial belief, signal availability and post-acquisition belief.
- Baselines: none, random, cheapest, most predictive and entropy reduction.
- Oracle uses the hidden DGP; it is an upper bound, not the proposed method.
- Primary inference: paired bootstrap over worlds, not individual companies.

## Results
| Run | Cost scale | Worlds | Learned NDV | Best baseline | Delta | 95% CI | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| Main seed 20260721 | 1.0 | 100 | 0.133006 | none 0.130234 | +0.002772 | [0.000133, 0.006112] | pass |
| Independent seed 20260722 | 1.0 | 50 | 0.138855 | none 0.138228 | +0.000627 | [-0.001914, 0.003176] | fail |
| Low cost | 0.5 | 50 | 0.162110 | none 0.158428 | +0.003682 | [-0.001263, 0.008690] | fail |
| High cost | 2.0 | 50 | 0.161387 | none 0.158428 | +0.002959 | [0.000424, 0.005781] | pass |

Main-run oracle NDV was 0.138856 versus learned 0.133006. The learned policy acquired information
for 15.8% of test decisions; the oracle acquired for 13.4%.

## Interpretation
The mechanism works in principle and correctly abstains more as information becomes expensive. But
the improvement is small and does not replicate across every preregistered robustness condition.
Therefore EXP-001A does **not** establish the P1 claim. It supports continued investigation while
rejecting any statement that cost-aware VoI has already been demonstrated.

The strongest baseline is consistently `none`. This is substantive: information acquisition must
clear a high value threshold; always acquiring the cheapest, most predictive, or entropy-reducing
block destroys NDV after costs.

## Decision
- Evidence maturity moves from M1 design to **M2-synthetic-conditional**, not M3 empirical.
- Do not tune on these test worlds. Freeze this result and preserve the negative replications.
- Next experiment is EXP-001B on a new world family with correlated/redundant signals, cost
  misspecification, private-information overlap and explicit distribution shift.
- Real-data EXP-001 remains blocked by the outcome-label and PiT source gates.
