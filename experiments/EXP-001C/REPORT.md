# EXP-001C — Cost-Aware Acquisition of SEC Issuer History

**Status:** complete exploratory one-block experiment; flagship gate not passed.  
**Scope:** decide whether to acquire analysis of the issuer's prior/intervening SEC Form D history.
Costs are normalized assumptions pending buyer elicitation.

## Why this block

OpenAlex was rejected as the first block because the privacy-minimized cohort has issuer identities
but no reviewed founder identities; name-only founder/author or company/institution matching would be
unreliable. SEC issuer history is open, already point-in-time audited, and naturally separable from the
anchor filing.

- Base state: 7 categorical and 7 numeric anchor-filing fields.
- Acquired block: 15 issuer-history fields available by `decision_time`.
- Train: 2016–2018; validation: 2019; locked temporal test: 2020.
- Base and enriched logistic models selected by validation log loss.
- A Ridge meta-policy learns realized acquisition gain from five-fold out-of-fold train predictions,
  using only base-state numeric fields and base uncertainty at decision time.
- Baselines: none, random, cheapest/acquire-all, most-predictive/acquire-all when validation lift is
  positive, and expected uncertainty reduction.
- Evaluation: three utility scenarios × five normalized costs; 1,000 paired bootstrap draws.

## Predictive value of the block

| Model | Validation log loss | Test ROC-AUC | Test AP | Test log loss | Test Brier |
|---|---:|---:|---:|---:|---:|
| Anchor only | 0.55267 | 0.62607 | 0.38589 | 0.58465 | 0.19916 |
| Anchor + SEC history | **0.53516** | **0.64849** | **0.39120** | **0.58278** | **0.19900** |

The block adds real but small predictive information. This is necessary but not sufficient for VoI.

## Cost-aware policy results

No utility×cost scenario passes the exploratory gate against the strongest non-VoI baseline.

| Utility | Cost | Acquire rate | Strongest baseline | NDV delta | 95% CI |
|---|---:|---:|---|---:|---:|
| Balanced | 0.000 | 94.27% | uncertainty reduction | -0.00164 | [-0.00464, 0.00109] |
| Balanced | 0.010 | 89.90% | uncertainty reduction | -0.00181 | [-0.00431, 0.00020] |
| Balanced | 0.025 | 75.04% | uncertainty reduction | +0.00302 | [-0.00025, 0.00639] |
| Balanced | 0.050 | 18.73% | none | -0.00363 | [-0.01434, 0.00773] |
| Balanced | 0.100 | 0.00% | none | 0.00000 | [0.00000, 0.00000] |
| False-positive averse | 0.010 | 30.58% | none | +0.00281 | [-0.00936, 0.01509] |
| Opportunity averse | 0.025 | 8.25% | none | **+0.00340** | [-0.00167, 0.00906] |

The last row is the best point estimate, but its interval crosses zero. At higher opportunity-averse
costs the cost-aware policy is significantly worse than acquiring nothing. Remaining rows are in
`results.json`; none pass.

## Verdict

**SEC-history block: predictive pass, cost-aware VoI fail.**

The block should not be used to claim that selective acquisition outperforms simpler policies. The
result falsifies the strong claim for this representation, meta-policy and assumed cost/utility grid.
It does not falsify the entire research programme: the information block may be too weak, almost
universally useful at low cost, or the gain model may lack enough observable heterogeneity.

## Implications

1. Do not tune costs after seeing these test results to manufacture a pass.
2. Obtain buyer-based costs/utilities before another confirmatory experiment.
3. Treat SEC history as part of an efficient baseline state when access cost is negligible.
4. The next external block must add qualitatively different information and have defensible identity
   and point-in-time semantics; do not reuse OpenAlex without founder matching.
5. A future method may use richer conditional treatment/gain estimation, but must be developed on
   train/validation and evaluated on a new temporal cohort or clearly labelled reused-test analysis.

## Claim boundary

Outcome remains a later Form D notice, not success. This experiment is exploratory because costs are
assumed and the 2020 test cohort has now been repeatedly inspected. It is not publication-grade
confirmation of P1.

## Reproduction

```powershell
python code/p1_sec_history_acquisition.py
```

Configuration and complete results: `config.json`, `results.json`. Web-source conclusions about
OpenAlex were paraphrased for licensing compliance; official references remain in
`../../datasets/P1_SOURCE_AUDIT.md`.
