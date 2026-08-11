# EXP-005 — Why the cost-aware acquisition policy fails its gates

**Date:** 2026-07-29
**Script:** `code/exp005_why_voi_fails.py` · **Artefacts:** `results.json`
**Status:** complete; diagnoses EXP-001C without re-running or altering it

## Question

EXP-001C reported that a learned selective acquisition policy passes **0 of 15**
declared utility-by-cost scenarios against the strongest non-VoI baseline. Three
explanations were carried forward unseparated:

```text
(a) misspecified utility model
(b) a cost regime where acquisition genuinely does not pay
(c) failure of the structural conditions licensing adaptive greedy acquisition
```

Nothing in the original design distinguished them. This experiment does.

## A correction before any result: (c) was a category error

**Adaptive submodularity is vacuous in this design, and carrying it as a live
hypothesis was a mistake.** The condition (Golovin & Krause, JAIR 2011) licenses
near-optimality of adaptive *greedy* selection over a *sequence* of tests.
EXP-001C acquires **one** block under a **binary** decision. With a single item
there is no sequence, greedy reduces to "acquire iff expected gain exceeds cost",
which is trivially optimal *given a correct gain estimate*, and submodularity has
nothing to constrain.

The defensible third candidate is about the selection signal instead:

```text
(c') either per-case gain does not vary (nothing to select on),
     or its variation is not predictable from the base state (the selector is noise)
```

Selective acquisition can only beat all-or-nothing when **both** hold: gain is
heterogeneous, *and* that heterogeneity is predictable. These are separately
measurable, which (c) never was.

## Design

The decisive instrument is an **oracle policy**: acquire exactly where the
*realised* per-case gain exceeds cost. It uses the outcome, so it is not a policy —
it is the least upper bound on what any selective policy could achieve. It splits
the diagnosis:

| Oracle vs best baseline | Learned vs best baseline | Diagnosis |
|---|---|---|
| advantage below threshold | — | **problem-side**: no selective policy can win; the utility/cost regime is the constraint |
| advantage above threshold | ≈ 0 | **model-side**: a winning policy exists; this gain model cannot find it |
| advantage above threshold | above threshold | not a failure in that cell |

Thresholds declared before running, in normalised NDV units: oracle margin 0.010,
learned margin 0.005, signal floor |r| = 0.05. No cost or utility value was
adjusted afterwards. The base and acquired models are reproduced exactly from
EXP-001C, so this describes that experiment rather than a variant.

## Result

**13 of 15 cells are model-side. 2 are problem-side. Zero are policy wins.**

| Utility | Gain nonzero | Gain sd | corr(predicted, realised) | Oracle advantage | Learned advantage |
|---|---:|---:|---:|---:|---:|
| balanced | 20.4% (+13.1 / −7.3) | 0.4061 | **+0.015** | +0.065 to +0.087 | −0.004 to +0.003 |
| false_positive_averse | 13.4% (+5.6 / −7.8) | 0.4067 | **−0.070** | +0.064 to +0.070 | −0.004 to +0.003 |
| opportunity_averse | 4.9% (+4.0 / −0.9) | 0.1634 | **+0.000** | +0.009 to +0.012 | −0.000 to +0.003 |

### The answer

