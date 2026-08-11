# Cost-Aware Value of Information for Private-Market Diligence

**Alessandro Guidi**  
**Working paper — evidence-building draft, 2026-07-29**

> This complete evidence draft reports the frozen P1 evidence without opening the locked 2023 test.
> It is not yet a submission manuscript: a formal literature review, venue-specific framing and
> external scholarly citations remain to be completed.
>
> **Revision note, 2026-07-29.** The 2026-07-22 draft ended with a falsified flagship policy and no
> account of why it failed. Six subsequent experiments diagnose the failure and are added here
> (§§4.5–4.9, §5, §8.6), including a synthetic sweep (§4.9) carrying a declared gate that could have
> refuted the resulting claim and did not. The central claim consequently changes from a policy claim to a condition on
> when selective acquisition can work at all, stated in §8.6. One earlier interpretation is retracted
> in §4.7 rather than removed.

## Abstract

Private-market diligence is usually framed as prediction: estimate an outcome from currently
available information. We study a different problem—whether, what and when additional information
should be acquired before a decision, after accounting for acquisition cost and delay. We formalize
this as a cost-aware Value-of-Information (VoI) policy evaluated by Net Decision Value (NDV), with
information state, belief, acquisition action, utility and outcome represented separately.

We test the framework in two phases. The first builds and falsifies a policy; the second diagnoses the
falsification and yields the paper's main contribution, a condition on when selective acquisition can
work at all.

Phase one proceeds in four stages. A synthetic temporal experiment provides conditional evidence:
the learned policy exceeds fixed acquisition baselines in its main configuration but not across all
independent-seed and cost sensitivities. We then construct an open-only, point-in-time panel from SEC
Form D filings. A real-data baseline predicts a later Form D notice better than a prior-only comparator,
but decision utility depends strongly on the assumed payoff matrix. An exploratory acquisition test
finds that issuer filing history adds predictive signal yet a learned selective policy beats no
strongest non-VoI baseline in any of 15 utility-by-cost scenarios. Finally, on a company-disjoint
2021→2022 cohort, issuer history transports as useful baseline information, improving ROC-AUC from
0.5930 to 0.6551; utility improvement is robust only under the balanced assumed matrix.

Phase two asks why. An oracle policy that acquires where the realised gain exceeds cost bounds what any
selective policy could achieve; it beats the strongest baseline by `+0.065` to `+0.087`, six to nine
times the declared margin, while the correlation between predicted and realised per-case gain is
`+0.015`, `-0.070` and `+0.000` across the three utilities. The failure is therefore the selector, not
the cost regime. Two repair routes are then closed. Restricting the population estimate to the slice a
capacity-constrained team would work is unmeasurable rather than merely different: the median
divergence of an arbitrary top-5% slice equals the entire cohort mean being estimated. And targeting the
*incidence* of a decision change—predictable at ROC-AUC 0.770, 0.679 and 0.950, far above per-case
gain—still passes zero of 15 gates, because among decision changes the helpful and harmful fractions do
not vary with predicted incidence.

The resulting claim is a condition rather than a policy: **selective value of information requires the
direction of a decision change to be predictable, not merely its incidence.** Incidence can be
predicted at ROC-AUC 0.95 while direction remains at zero correlation, and a policy targeting incidence
scales harmful changes at the same rate as helpful ones.

The evidence therefore rejects a simple equivalence between predictive lift, uncertainty reduction
and decision value. It supports a falsifiable research design for information acquisition, not a claim
that cost-aware VoI already improves real venture-capital decisions. Buyer utilities remain
unelicited, the outcome is a weak regulatory proxy, the diagnosis rests on a single information block,
and a 914-company 2023 test remains locked.

**Keywords:** value of information; decision intelligence; due diligence; private markets;
point-in-time data; selective information acquisition; temporal validation; negative results

## 1. Introduction

Investment teams rarely possess all potentially relevant information. They choose which question to
ask, source to consult or diligence task to fund next. Each acquisition consumes analyst time, direct
spend and calendar time, and may still leave the decision unchanged. A model that predicts an outcome
more accurately does not by itself solve this resource-allocation problem.

This paper asks:

> Given the information defensibly available at a decision time, can a learned policy acquire an
> additional information block only when its expected decision value exceeds its total cost?

The intended contribution is methodological and empirical. First, we specify a decision-theoretic
object and a falsification rule rather than treating AUC or entropy reduction as sufficient. Second,
we implement temporal and point-in-time controls on an open regulatory source. Third, we preserve
negative evidence: the first real acquisition policy fails its declared gate despite predictive lift.
Fourth, we prepare a company-disjoint future evaluation whose outcomes remain isolated.

Fifth, and added in this revision, we do not stop at the negative result. A failed gate is compatible
with several incompatible explanations—a misspecified utility, a cost regime where acquisition cannot
pay, or a selection signal that carries no information—and reporting the failure without separating them
leaves the reader unable to tell which. We therefore build an instrument that separates them, use it to
locate the failure, and test the two most plausible repairs. Both fail, and the manner of their failure
is more informative than the original gate: it identifies the specific quantity a selective policy needs
and shows that a closely related, far more predictable quantity is not a substitute for it.

That fifth contribution is the one we would defend as transferable. The first four concern how to
evaluate an information-acquisition policy in this domain; the fifth concerns when such a policy can
exist, and its statement does not mention private markets.

The current paper does **not** claim to predict startup success, identify Series A rounds, represent a
verified venture-backed population or estimate realized fund returns. It does not establish that its
utility matrices represent investor preferences.

### 1.1 Related work and positioning

> **Status of this subsection.** Entries below are verified bibliographically against official
> listings and abstracts. The differentiation statements are written from abstracts and, where
> available, introductions — not from complete readings. They are sufficient to position the
> contribution and **not** sufficient to defend it under examination; the full texts must be read
> before submission. Two entries used elsewhere in this project could not be verified and are listed
> as such rather than cited, because an unverifiable citation is worse than an acknowledged gap.

