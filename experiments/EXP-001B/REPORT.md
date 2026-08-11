# EXP-001B — Real SEC Baseline

**Status:** complete, exploratory real-data baseline.  
**Scope:** prediction and zero-acquisition decision utility for the SEC weak proxy. This is **not** a
Value-of-Information experiment and does not predict startup success.

## Design

- Population: 12,381 unique US technology-related Form D issuers, not a verified VC/startup cohort.
- Target: later non-amendment Form D notice in the 18 months after decision time.
- Temporal split: train 2016–2018 (8,455), validation 2019 (2,095), test 2020 (1,831).
- Models: prior-only dummy and regularized logistic regression over 29 point-in-time fields.
- Preprocessing fitted on train only: missing-value handling, categorical one-hot encoding, signed
  `log1p` for count/amount/lag fields and standardization.
- Logistic `C` selected by validation log loss from `{0.1, 1, 10}`; selected `C=0.1`.
- Test uncertainty: 1,000 paired bootstrap draws for utility deltas.
- Acquisition cost is zero because no external information block is present yet.

## Predictive results

| Model / split | ROC-AUC | Average precision | Log loss | Brier |
|---|---:|---:|---:|---:|
| Dummy / test | 0.5000 | 0.2922 | 0.6041 | 0.2068 |
| Logistic / validation | 0.6840 | 0.4099 | 0.5352 | 0.1789 |
| Logistic / test | 0.6485 | 0.3912 | 0.5828 | 0.1990 |

The logistic baseline carries real signal for the weak Form-D outcome and improves proper scoring
metrics over the prior-only comparator. Performance drops from validation to test, so temporal drift
or cohort change remains material. This is moderate ranking performance, not strong outcome
prediction and not evidence about company success.

## Zero-acquisition decision utility

The utility grid was declared in `config.json`; it is an assumption grid, not buyer-elicited utility.

| Utility scenario | Logistic mean | Dummy mean | Paired delta | 95% bootstrap CI |
|---|---:|---:|---:|---:|
| Balanced | 0.00519 | -0.06171 | +0.06690 | [0.04450, 0.09011] |
| False-positive averse | -0.08042 | -0.07305 | -0.00737 | [-0.02540, 0.01312] |
| Opportunity averse | 0.11551 | 0.11524 | +0.00027 | [-0.00887, 0.00861] |

**Interpretation:** a predictive improvement does not guarantee decision-value improvement. The
logistic model clearly beats the dummy only under the balanced assumed utility. Under asymmetric
utilities the difference is negative or indistinguishable from zero. Therefore utility elicitation is
a load-bearing gate, not a reporting detail.

## Owner-accepted Layer-A pilot sensitivity

The 20-case balanced pilot contains 9 positive, 4 no-public-evidence and 7 unknown model-reviewed,
project-owner-accepted labels. It was not used for training or model selection.

- Known-only (13 cases): ROC-AUC 0.7778, AP 0.9052, log loss 0.8882, Brier 0.3329.
- Map all unknown to 0: ROC-AUC 0.7374, AP 0.6693, positive rate 45%.
- Map all unknown to 1: ROC-AUC 0.7188, AP 0.9153, positive rate 80%.

The ordering is directionally stable, but probabilities are poorly aligned to these labels and the
sample is tiny and deliberately balanced on the SEC proxy. This analysis is descriptive only: it
cannot estimate prevalence, validate the weak label or serve as an untouched gold test.

## Verdict

**Baseline gate: pass for pipeline feasibility; P1 VoI claim: not tested.**

The real SEC data support a non-trivial temporal predictive baseline. The result justifies proceeding
to utility/cost freeze and one acquisition block. It does not establish that acquiring information
adds value, because no acquisition action or cost has been evaluated.

## Limitations

- Outcome is a subsequent SEC notice, not fundraising success, Series A or company health.
- CIK-level separation does not fully resolve parent/SPV/economic-company identity.
- Test-year aggregate characteristics were already audited; this is not a pristine preregistration.
- The utility grid is assumed, not elicited from buyers.
- Pilot labels are model-reviewed/owner-accepted, not human publication-grade gold.
- No fairness, causal, profitability or real-investor-performance claim follows from these results.

## Reproduction

```powershell
python code/p1_real_baseline.py
```

Environment: Python 3.13.2, pandas 3.0.3, NumPy 2.4.5, scikit-learn 1.8.0. Results and hashes are in
`results.json`; deterministic rerun SHA-256: `7E0B89259E419868FCBBF52D81053DFAD20765F9951D89ED80D4272CC0579AE9`.