**The failure is neither (a) nor (b) nor (c). It is (c'), in its second form.**

* **Gain is genuinely heterogeneous.** Acquisition changes the realised decision in
  20.4% of cases under the balanced utility, helping in 13.1% and *hurting* in 7.3%,
  with a standard deviation of 0.41 against a mean of +0.028. There is a great deal
  to select on. Condition one holds.
* **The heterogeneity is not predictable.** Pearson correlation between predicted
  and realised per-case gain is **+0.015, −0.070 and +0.000** across the three
  utilities. Condition two fails.

  *Precision on the previous sentence, against my own first draft of it.* Spearman is
  **+0.055, −0.017 and +0.131**, so under two utilities the rank correlation clears the
  declared 0.05 floor and under `opportunity_averse` it clears it by 2.6x. "Selecting
  at chance" is therefore too strong: there is a faint monotone ordering that the
  linear coefficient does not see. It does not rescue anything — the learned advantage
  in those same cells is −0.000 to +0.003, i.e. still zero — but the honest statement
  is *the ordering is far too weak to act on*, not *there is none*. Recorded because a
  methods group will compute both coefficients.
* **A winning policy exists.** The oracle beats the strongest baseline by +0.065 to
  +0.087 under the two informative utilities — six to nine times the declared
  0.010 margin. So the problem is not that acquisition cannot pay. It is that this
  selector cannot tell where it pays.

### Why per-case gain is close to unpredictable, structurally

This is not a tuning failure and should not be treated as one. Per-case gain is

```text
gain_i = U(y_i, a_full_i) − U(y_i, a_base_i)
```

which is nonzero only when the two models choose **different actions** *and* the
realised outcome decides which was right. Predicting it therefore requires
predicting whether the base model's error will be corrected on that specific case —
which is predicting the base model's residual, i.e. predicting the outcome *better
than the base model does*. With base ROC-AUC around 0.59–0.65 on this weak proxy,
the gain model inherits that ceiling and then loses further to the extra variance.

Corroborating symptom of noise rather than signal, and it is worse than a single
mis-scaling. The predicted-gain dispersion misses the realised one **in both
directions depending on the utility**:

| Utility | sd(predicted) | sd(realised) | Ratio |
|---|---:|---:|---:|
| balanced | 0.0438 | 0.4061 | **0.11x** — ten times too flat |
| false_positive_averse | 0.1043 | 0.4067 | 0.26x |
| opportunity_averse | 0.6778 | 0.1634 | **4.15x** — four times too wild |

A model that is uniformly over- or under-confident is mis-scaled and can be
recalibrated. One whose dispersion is 0.11x the truth on one payoff matrix and 4.15x
on another, at zero correlation throughout, is not tracking the quantity at all. The
same features and the same learner produce opposite pathologies purely because the
utility changed. That is variance with no location, not weak learning.

### The two problem-side cells

`opportunity_averse` at cost 0.0 and 0.1 show oracle advantages of +0.0098 and
+0.0088, just under the 0.010 margin. Under that utility, acquisition changes the
decision in only 4.9% of cases, so there is little to win at any cost. Those two
cells are correctly read as "the regime does not pay", and they are the only ones.

## What follows for P1

**Stop trying to improve the gain model.** The oracle gap says a win exists; the
zero correlation says it is not reachable by predicting per-case gain from the base
state, because that is a harder problem than the prediction task itself. Better
regularisation, a richer meta-feature set or a stronger learner do not close a gap
that starts at r ≈ 0.

**The right policy in this regime is all-or-nothing, not selective — and under two of
the three utilities the correct answer is "nothing".** This is more specific than
"decide at the population level", because the population-level sign is not the same
everywhere:

| Utility | Mean per-case gain | All-or-nothing verdict at zero cost |
|---|---:|---|
| balanced | **+0.0284** | acquire for the whole cohort |
| false_positive_averse | **−0.0081** | acquire for nobody; the block *destroys* value on average |
| opportunity_averse | +0.0030 | indifferent, and negative once cost bites |

So the block is not weakly useful everywhere: under `false_positive_averse` buying it
makes decisions worse **before paying for it**, because it flips 7.8% of cases into
error against 5.6% into correctness. That is why `none` is the strongest non-VoI
baseline in 11 of the 15 cells. When you cannot tell *which* cases benefit, the only
estimable quantity is the population mean, and here it changes sign with the payoff
matrix — which means the utility function, not the selector, is what decides whether
to acquire at all.

**This is a positive result for P5, not just a negative one for P1.** It identifies
a condition under which selective, per-case value of information cannot work, and
that condition is stateable in general: *selective acquisition requires the
per-case gain to be more predictable than the outcome, and it usually is not.* The
budgeted-portfolio formulation in P5 does not need per-case gain — it needs the
population-level trade-off — which is precisely the quantity that is estimable here.

## Threats to validity

**The oracle is an upper bound, not a target.** It uses the outcome. Its advantage
proves a winning selective policy exists in principle; it does not imply any
implementable policy can reach it. The claim made is only the negative one: the
failure is not the utility or cost regime.

**One block, one cohort, weak proxy.** Single information block, 2016–2020 anchors,
outcome is a subsequent non-amendment Form D notice within 18 months. Whether the
same diagnosis holds for a qualitatively different block is untested.

**The meta-feature set is EXP-001C's.** The zero correlation is a property of that
feature set plus Ridge. A radically different representation of the base state
could in principle carry signal, though the structural argument above says it would
still be bounded by the difficulty of predicting the residual.

**Utility grid is assumed, not elicited.** As in EXP-001C. But note this cuts the
right way: the diagnosis holds across all three assumed utilities, so it does not
rest on one payoff matrix.

**Cost grid is normalised and assumed.** Also as in EXP-001C, and unchanged after
seeing the result.

## Reproduction

```bash
python code/exp005_why_voi_fails.py
```

Deterministic given the seed in `experiments/EXP-001C/config.json`.