**The acquisition machinery exists; its application here does not.** Bayesian experimental design
formalises choosing which observation to make next, reviewed by
[Chaloner and Verdinelli](https://doi.org/10.1214/ss/1177009939) and brought up to modern estimators
by [Rainforth and colleagues](https://arxiv.org/abs/2302.14545). Two lines are closest to our object.
[Javdani and colleagues](https://arxiv.org/abs/1010.3091) study Bayesian active learning where the aim
is a downstream *decision* rather than hypothesis identification, which is our criterion.
[EDDI](https://arxiv.org/abs/1809.11142) makes per-instance feature acquisition tractable with a
partial variational autoencoder, which is the closest existing implementation of the per-case
targeting we test. We differ in the evaluation object and in the reported result: these works measure
information-theoretic or predictive criteria on benchmark data, whereas we impose a decision-value
gate with declared costs on point-in-time private-market records, and we report that per-case
targeting fails it. Our §8.6 condition is a statement about when such methods can help, phrased in
their terms.

[Golovin and Krause](https://ocs.aaai.org/Library/JAIR/Vol42/jair42-012.php) (JAIR 42, 2011;
[arXiv:1003.3967](https://arxiv.org/abs/1003.3967)) prove that adaptive greedy selection is
competitive with the optimal policy when a problem is adaptively submodular. We cite this for a
negative reason recorded in §4.5: the condition is **vacuous** in a single-block, binary-decision
design, because it licenses greedy selection over a *sequence* of tests and there is no sequence. We
had carried it as a live explanation for our failure, which was a category error, and we state it here
so the mistake is attributable rather than invisible.

**The closest methodological neighbour to our central claim is not in the VoI literature.**
[Alur and colleagues](https://arxiv.org/abs/2306.01646) test whether human experts carry information
beyond the available features by asking whether expert predictions are conditionally independent of
the outcome given those features. That is the same structural question our §8.6 answers for an
information block rather than an expert: per-case gain is nonzero only where the acquired block
changes the action and the outcome adjudicates, so predicting it is predicting the base model's
residual. Their framing supplies a hypothesis test where we supply an oracle bound; the two are
complementary and we should adopt their test in a later revision. We differ in target (a purchasable
information block, not a human judge) and in what is at stake (whether to *pay* for the information,
not whether to automate the decision).

**Prediction in private markets is crowded, and is not our claim.** Recent work applies
leakage-controlled, calibration-first evaluation to startup-outcome prediction and questions whether
high reported accuracy reflects ex-ante signal or methodological artefact
([Information, 2026](https://www.mdpi.com/2078-2489/17/7/702)). That concern is upstream of ours and we
adopt its discipline: our §7.2 point-in-time and CIK-disjointness controls exist for the same reason.
We differ in question. A calibrated predictor of an outcome does not tell an investment team which
diligence task to fund next, which is the resource-allocation problem we formalise.

**On the descriptive side**, [Gompers, Gornall, Kaplan and
Strebulaev](https://doi.org/10.1016/j.jfineco.2019.06.011) survey how venture capitalists report
making decisions, including the weight placed on diligence. That literature establishes that
information acquisition is a deliberate, costly, heterogeneous activity; it does not model the
acquisition choice or evaluate a policy over it, which is the gap this paper enters.

**Decision quality with partially observed outcomes.**
[Dong, Saar-Tsechansky and Geva](https://doi.org/10.1287/mnsc.2021.03357) (*Management Science* 71(7),
2025; preprint [arXiv:2110.11425](https://arxiv.org/abs/2110.11425)) estimate expert decision accuracy
in the setting that actually obtains in practice: abundant records of past decisions, scarce instances
with ground truth. That is our measurement situation too, and it bears on this paper in two places.
It supports treating our 20-case model-reviewed pilot as a sensitivity instrument rather than a gold
standard (§7.1), and it is the closest existing treatment of the problem our weak regulatory proxy
creates. We differ in the object assessed. They assess the quality of decisions already taken; we
assess whether to buy information before taking one. The two compose rather than compete, and their
framework is the natural anchor for a companion decision-quality study rather than for this paper.

**A venture-capital prediction benchmark already exists, and we do not claim to introduce one.**
[VCBench](https://arxiv.org/abs/2509.14448) evaluates founder-success prediction across 22 systems from
nine organisations on a held-out test set, reporting precision, recall and F<sub>0.5</sub>. Two
observations matter for our positioning, and the second cuts in our favour more than we expected.

First, the differentiation is clean because the two designs vary different things. VCBench holds the
information set fixed and ranks predictors; this paper holds the predictor fixed and asks whether to
purchase additional information at a cost. A leaderboard position is silent on that question.

Second, VCBench's choice of a precision-weighted headline metric is independent support for §8.3 rather
than a competing claim. A benchmark built for this domain converged on weighting precision above
recall, which is the same capacity-constrained logic our tail-lift argument makes: a team acts on a
small slice, so average discrimination is the wrong summary. We cite it as corroboration of the metric
argument and as the reason no first-benchmark claim appears anywhere in this paper.

We do not compare our numbers to VCBench's. The target differs (founder success against a Form D
regulatory event), the population differs, and the test sets are unrelated; a cross-benchmark
comparison would be meaningless.

**What this positioning does not claim.** Not that value of information is novel, that graph or
representation methods for private markets are novel, or that no benchmark exists. The claim is
narrower: the machinery is mature, its application to a cost-constrained private-market diligence
decision under point-in-time discipline is where we contribute, and the transferable result is a
condition on when per-case targeting can work at all.

## 2. Decision problem

For company information state `I_t`, latent state `theta`, final decision `d` in decision set `D`,
information action `a` and returned observation `X_a`, define:

```text
BaseValue(I_t) = max_d E[U(d, theta) | I_t]
NDV(a | I_t)  = E[max_d E[U(d, theta) | I_t, X_a] | I_t] - C(a)
NetVoI(a|I_t) = NDV(a | I_t) - BaseValue(I_t)
```

`C(a)` includes direct spend, loaded analyst time, delay and opportunity cost. The action `none` has
zero cost. A cost-aware policy acquires only when estimated NetVoI is positive and otherwise abstains.

We separate five objects: (1) point-in-time Information State; (2) calibrated Belief State;
(3) Acquisition Action and observation model; (4) Utility Model; and (5) Decision/Outcome Records.
This prevents a probability estimate from being mislabeled as an investment decision.

### 2.1 Success and falsification

The flagship policy passes only when it exceeds every declared non-VoI baseline on mean NDV, the
paired interval against the strongest comparator excludes zero, and the conclusion survives declared
cost and utility sensitivities. Otherwise the tested claim is narrowed or rejected; predictive gains
are reported separately.

## 3. Data

### 3.1 Historical SEC cohort

We use official quarterly SEC Form D structured datasets. The historical panel covers 2008 Q1–2023
Q2 and contains 594,422 privacy-minimized filings from 274,947 issuers. The first-anchor model-ready
cohort contains 12,381 unique US technology-related primary issuers: 8,455 in 2016–2018, 2,095 in
2019 and 1,831 in 2020.

The population is not a verified startup, software, seed or venture-backed cohort. The weak outcome is
one when the same CIK records a later non-amendment Form D notice in the 18 months after a decision
time set 12 months after anchor availability. It is not a priced round, institutional financing,
Series A, fundraising success or company success label.

Related-person, signature and recipient tables are not retained. Phone numbers and street addresses
are excluded. Corporate name, CIK and coarse corporate geography are retained for entity-resolution
audits.

### 3.2 Future company-disjoint cohort

A separate panel extends the archive through 2026 Q1. Candidate anchors span 2021–2023. Label
completeness uses a conservative 2025-12-31 cutoff, leaving a three-month buffer for records that may
appear in a subsequent quarterly release. Incomplete windows are censored. Every CIK in the historical
model-ready cohort is removed.

The resulting cohort contains 2,369 development issuers in 2021, 2,243 validation issuers in 2022 and
914 locked-test issuers in 2023, with zero historical CIK overlap. The 2023 outcomes are null in
operational copies and isolated in a hashed local vault. No result in this draft uses those outcomes.

## 4. Experimental sequence

### 4.1 EXP-001A: synthetic mechanism test

The synthetic harness samples worlds with known hidden signal quality, availability and heterogeneous
cost. Models train on 2016–2018, select on 2019 and evaluate on 2020. Comparators are no acquisition,
random, cheapest, most predictive and expected uncertainty reduction; an oracle sees the data-
generating process and is only an upper bound.

The main 100-world run gives learned-minus-best-baseline NDV `+0.002772`, with paired 95% interval
`[0.000133, 0.006112]`. An independent-seed run and low-cost sensitivity cross zero, whereas the
high-cost sensitivity passes. We therefore classify the evidence as synthetic-conditional, not a
demonstration in private markets.

### 4.2 EXP-001B: historical real-data baseline

A regularized logistic model over point-in-time SEC fields is selected by 2019 log loss and evaluated
on 2020. It improves ROC-AUC from 0.5000 to 0.6485 and log loss from 0.6041 to 0.5828. Under the
balanced assumed utility its mean utility exceeds the dummy by `+0.06690` (`[0.04450, 0.09011]`).
Under false-positive-averse and opportunity-averse matrices, intervals include zero. Prediction is
therefore informative but not utility-invariant.

### 4.3 EXP-001C: first real acquisition test

The baseline state contains anchor-filing fields. The acquired block contains prior/intervening SEC
issuer history known by decision time. The enriched model improves 2020 ROC-AUC from 0.6261 to 0.6485
and log loss from 0.58465 to 0.58278.

A Ridge meta-policy estimates heterogeneous acquisition gain from cross-fitted development
predictions. Across three utility matrices and five normalized costs, the learned policy passes zero
of 15 gates against the strongest non-VoI comparator. Its best point estimate is `+0.00340`, with
interval `[-0.00167, 0.00906]`. This falsifies selective acquisition for the tested block,
representation, gain model and assumption grid. Costs are not adjusted after observing this result.

### 4.4 EXP-001D: company-disjoint baseline transport

The future-cohort recipe selects regularization with five-fold cross-validation inside 2021 only and
evaluates once on 2022. No 2022 tuning and no 2023 outcome access occur.

| Model | ROC-AUC | Average precision | Log loss | Brier |
|---|---:|---:|---:|---:|
| Development prior | 0.5000 | 0.1922 | 0.4925 | 0.1563 |
| Anchor only | 0.5930 | 0.2502 | 0.4840 | 0.1537 |
| Anchor + SEC history | **0.6551** | **0.3214** | **0.4681** | **0.1482** |

Relative to anchor-only, full-model utility improves by `+0.04191` under the balanced matrix, with
interval `[0.02317, 0.05996]`. False-positive-averse and opportunity-averse deltas are small and their
intervals cross zero. Mean utility for the full model remains negative in every declared scenario;
relative lift must not be interpreted as positive business value.

### 4.5 EXP-005: separating rival explanations of the failure

EXP-001C carried three unseparated explanations for its 0-of-15 result: a misspecified utility model, a
cost regime in which acquisition genuinely does not pay, and failure of the structural conditions
licensing adaptive greedy acquisition. Nothing in the original design distinguished them.

The third candidate is void as originally stated and we record the correction rather than quietly
replacing it. Adaptive submodularity licenses near-optimality of adaptive *greedy* selection over a
*sequence* of tests. EXP-001C acquires one block under a binary decision, so there is no sequence,
greedy reduces to acquiring where expected gain exceeds cost, and submodularity has nothing to
constrain. Carrying it as a live hypothesis was a category error. The defensible third candidate
concerns the selection signal instead: either per-case gain does not vary, so there is nothing to select
on, or its variation is not predictable from the base state, so the selector is noise.

The separating instrument is an **oracle** policy that acquires exactly where the *realised* per-case
gain exceeds cost. It uses the outcome and is therefore not a policy; it is the least upper bound on
what any selective policy could achieve. The decomposition follows directly. An oracle advantage below
the declared margin implies no selective policy can win and the constraint is the problem. An oracle
advantage above the margin with a learned advantage at zero implies a winning policy exists and this
selector cannot find it.

Thresholds were declared before running, in normalised NDV units: oracle margin `0.010`, learned margin
`0.005`, signal floor `|r| = 0.05`. The base and acquired models reproduce EXP-001C exactly, so the
result describes that experiment rather than a variant.

| Utility | Gain nonzero | Gain sd | corr(predicted, realised) | Oracle advantage | Learned advantage |
|---|---:|---:|---:|---:|---:|
| balanced | 20.4% (+13.1 / −7.3) | 0.4061 | **+0.015** | +0.065 to +0.087 | −0.004 to +0.003 |
| false-positive-averse | 13.4% (+5.6 / −7.8) | 0.4067 | **−0.070** | +0.064 to +0.070 | −0.004 to +0.003 |
| opportunity-averse | 4.9% (+4.0 / −0.9) | 0.1634 | **+0.000** | +0.009 to +0.012 | −0.000 to +0.003 |

Thirteen of fifteen cells are model-side; two are problem-side; none is a policy win. Gain is genuinely
heterogeneous—acquisition changes the realised decision in 20.4% of cases under the balanced matrix,
helping in 13.1% and harming in 7.3%, with standard deviation 0.4061 against a mean of `+0.0284`—so
there is a great deal to select on. The heterogeneity is not recoverable from the base state.

Two precisions, both against our own first reading. Spearman coefficients are `+0.055`, `−0.017` and
`+0.131`, so under one utility the rank correlation exceeds the declared floor by 2.6x; "selecting at
chance" is too strong, and the accurate statement is that a faint monotone ordering exists and is far
too weak to act on. Second, the predicted-gain dispersion misses the realised dispersion in *both*
directions depending on the utility—0.11x under balanced, 4.15x under opportunity-averse—at
approximately zero correlation throughout. A uniformly over- or under-confident model is mis-scaled and
can be recalibrated; one whose dispersion is ten times too flat on one payoff matrix and four times too
wide on another is not tracking the quantity.

The structural reason is that per-case gain is `U(y, a_full) − U(y, a_base)`, which is nonzero only when
the two models choose different actions *and* the realised outcome adjudicates between them. Predicting
it requires predicting whether the base model's error will be corrected on that case, which is
predicting the base model's residual, which is predicting the outcome better than the base model does.
With base ROC-AUC between 0.59 and 0.65 on this weak proxy, a gain model inherits that ceiling and then
loses further to variance.

The constructive residue is that the *population mean* gain is estimable and changes sign with the
utility: `+0.0284` under balanced, `−0.0081` under false-positive-averse, `+0.0030` under
opportunity-averse. Under false-positive-averse the block therefore reduces decision quality before any
cost is charged, flipping 7.8% of cases into error against 5.6% into correctness, which is why
abstention is the strongest non-VoI comparator in eleven of fifteen cells.

Artefacts: `experiments/EXP-005/`.

### 4.6 EXP-007: restricting the estimate to a capacity-constrained slice

If only the population mean is estimable, a budgeted formulation must use it. But a team under a
capacity constraint works only the top slice of its pipeline, so the quantity is measured on a
population the decision never sees. EXP-007 restricts the estimate to nested top-k slices of the test
cohort ordered by the base model's own predicted probability, which is the only ranking available before
acquiring anything.

Slices `5/10/20/50/100%`, transfer margin `0.010` and minimum slice size 30 were declared before
running, as was the expected direction: the top of a probability ranking is where the base model is
already confident, gain is nonzero only where acquiring changes the action, and confident cases are the
hardest to move, so the slice mean should be smaller in magnitude than the cohort mean.

| Utility | Cohort mean | Top 5% | Top 10% | Top 20% |
|---|---:|---:|---:|---:|
| balanced | +0.0284 | +0.0054 | +0.0055 | +0.0082 |
| false-positive-averse | −0.0081 | +0.0679 | +0.0587 | +0.0034 |
| opportunity-averse | +0.0030 | 0.0000 | 0.0000 | 0.0000 |

The declared direction was correct under balanced. Under false-positive-averse the point estimate
changes sign. Under opportunity-averse the block does not change the decision for a single case in the
top half of the ranking, so the cohort mean is generated entirely outside the slice a budget reaches.
Across cost scenarios the all-or-nothing decision computed on the cohort differs from the one computed
inside a slice in 20 of 75 cells.

### 4.7 EXP-008: a null ordering, and a retraction

EXP-007 was written as a confirmation that the cohort estimate does not transfer. EXP-008 added a random
ordering as a control and that conclusion does not survive.

| Ordering | Top 5% | Top 10% | Top 20% |
|---|---:|---:|---:|
| base probability (EXP-007's) | −0.0230 | −0.0229 | −0.0202 |
| offering size | −0.0012 | −0.0175 | −0.0188 |
| investor count | −0.0393 | −0.0339 | −0.0202 |
| **random (control)** | **−0.0936** | −0.0503 | −0.0120 |

An arbitrary ordering produces a larger divergence than any substantive one, and across all utilities
real orderings diverge in 4 of 36 cells against the control's 1 of 9—the same rate. **We therefore
retract EXP-007's interpretation.** What is established is not that the slice mean differs from the
cohort mean, but that at this slice size it cannot be estimated: a precision statement, not a bias
statement. The arithmetic was already present in EXP-007's own limitations, where the standard error on
92 cases with per-case standard deviation 0.41 is approximately 0.043, and we failed to apply it to our
own headline.

EXP-008 also retracts the secondary reading. The monotone rise EXP-007 described as a structural
regularity tests at Spearman `−0.479` with `p = 0.174` and is not established. An equal-count decile
profile of the base probability shows instead a concentration in the lower-middle of the range under the
balanced matrix—deciles three and four reach `+0.0710` and `+0.0984`, with the share of decision changes
peaking at 56.3% in decile five—giving a middle-versus-extremes gap of `+0.0308` that clears the
declared margin. But exactly one of ten decile intervals excludes zero without multiplicity correction,
and the shape does not replicate under the other two utilities (`p = 0.715` and `p = 0.814`, with
deciles four through ten exactly zero under opportunity-averse).

One design fault in EXP-008 is recorded because it bounds what the experiment tested. A ranking intended
to order cases by base-model uncertainty returned results identical to the probability ranking. The base
model never predicts above 0.474, so every case lies below 0.5 and `−|p − 0.5|` is a monotone increasing
function of `p`: the two orderings coincide. The robustness check therefore ran with two independent
alternatives rather than four. Separately, that a model with a 29.2% base rate never assigns probability
above 0.474 means it never asserts the outcome is more likely than not.

### 4.8 EXP-009: a calibrated null, and targeting incidence instead of gain

EXP-008 established its correction against a single random ordering. EXP-009 draws four hundred per
utility, giving a threshold rather than a comparison point.

| Utility | Slice | n | Null sd | Median \|divergence\| | 95th percentile |
|---|---|---:|---:|---:|---:|
| balanced | 5% | 92 | 0.0427 | **0.0284** | 0.0882 |
| balanced | 10% | 183 | 0.0267 | 0.0202 | 0.0530 |
| balanced | 20% | 366 | 0.0190 | 0.0126 | 0.0366 |

The cohort mean gain under the balanced matrix is `+0.0284` and the median divergence of an arbitrary
top-5% slice is `0.0284`. At the slice size a capacity constraint implies, the typical meaningless
deviation equals the entire quantity being estimated. Three of 27 ordering-by-slice cells clear the
null against 1.35 expected, all under the false-positive-averse matrix, and we report them as a lead
rather than a finding.

The second half of EXP-009 tests the one repair route EXP-008 left open, and tests the objection to it
first. If gain concentrates where the base and acquired models disagree, and disagreement requires the
block but not the outcome, then predicting *whether* the action changes might support targeting without
requiring per-case gain. The objection is that knowing the action changes says nothing about direction.
Decomposing `E[gain] = P(change) · E[gain | change]` tests it directly.

| Utility | Action changes | E[gain \| change] | Helped |
|---|---:|---|---:|
| balanced | 20.4% (n=374) | +0.139 | 64% |
| false-positive-averse | 13.4% (n=245) | −0.0602 `[−0.1980, +0.0796]` | 42.0% |
| opportunity-averse | 4.9% (n=89) | +0.0618 `[−0.0927, +0.2079]` | 82.0% |

Predictions recorded before running—positive under balanced, negative under false-positive-averse, and
approximately 42% helped in the latter, derived arithmetically from EXP-005's reported 5.6% against
7.8%—hold in all three cases. The objection is therefore *not* fatal as stated: a decision change is
worth something and its sign is stable within a utility, which the investor selects before acquiring.

The premise of the repair also holds, and strongly. Discarding the direction makes the target far more
predictable: the change indicator reaches ROC-AUC `0.770`, `0.679` and `0.950` across the three
utilities, against per-case gain correlations of `+0.015`, `−0.070` and `+0.000`.

**And the policy passes zero of 15 gates.** Its best advantage anywhere is `+0.0025` with an interval
spanning zero, against the declared margin of `0.005`. The acquisition rate also shows almost no
dynamic range—94.6% at zero cost, 15.2% at cost 0.05, 0.1% at cost 0.1—so the policy is close to an
all-or-nothing threshold, which is what EXP-005 identified as correct in this regime.

Artefacts: `experiments/EXP-007/`, `experiments/EXP-008/`, `experiments/EXP-009/`.

### 4.9 EXP-010: the condition as a mechanism, with a falsification gate

Everything above rests on one information block, one cohort and one weak proxy, and a
second real block is blocked on four independent source gates (§6). The condition's
generality therefore cannot be tested with real data at present. It can be tested as
a mechanism: in synthetic worlds the hidden truth is ours to set, so the two
quantities the condition names can be varied independently.

Two knobs are swept. `lam` scales how strongly the base features predict the
acquirable signal, so high `lam` means the base state anticipates the block.
`base_strength` scales how much the base features explain the outcome, which the
structural argument of §8.6 says should govern the size of the residual. The grid is
5 × 3 cells, 40 worlds each, 1,500 cases per world, two costs, giving base ROC-AUC
from 0.614 to 0.840 — spanning and exceeding the 0.59–0.65 range observed on real
data. The gate was declared before running:

> A cell **refutes** the condition if the learned selective policy beats the
> strongest non-VoI baseline by more than `0.010` with a paired bootstrap interval
> over worlds excluding zero, while corr(predicted, realised gain) exceeds `0.05`.

**Zero of thirty tests refute, and no cell approaches the margin.** The learned
advantage is negative in all fifteen cells at both costs, with the interval over
worlds excluding zero in every one, ranging from `−0.0018` to `−0.0064`. The
selective policy is not merely failing to beat the best fixed baseline; it is
reliably worse than it across the grid, in worlds where the model class is correctly
specified. The conclusion does not depend on the gate's conjunction: no cell reaches
an advantage above the margin irrespective of its correlation, so the advantage
branch decides it alone.

The oracle advantage runs from `+0.0217` to `+0.0562`, acquiring 60% to 76% of cases,
so a winning selective policy existed in principle in every cell. The synthetic
worlds reproduce the real-data structure of §4.5 — a large oracle gap with a zero
learned gap — which is the reason for running them.

One declared prediction was confirmed and one was refuted, and the refuted one
changes the mechanism we assert. The prize falls on both axes as predicted: the share
of cases where acquiring changes the decision falls from 21.0% to 13.7% as `lam`
rises at low base strength and from 21.0% to 12.3% as `base_strength` rises at
`lam` = 0, with mean realised gain falling from `+0.0276` to `+0.0099` across the
diagonal. But we predicted the predicted-realised gain correlation would *rise* with
`lam`, on the reasoning that a base state anticipating the block makes the direction
of a change knowable. It falls: at `base_strength` 0.65 the sequence is 0.056, 0.049,
0.038, 0.024, 0.007.

The corrected mechanism is less favourable to selective acquisition than the one we
proposed, which is why the error is recorded rather than smoothed over. We had
hypothesised a trade-off frontier, with a predictable direction and a small prize at
one end and a large prize with a blind selector at the other. There is no frontier.
When the base state anticipates the block, the prize shrinks **and** the direction
becomes less predictable, because the quantity being predicted becomes rare and its
estimate is then dominated by noise. Both terms degrade together.

The residual correlation is largest at `lam` = 0, where the base state carries no
information about the signal — the cell our proposed mechanism predicts should be
lowest. The coherent reading is that this residue is incidence rather than direction:
with an independent signal, acquiring changes the decision in 21% of cases, and those
are the cases near the decision boundary, which is predictable from the base state
alone. The gain model is partly detecting which cases will change rather than which
changes will help. That is §4.8's finding reproduced where we control the generator,
and it is the strongest corroboration this experiment provides.

The strongest limitation is stated first: both the outcome and the signal are
generated logistically and both learners are logistic, so no functional-form mismatch
exists anywhere in the grid. A misspecified base model could leave a structured
residual that a gain model exploits, and this design cannot see that. Artefacts:
`experiments/EXP-010/`.

## 5. Findings

First, the cost-aware mechanism can work in synthetic environments, but its advantage is small and
not robust to every declared replication. Second, real SEC information has reproducible predictive
signal across two temporal regimes. Third, predictive lift does not imply selective-acquisition value:
SEC history is useful enough to belong in the efficient baseline state, yet EXP-001C provides no
evidence that a learned policy should selectively pay to retrieve it. Fourth, utility assumptions are
load-bearing. Model rankings by proper scoring rule are more stable than their decision-value
consequences. Fifth, the choice of evaluation metric is itself load-bearing: EXP-002 finds that the
same block yielding ROC-AUC near 0.61 concentrates 1.45x outcome enrichment in its top 5% across a
CIK-disjoint boundary, so average discrimination and tail concentration diverge materially and a
capacity-constrained policy must be judged on the latter.

Sixth, and this is the finding we would put first if the sequence permitted it, the failure of selective
acquisition is located rather than merely reported. An oracle bound shows a winning selective policy
exists in this regime, so neither the utility grid nor the cost grid is the binding constraint; the
selector is. Seventh, the two available repairs fail, and their failure identifies the operative
quantity. Restricting the estimate to a capacity-constrained slice is unmeasurable at this cohort size,
with the median null divergence equal to the whole quantity being estimated. Targeting the incidence of a
decision change succeeds at prediction and fails at decision value, because the helpful and harmful
fractions of a change do not vary with predicted incidence.

The strongest empirical conclusion is therefore narrower than the original flagship hypothesis and, in
one respect, more general than it. Narrower: **point-in-time issuer history transports as baseline
information for the weak SEC outcome, while the first tested cost-aware acquisition policy fails its
declared real-data gate.** More general: **the failure is attributable to a specific, statable condition
on the selection signal rather than to this block, this cohort or this implementation** (§8.6).

## 6. Source-gate evidence

A candidate information block is not admissible merely because a current public dataset contains a
relevant-looking field. It must also satisfy source rights, identity resolution and historical
availability at the decision time. We applied these gates before outcome modelling to three
qualitatively different candidates.

### 6.1 OpenAlex: identity gate failure

OpenAlex offers reusable scholarly metadata and public snapshots, but the privacy-minimized SEC
cohort does not contain reviewed founder identities. Company-to-institution or founder-to-author
name matching would therefore introduce unmeasured false links, while a current corrected entity
link would not necessarily establish what was knowable historically. We rejected this block rather
than reintroducing SEC related-person data or using name-only matching to make the experiment run.

That rejection is supported by measurement rather than assertion. Using SEC CIK as ground truth on
deliberately adversarial pairs—lexically similar but distinct issuers, and lexically dissimilar but
identical ones—seven string matchers were compared: token Jaccard with and without legal-suffix
stripping, sequence ratio, character trigrams, inverse-document-frequency weighting, a head-token
variant, and the pointwise maximum of all of them. The best single matcher reaches **80.8%** balanced
accuracy and the pointwise maximum reaches 80.2%, so combining every similarity does not beat the best
one, which is the signature of a ceiling rather than of a poorly chosen metric. Accuracy on lexically
dissimilar same-entity pairs ranges from 0.0% to 7.5%: no string similarity recovers a corporate
rename, because the information is absent from the string. Non-name attributes available for 99.8% of
pairs separate precisely those hard cases—state agreement differs by 53 percentage points between
same-entity and different-entity pairs, entity type by 38 and industry by 26—so the limitation is
missing signal rather than a weak model. Because the SEC cohort retains no reviewed founder identities,
none of those attributes is available for a founder-to-author join, which is why §6.1 fails on identity
and not on model capacity. Artefacts: `experiments/EXP-005-ER/`, `experiments/EXP-006/`.

### 6.2 SBIR/STTR: temporal-availability gate failure

A development/validation-only audit joined the official SBIR/STTR award download to 10,550 issuers
from 2016–2019 using exact normalized company name plus two-letter state. It found 622 candidate
matches (5.90%), of which 350 had a proposal-award date no later than the SEC decision time. No
candidate key was ambiguous under that conservative rule.

These counts did not justify modelling. Proposal-award date is an event date and applicant
notification date is a process date; neither proves when the record first became publicly observable.
A current complete download can contain later corrections or backfill. Because the required
`available_time <= decision_time` relation could not be established, the block failed before any
outcome, utility or VoI analysis. Sparse coverage was not the binding reason for rejection.

### 6.3 USPTO/PatentsView: operational access gate

Pre-grant patent publications are conceptually suitable because official publication date can define
availability and the signal differs from financing history. The documented PatentsView transition
maps published-application and disambiguated-assignee tables to the USPTO Open Data Portal product
`pvpgpubdis`. At the time of audit, however, metadata and file endpoints required authenticated
access and returned 401/403 without a personal API key. No credentials were requested or stored, no
unofficial mirror was substituted, and no extraction or matching was performed.

Even after access becomes available, the block still requires an immutable product/file version,
publication-date cutoffs, separate raw and retrospectively disambiguated assignee fields, reviewed
assignee-to-issuer resolution and a redistribution review.

### 6.4 SEC Form C: coverage gate failure

The official SEC Crowdfunding Offerings data provide filing dates, issuer CIKs and structured
Regulation Crowdfunding disclosures, allowing exact identity resolution and a defensible
point-in-time cutoff. Across 31 quarterly archives, only 52 of 2,369 development issuers (2.20%) and
57 of 2,243 validation issuers (2.54%) had a Form C known by decision time. This failed the declared
minimum of 100 development matches. No outcome model or VoI policy was run. The rejection concerns
coverage in this Form-D-derived cohort, not the information content of Form C when present.

### 6.5 Why source audits are part of the result

These failures are not incidental data-engineering notes. A retrospective source can generate
apparently strong predictive lift while violating the intervention being evaluated: information that
could actually have been acquired at time `t`. Auditing rights, identity and public availability
before modelling limits researcher degrees of freedom, prevents outcome-driven source selection and
preserves the meaning of VoI. Under this design, a failed source gate is a valid negative result and
must not be bypassed to increase model coverage.

## 7. Threats to validity

### 7.1 Construct validity

The observed outcome is a subsequent non-amendment Form D notice within a fixed window. It is a weak
regulatory-event proxy, not company success, investment return, institutional participation, a priced
round or Series A. Likewise, the technology-related Form D filter does not identify a verified
startup, software, seed or venture-backed population. Any interpretation beyond the regulatory event
would exceed the measurement design.

The decision utility matrices are assumed scenarios. They have not been elicited from investment
professionals, and normalized acquisition costs do not measure actual analyst time, direct spend,
delay or opportunity cost. Results involving utility or NDV are consequently assumption-bound. The
absence of current interview access defers this validity gate; it does not remove it.

The 20-case public-evidence pilot is model-reviewed and project-owner accepted. It is deliberately
small, selected through a weak-label-balanced queue and contains unresolved unknowns. It is not an
independently adjudicated human gold standard, cannot estimate prevalence and is not an untouched
publication-grade test.

### 7.2 Internal validity

Point-in-time controls use SEC filing dates at day precision, not sub-day acceptance times. Form D is
issuer-submitted, may be amended and can appear in a later quarterly release. Although features are
restricted to filing dates no later than decision time, source errors and release-boundary effects
remain possible.

CIK separation prevents the same issuer identifier from crossing the declared company-disjoint
boundary, but a CIK is not always equivalent to an economic company. Reorganizations, special-purpose
vehicles, parent/subsidiary relationships or identifier changes may leave residual dependence. The
current design therefore establishes CIK-disjointness, not perfect economic-entity disjointness.

EXP-001C estimates heterogeneous gains with one Ridge meta-policy and one representation of the SEC
history block. Its failure applies to that declared design, not to all possible conditional-value
estimators. Conversely, trying many alternative estimators after observing the test would weaken any
subsequent claim; such work requires a new development protocol and evaluation cohort.

The condition in §8.6 inherits that limit and adds two of its own. It rests on **one** information
block, so whether direction becomes predictable for a qualitatively different block is untested, and
this is the largest single threat to the paper's main claim rather than a minor caveat. The oracle
policy in §4.5 uses realised outcomes, so it bounds what a selective policy could achieve and does not
demonstrate that any implementable policy reaches it; the inference drawn from it is only the negative
one, that the utility and cost grids are not the binding constraint. And the change-targeting policy of
§4.8 holds `E[gain | change]` at a population constant. A policy modelling `E[gain | change, x]` was not
run; it is per-case gain conditional on a change, which is the quantity §4.5 finds unpredictable
restricted to a smaller sample, so the structural argument predicts it does not help—but that prediction
is untested and stated as such.

Two of the diagnostic experiments were run in sequence on the same cohort after an earlier result was
seen, which is optional stopping. EXP-007's slice comparison failed a declared bar at one cohort size
and passed after the sample was expanded; the corresponding conclusion was subsequently retracted for an
independent reason (§4.7). Where a comparable pattern arose elsewhere in the wider project, a
split-sample check was substituted for a repeated look. Readers should treat §§4.6–4.8 as a diagnostic
sequence on an exploratory cohort, not as confirmatory tests.

### 7.3 Evaluation validity

The 2020 cohort has been inspected repeatedly across data audits and EXP-001B/C. It is exploratory and
cannot supply new confirmatory evidence. The 2022 cohort has now been used once for EXP-001D and the
baseline recipe is frozen; it must not be used for further baseline tuning. A new block may receive
one declared validation use on 2022 after development on 2021, but decisions induced by that result
must be recorded before any future test.

The 914-case 2023 outcomes remain isolated and uninspected. This protects a future evaluation but does
not guarantee that a positive result will generalize beyond the SEC population, weak outcome,
calendar regime or assumed utility grid. Opening the vault without a complete protocol and script
hash would invalidate its intended role.

### 7.4 External, causal and normative validity

No experiment observes real investment-committee behavior, private diligence information, realized
fund returns or buyer willingness to pay. The study makes no causal claim that a signal changes
company outcomes, no profitability claim and no product-market-fit claim. It also does not establish
fairness across founder or company groups: sensitive personal attributes were intentionally not
collected, so subgroup fairness cannot be inferred from their absence. The system is decision-support
research, not automated investment advice.

## 8. Discussion

### 8.1 Prediction is not decision value

The experiments separate three questions that are often conflated: whether information predicts an
outcome, whether it changes the utility-maximizing decision and whether that change is worth the cost
of obtaining the information. SEC history answers the first question positively in both historical
and company-disjoint temporal comparisons. It does not answer the third: EXP-001C passes no declared
cost-aware gate.

Uncertainty reduction is similarly insufficient. A block can reduce entropy while leaving the chosen
decision unchanged, or alter a decision by less than its retrieval and delay cost. The relevant
object is the distribution of utility-changing observations conditional on the current state, not
information quantity alone.

### 8.2 Baseline information and acquisition actions are different objects

EXP-001D supports SEC history as part of an efficient initial state when it is cheaply and lawfully
available. That same finding makes it a poor candidate for a discretionary acquisition action: if a
block is broadly useful and nearly free, a selective policy has little heterogeneity to exploit; if
its processing cost is material, `none` may dominate for most cases. Information can therefore be
valuable as infrastructure while failing as a next-best-diligence action.

This distinction prevents a failed VoI experiment from being rewritten as a success based on AUC.
The correct update is to strengthen the baseline and require the next action to add qualitatively
different, point-in-time-safe evidence.

### 8.3 The evaluation metric must match the capacity constraint

EXP-001B through EXP-001D evaluate information with average criteria: ROC-AUC, log loss, mean
utility. These are appropriate when every case carries equal weight. They are mismatched when the
decision concerns only an extreme slice, which is the operative case under a capacity constraint: an
investment team screens the companies it has capacity to examine, not the median company.

EXP-002 measures the alternative quantity on the same cohort, defined as

```text
lift(q) = P(outcome = 1 | feature in top q) / P(outcome = 1)
```

with bootstrap intervals and Benjamini-Hochberg control across the feature-by-threshold scan. On a
CIK-disjoint 2021 to 2022 split, four issuer-history features transport with intervals excluding
1.0; `known_amendment_count` reaches 1.77x and `known_filing_count` 1.45x in the top 5%. The same
block yields ROC-AUC near 0.61. Five features show lift rising monotonically as the slice narrows,
which is harder to obtain by chance than a single significant threshold. Anchor deal-size terms
carry no tail lift and invert in development, consistent with issuers raising the largest single
offerings filing again less often.

Three qualifications bound this. First, an issuer that has filed repeatedly is by construction an
issuer that files, so part of the lift reflects persistence of filing behaviour rather than any
economic property of the company; this experiment does not separate the two and the effect should be
assumed largely mechanical until a design does. Second, the outcome remains the weak regulatory
proxy, so the enrichment concerns that event and not fundraising success. Third, an enrichment ratio
is not a decision value: converting it requires the elicited utilities that remain unavailable.

The methodological point survives these qualifications. Average discrimination and tail concentration
are distinct properties of the same information, they can diverge materially, and a policy that only
ever acts on an extreme slice should be evaluated on the second. Reporting only the average metric
would have left this concentration invisible, in the same way that reporting only predictive lift
would have obscured the acquisition failure in EXP-001C. Artefacts: `experiments/EXP-002/`;
estimator: `code/tail_lift.py`.

### 8.4 Abstention is a substantive comparator

Across the synthetic runs, the strongest fixed baseline is consistently `none`; in several real
utility-cost scenarios, acquiring nothing is again strongest. This is not a trivial benchmark.
Diligence consumes scarce attention, can delay a decision and may retrieve redundant information.
A credible acquisition policy must therefore beat an active default of stopping information search,
not merely outperform random acquisition.

### 8.5 Utility elicitation is deferred, not eliminated

A complete bounded assumption grid allows method development to proceed while access to qualified
buyers is unavailable. It can reveal whether conclusions reverse under plausible preference
structures and prevents selecting one favorable matrix after the result. It cannot establish which
scenario represents an investment organization. Interviews and workflow observation remain required
for buyer-realistic cost, delay and payoff estimates, external validity and commercial claims.

### 8.6 Selective acquisition needs the direction of a decision change, not its incidence

This is the paper's central claim after the diagnostic sequence, and it is a condition rather than a
policy.

> Selective value of information can beat all-or-nothing acquisition only when the **direction** of a
> decision change is predictable from the pre-acquisition state. Predicting the **incidence** of a
> change is not sufficient, however well it is done.

Both halves are measured rather than argued. Incidence is predictable here at ROC-AUC up to `0.950`.
Direction is not: the correlation between predicted and realised per-case gain is `+0.015`, `−0.070`
and `+0.000`. And a policy built on the predictable half passes none of its fifteen declared gates.

The mechanism is explicit. A policy scoring cases by `P(change) · E[gain | change]`, with the second
term a population constant, concentrates acquisition where the action is most likely to change. Among
changes, 64% help and 36% harm under the balanced matrix, and that ratio does not vary with `P(change)`.
Purchasing more probability-of-change purchases proportionally more helpful *and* more harmful changes.
The policy buys action, not correctness.

Two reasons to state the condition this way rather than the way we stated it after EXP-005. First, the
earlier formulation—that selective acquisition requires per-case gain to be more predictable than the
outcome—invites the objection that the gain model was simply weak. EXP-009 removes that objection by
predicting a closely related quantity almost perfectly and still failing. Second, incidence is exactly
the quantity a practitioner would reach for, because it is observable as `|p_base − p_full|` and needs no
outcome. Naming it and showing it does not work is more useful than a general statement about
predictability.

**The mechanism is not a trade-off, and we had it wrong.** The natural reading of the condition is that
predictability and prize trade off: a base state that anticipates the acquired block makes the direction
of a change knowable but leaves little to gain, while a base state that does not leaves a large prize
and a blind selector. We wrote that reading down as a prediction and EXP-010 refuted it. Sweeping how
strongly the base state anticipates the block, the prize falls as expected *and the correlation falls
too* — 0.056, 0.049, 0.038, 0.024, 0.007 at intermediate base strength. There is no frontier to sit on.
Anticipating the block does not make direction predictable; it makes the quantity rare, and a rare
quantity is estimated with more noise, not less. Both terms degrade together, which is a stronger
statement against selective acquisition than the trade-off we had assumed and the reason the failed
prediction is reported rather than removed.

**The condition is mechanism-supported, not merely cohort-observed.** Across a 5 × 3 grid spanning base
ROC-AUC from 0.614 to 0.840, with 40 worlds per cell and a correctly specified model class, the learned
selective policy is *significantly worse* than the best fixed baseline in 30 of 30 tests, while an oracle
prize of `+0.0217` to `+0.0562` existed in every cell (§4.9). The gate that would have refuted the
condition was declared before running and did not fire. That is the strongest generality evidence
available without a second real block, and it is not a substitute for one: the synthetic worlds cannot
exhibit functional-form misspecification, which is the one route by which a real base model might leave
a structured residual for a gain model to exploit.

The condition also explains why the correct policy in this regime is all-or-nothing. If direction is
unpredictable, the only estimable object is the population mean gain, whose sign depends on the utility
matrix; the acquire decision then belongs to the utility function at cohort level rather than to any
per-case selector. That is consistent with abstention being the strongest comparator in eleven of
fifteen cells.

Three limits bound the condition's generality and none is small. It rests on **one real** information
block, so whether direction becomes predictable for a qualitatively different real block is untested and
remains the single largest threat to this section; EXP-010 addresses generality across worlds, not across
blocks. The utilities are assumed rather than elicited, though the diagnosis holds across all three on
real data and the sweep varies the world rather than the preferences. And the sweep's model class is
correctly specified throughout, so the one route by which the condition could fail on real data —
a misspecified base model leaving a structured residual — is exactly the route the synthetic design
cannot exhibit. A richer state representation that pushed the predicted-realised correlation above the
declared floor *and* converted it into an NDV win would refute the condition; the structural argument and
the sweep together make that unlikely rather than impossible.

## 9. Future protocol

The next empirical step is not another model on SEC history. It is one qualitatively different
information block that passes legal/reproducibility, identity-resolution and point-in-time gates. No
proprietary database is required, and no source will be rescued through undocumented mirrors,
retrospective timestamps, personal-data expansion or unverifiable name matching.

The sequence before opening the future test is:

1. **Source freeze.** Record official source, rights, immutable version/checksum, coverage and the
   defensible rule for `available_time`.
2. **Entity-resolution freeze.** Declare blocking fields, normalization, ambiguity handling, review
   sample and match-quality criteria before outcome modelling.
3. **Development-only construction.** Define features and missingness using the 2,369 issuers from
   2021; preserve anchor plus SEC history as the EXP-001D baseline.
4. **Policy freeze.** Fix belief models, gain estimator, acquisition eligibility, abstention rule and
   all non-VoI comparators. No selection may use 2023 outcomes.
5. **Utility/cost freeze.** Declare the complete assumption grid and sensitivity ranges. Label every
   scenario as non-buyer-elicited until interviews become possible.
6. **Single validation use.** Evaluate the new block once on the 2,243 issuers from 2022. Do not
   retune the frozen EXP-001D baseline on this cohort. Record any protocol changes and, if they are
   material, do not call the later test confirmatory without a new lock.
7. **Analysis freeze.** Fix the primary NDV comparison, bootstrap unit and draws, subgroup and
   missingness analyses, failure rules, software environment and analysis-script hash.
8. **Vault decision.** Only after all preceding artifacts are immutable may the 914-case 2023 label
   vault be opened for one evaluation. Report every declared baseline and sensitivity regardless of
   direction.

The future gate remains stringent: the cost-aware policy must exceed every declared non-VoI baseline,
and the paired interval against the strongest comparator must exclude zero under the declared
robustness conditions. A failure narrows the method claim; costs, utilities or comparators must not be
changed post hoc to manufacture a pass.

Buyer interviews can occur later when PhD or institutional-partner access exists. Until then, even a
future statistical pass would establish robustness only across the frozen assumption grid. It would
not demonstrate buyer economics, improved real VC decisions or commercial demand.

## 10. Reproducibility, ethics and data availability

The empirical base uses official public SEC Form D quarterly datasets and open-source Python code.
Raw and processed data remain local and git-ignored; the repository versions dataset definitions,
feature rules, experiment configurations, reports and hashes. Historical reconstruction is generated
by `code/build_sec_formd_dataset.py` and `code/enrich_formd_cohort.py`. EXP-001A through EXP-001D have
separate executable scripts, configurations and result artifacts. EXP-001D produced byte-identical
results on rerun; its recorded result hash is
`dffc2ff84bfde9e7d4671fd9e8928b0481c577805d2d1dd7be544e718e3e982c`.

**Reproducibility is checked, not asserted.** `code/verify_p1_reproducibility.py` hashes every
diagnostic result artefact, re-runs the experiment and compares. All seven reproduce byte-identically;
the manifest with per-experiment SHA-256 digests is `experiments/P1_REPRODUCIBILITY.json`.

The first run of that check **failed on two of seven**, and the cause is worth recording because it is
invisible to a fixed seed. The entity-resolution pair construction supporting §6.1 iterated over Python
sets of strings. String hashing is randomised per interpreter process, so the blocking lists were built
in a different order on every run and the truncated sample of hard negatives differed, moving the
reported balanced accuracies by roughly 0.2 percentage points. A seed does not protect against this. The
iteration points are now sorted, both experiments reproduce, and the §6.1 figures quoted above are the
post-fix values; the qualitative conclusion — a ceiling near 81%, with the pointwise maximum of seven
matchers failing to beat the best single one — is unchanged. Any earlier reading of those two artefacts
should be treated as a draw from a distribution rather than a fixed result.

The diagnostic experiments in §§4.5–4.9 reuse EXP-001C's configuration and seed unchanged, so they
describe that experiment rather than variants of it, and each is deterministic given that seed. Their
declared thresholds and, where applicable, their pre-run directional expectations are written in the
module docstrings before execution, which is what allows a correct prediction to be distinguished from a
retrospective explanation. Two bookkeeping defects are recorded rather than corrected silently. Two
experiments were both numbered EXP-005 and wrote the same results file, so the second run destroyed the
first artefact; the entity-resolution experiment now writes to `experiments/EXP-005-ER/` and was re-run
to restore it, while the value-of-information experiment retains the number cited throughout. And
EXP-006 held result artefacts without a report until 2026-07-29. Neither affects a reported number, and
both are the class of defect that makes a record irreproducible if left unlogged.

The future lock separates features from outcomes. Operational copies contain null outcomes for 2023;
the local label vault and locked feature file have recorded checksums, and key drift causes the
pipeline to fail rather than silently rebuild the holdout. This paper reports only non-outcome test
count and lock metadata.

Data minimization excludes related persons, signatures, recipients, phone numbers and street
addresses. Corporate identity and coarse geography are retained only for cohort construction and
entity-resolution audit. No LinkedIn scraping, proprietary commercial dataset or unofficial source
mirror is used. No USPTO credential is requested, transmitted or stored. These controls reduce but
do not eliminate risks from entity mismatch, public-record aggregation or downstream misuse.

The study does not automate investment decisions. Any later deployment would require human review,
source-level provenance, access control, retention rules and separate evaluation of automation bias,
fairness and institutional compliance.

## 11. Conclusion

This study reframes private-market diligence from outcome prediction to a sequential resource
allocation problem: acquire information only when its expected decision benefit exceeds its total
cost. The contribution is a falsifiable object—Net Decision Value—combined with point-in-time source
gates, explicit abstention and preservation of negative results.

The evidence is deliberately mixed. A learned cost-aware policy shows a small, non-universal
advantage in synthetic worlds. SEC Form D information carries temporal predictive signal, and issuer
history transports from 2021 to a company-disjoint 2022 cohort. Yet the first real selective-
acquisition policy passes none of its 15 declared utility-by-cost gates. Predictive usefulness,
uncertainty reduction and acquisition value are therefore empirically distinct in this setting.

The diagnostic sequence turns that negative result into a condition. An oracle bound places a winning
selective policy inside the reachable set, so the utility and cost grids are not the constraint. Two
repairs then fail in instructive ways: the capacity-constrained slice is too small to estimate the
relevant mean, with the median null divergence equal to the whole quantity; and targeting the incidence
of a decision change reaches ROC-AUC 0.950 yet still clears no gate, because incidence is orthogonal to
whether a change helps. What selective value of information requires is the **direction** of a decision
change, not its incidence, and direction is the base model's residual—so the condition binds wherever
base-model accuracy is modest.

The defensible conclusion is not that VoI already improves venture-capital decisions. It is that an
open-only research design can identify when an information block belongs in the baseline, reject a
selective policy that does not clear its costs, locate *why* it fails rather than only that it failed,
and protect a future test from iterative overfitting. The next claim depends on a qualitatively
different point-in-time-safe block and a fully frozen protocol; that block is also what would test the
condition's generality, since the condition currently rests on one. Buyer elicitation remains necessary
before translating assumption-bound NDV into real investment or commercial value.

We note one methodological practice that changed a conclusion within this paper and would generalise
cheaply. A null ordering, costing four lines of code, overturned an interpretation we had written the
same day (§4.7). Any estimate restricted to a subset selected by a score should be reported against a
calibrated null of arbitrary subsets of the same size, because at small subset sizes the two are not
distinguishable by inspection.

## Repository and official-source references

This evidence-building draft does not yet claim a complete scholarly literature review. §1.1 positions
the contribution against verified prior art at abstract level and flags two unverified entries. The
entries below are the auditable artifacts and official data documentation directly used; no
bibliographic citation has been inferred or fabricated.

### Scholarly references cited in §1.1

Verified bibliographically; differentiation written from abstracts, not from complete readings.

- Chaloner, K. and Verdinelli, I. "Bayesian Experimental Design: A Review." *Statistical Science*,
  1995. https://doi.org/10.1214/ss/1177009939
- Rainforth, T. et al. "Modern Bayesian Experimental Design." arXiv:2302.14545.
- Javdani, S. et al. "Near-Optimal Bayesian Active Learning with Noisy Observations."
  arXiv:1010.3091.
- Ma, C. et al. "EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE."
  arXiv:1809.11142.
- Golovin, D. and Krause, A. "Adaptive Submodularity: Theory and Applications in Active Learning and
  Stochastic Optimization." *Journal of Artificial Intelligence Research* 42, 2011. arXiv:1003.3967.
  Cited in §4.5 for a condition that is vacuous in this design.
- Alur, R., Laine, L., Li, D. K., Raghavan, M., Shah, D. and Shung, D. "Auditing for Human Expertise."
  arXiv:2306.01646. Nearest methodological neighbour to §8.6.
- Gompers, P., Gornall, W., Kaplan, S. N. and Strebulaev, I. A. "How Do Venture Capitalists Make
  Decisions?" *Journal of Financial Economics*, 2020. https://doi.org/10.1016/j.jfineco.2019.06.011
- "A Leakage-Controlled, Calibration-First Evaluation of Machine Learning Models for Startup-Outcome
  Prediction." *Information*, 2026. https://www.mdpi.com/2078-2489/17/7/702
- Dong, W., Saar-Tsechansky, M. and Geva, T. "A Machine Learning Framework for Assessing Experts'
  Decision Quality." *Management Science* 71(7):5696–5721, 2025.
  https://doi.org/10.1287/mnsc.2021.03357 Preprint: arXiv:2110.11425, titled "A Machine Learning
  Framework Towards Transparency in Experts' Decision Quality".
- VCBench. "VCBench: A Benchmark for Founder-Success Prediction." arXiv:2509.14448; live leaderboard at
  https://vcbench.com/ Cited as existing prior art in §1.1; no first-benchmark claim is made anywhere
  in this paper, and no numerical comparison to it is drawn.

Source descriptions above are paraphrased. Both entries previously listed as unverified were supplied
and confirmed on 2026-07-29; the *Management Science* article is 2025, not 2024 as recorded in earlier
internal notes, and that correction has been propagated.

- Private-Market-AI. `docs/Theory.md`; `docs/protocols/P1_VoI_Protocol.md`; and
  `datasets/P1_DATA_CONTRACT.md`. Current repository artifacts.
- Private-Market-AI. `experiments/EXP-001A/REPORT.md` through
  `experiments/EXP-001D/REPORT.md`. Frozen experiment reports.
- Private-Market-AI. `experiments/EXP-002/REPORT.md` (tail lift), `experiments/EXP-005/REPORT.md`
  (oracle decomposition), `experiments/EXP-007/REPORT.md` (slice restriction, carrying its own
  retraction), `experiments/EXP-008/REPORT.md` (null ordering and decile profile),
  `experiments/EXP-009/REPORT.md` (calibrated null and change targeting),
  `experiments/EXP-010/REPORT.md` (synthetic mechanism sweep with a declared falsification gate, and a
  refuted authorial prediction). Diagnostic sequence reports.
- Private-Market-AI. `experiments/EXP-005-ER/` and `experiments/EXP-006/REPORT.md`. Entity-resolution
  difficulty and the measured string-matching ceiling supporting §6.1.
- Private-Market-AI. `code/exp005_why_voi_fails.py`, `code/exp007_topk_transfer.py`,
  `code/exp008_where_gain_lives.py`, `code/exp009_change_targeting.py`, `code/tail_lift.py`.
  Executable analyses; declared thresholds and pre-run expectations appear in each module docstring.
- Private-Market-AI. `datasets/P1_DATASET_CARD.md`, `datasets/P1_SOURCE_AUDIT.md`,
  `datasets/P1_SBIR_BLOCK_AUDIT.md`, `datasets/P1_USPTO_BLOCK_AUDIT.md`, and
  `datasets/P1_FUTURE_COHORT_LOCK.md`. Data and source-audit artifacts.
- U.S. Securities and Exchange Commission. [Form D Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets),
  [Form D frequently asked questions](https://www.sec.gov/about/divisions-offices/division-corporation-finance/frequently-asked-questions-answers-form-d),
  and [Form D dataset guide](https://www.sec.gov/files/Form_D.pdf).
- SBIR.gov. [Data resources](https://www.sbir.gov/data-resources).
- USPTO Open Data Portal. [PatentsView transition guide](https://data.uspto.gov/support/transition-guide/patentsview),
  [registration requirements](https://data.uspto.gov/support/universal-registration), and
  [bulk-data product API](https://data.uspto.gov/apis/bulk-data/product).
- OpenAlex. [API overview](https://docs.openalex.org/how-to-use-the-api/api-overview) and
  [snapshot overview](https://docs.openalex.org/download/overview).

External-source descriptions are paraphrased. No more than the source facts necessary to document
access and temporal-validity decisions are reproduced.