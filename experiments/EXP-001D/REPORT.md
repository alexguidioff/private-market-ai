# EXP-001D — Company-Disjoint 2021→2022 Baseline Transport

**Status:** complete assumption-bound development/validation baseline.  
**Scope:** transport of prior, anchor-only and anchor+SEC-history models. This is not an acquisition
experiment, not a VoI test and not an evaluation of the locked 2023 cohort.

## Design
- Company-disjoint development: 2021, n=2,369.
- Temporal validation: 2022, n=2,243.
- Locked test: 2023, n=914; outcomes remained masked and were not accessed.
- Target: later non-amendment Form D notice in the declared 18-month window (weak proxy).
- Models: development prior, anchor-only logistic and anchor+SEC-history logistic.
- Regularization selected by five-fold stratified CV entirely within 2021; both models selected
  `C=0.01`. No 2022 tuning was performed.
- Utility matrices are assumptions copied from EXP-001C; no buyer elicitation is claimed.

## 2022 predictive transport
| Model | ROC-AUC | Average precision | Log loss | Brier |
|---|---:|---:|---:|---:|
| Development prior | 0.5000 | 0.1922 | 0.4925 | 0.1563 |
| Anchor only | 0.5930 | 0.2502 | 0.4840 | 0.1537 |
| Anchor + SEC history | **0.6551** | **0.3214** | **0.4681** | **0.1482** |

SEC history transports as useful baseline information across company-disjoint years. This supports
including it in the efficient initial state; it does not revive the failed selective-acquisition claim
from EXP-001C.

## Assumption-bound decision utility
Compared with anchor-only, anchor+history changes mean utility by:

| Scenario | Delta | 95% paired bootstrap CI | Interpretation |
|---|---:|---:|---|
| Balanced | +0.04191 | [0.02317, 0.05996] | positive under this assumed matrix |
| False-positive averse | +0.00256 | [-0.00256, 0.00769] | inconclusive |
| Opportunity averse | +0.00368 | [-0.00011, 0.00769] | inconclusive |

Against the development-prior policy, the full model is positive under balanced and
opportunity-averse assumptions, but these are not buyer-elicited economics. Mean utility remains
negative in all three full-model scenarios; relative improvement must not be described as positive
business value.

## Verdict
**Temporal baseline pass; VoI claim not tested.** SEC history is justified as part of the baseline
state for subsequent method development. Decision-value conclusions remain utility-dependent, which
reinforces—rather than removes—the later need for buyer elicitation.

Do not tune on 2022 after this report. Develop any new acquisition policy on 2021 using this frozen
baseline recipe, use 2022 only for declared validation, and keep the 914-case 2023 vault closed until
the full protocol is frozen.

## Reproducibility
- Results SHA-256: `dffc2ff84bfde9e7d4671fd9e8928b0481c577805d2d1dd7be544e718e3e982c`
- Script/config/input hashes are recorded in `results.json`.
- A deterministic rerun produced byte-identical results.