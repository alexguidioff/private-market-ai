# EXP-008 — Where is information worth buying, and was EXP-007's divergence real?

**Date:** 2026-07-29
**Script:** `code/exp008_where_gain_lives.py` · **Artefacts:** `results.json`, `stdout.txt`
**Corrects:** `experiments/EXP-007/REPORT.md` — see §3, which is the most important
section in this file

## Question

EXP-007 found the mean per-case gain rising monotonically as the pipeline slice
widens and read it as "information is worth most where the base model is least
confident". That reading did not follow: the slices are nested and ranked by
predicted probability descending, so widening from the top mixes in the uncertain
middle *and* the confident-negative bottom at once. Two hypotheses were declared
before running, with an explicit statement that I could not predict which held:

* **H-uncertainty** — gain peaks mid-probability, small at both extremes.
* **H-descending** — gain rises as probability falls, largest in the bottom decile.

A random ordering was included as a control so that the size of a null divergence
would be visible on the same table as the real ones. That control is what makes this
report a correction rather than a continuation.

## 1. Under `balanced`, gain is concentrated in the lower-middle of the range

| decile | p range | mean gain | nonzero |
|---:|---|---|---:|
| 1 | 0.053–0.148 | +0.0272 [−0.0136, +0.0707] | 9.8% |
| 2 | 0.148–0.195 | +0.0055 [−0.0492, +0.0656] | 18.6% |
| 3 | 0.196–0.230 | +0.0710 [+0.0000, +0.1421] | 25.1% |
| **4** | 0.231–0.254 | **+0.0984 [+0.0191, +0.1831]** | 29.5% |
| 5 | 0.254–0.274 | +0.0301 [−0.0628, +0.1230] | **56.3%** |
| 6 | 0.274–0.296 | +0.0246 [−0.0464, +0.0902] | 33.3% |
| 7 | 0.297–0.318 | +0.0191 [−0.0301, +0.0628] | 16.9% |
| 8 | 0.318–0.341 | −0.0082 [−0.0546, +0.0301] | 9.3% |
| 9 | 0.341–0.371 | +0.0109 [−0.0164, +0.0328] | 4.4% |
| 10 | 0.372–0.474 | +0.0055 [+0.0000, +0.0137] | 1.1% |

Middle four deciles +0.0430 against extremes +0.0123, a gap of +0.0308 which clears
the declared 0.010 margin, so the shape classifier returns H-uncertainty over
H-descending. The share of cases where acquiring changes the decision peaks at 56.3%
in decile 5, which is the mechanism one would expect: the two models disagree most
where the base model is least committed.

**Two reasons not to lean on this.** The monotonicity test gives Spearman −0.479 with
**p = 0.174**, so no monotone trend is established — consistent with a peak, but it
means EXP-007's "monotonic" description was not supported either. And exactly **one**
of ten decile intervals excludes zero, with no multiplicity correction across ten
bins, which is what chance produces.

## 2. The shape does not replicate across utilities

Agenda check (a) fails. `false_positive_averse`: Spearman +0.139, p = 0.715, middle
minus extremes −0.0171, shape unclassified. `opportunity_averse`: Spearman +0.091,
p = 0.814, and deciles 4 through 10 have mean gain of exactly zero — all of the
action sits in the bottom two deciles. Whatever structure exists under `balanced` is
a property of that payoff matrix, not of the cohort.

## 3. The correction: EXP-007's divergence is not distinguishable from noise

This is the finding that matters and it goes against the previous report.

| ordering | top 5% | top 10% | top 20% |
|---|---|---|---|
| base probability (EXP-007's) | −0.0230 * | −0.0229 * | −0.0202 |
| offering size | −0.0012 | −0.0175 | −0.0188 |
| investor count | −0.0393 | −0.0339 | −0.0202 |
| **random (control)** | **−0.0936 \*** | −0.0503 | −0.0120 |

`*` = bootstrap interval on (slice mean − cohort mean) excludes zero. Under
`balanced`, cohort mean +0.0284.

**A random ordering produces a larger divergence than any real one.** Across all
three utilities, real orderings diverge in 4 of 36 cells and the random control in 1
of 9 — the same rate. With 92 cases and a per-case standard deviation of 0.41 the
standard error on a top-5% mean is about 0.043, so an arbitrary subsample of that
size routinely differs from the cohort by more than the cohort mean itself.

**What EXP-007 actually established, restated.** Not that the slice mean *differs*
from the cohort mean — the control shows that claim cannot be supported at this slice
size. What it established is that the slice mean **cannot be estimated** there. That
is a precision statement rather than a bias statement, and EXP-007's own threats
section contained the arithmetic ("the standard error is five times the quantity
being tested") without applying it to its own headline. This report applies it.

The one thing that survives, weakly: the probability ordering diverges with the same
sign at both 5% and 10% while the control diverges at 5% only. Consistency across
nested slices is *some* evidence of a real effect, and nested slices share most of
their data, so it is weak evidence and should be called that.

## 4. A design error in this experiment, recorded

The ranking "base uncertainty, most-unsure first" returned numbers **identical** to
"base probability, descending". The reason is not a coincidence: the base model never
predicts above 0.474, so every case sits below 0.5, and `-|p − 0.5|` reduces to
`p − 0.5`, a monotone increasing function of `p`. The two rankings are the same
ordering.

So agenda check (b) was run with **two** genuinely independent alternatives — offering
size and investor count — plus the control, not four. And the uncertainty hypothesis
in §1 could not be tested by the ranking route at all, only by the decile profile.
A model whose predictions never cross the decision boundary is worth noting in its
own right: with a 29.2% base rate and a maximum predicted probability of 0.474, the
base model never asserts that an outcome is more likely than not.

## What follows for P5

**The compounding caution is unresolved, not confirmed.** EXP-007 was written as a
confirmation; the control says the divergence is inside noise. The honest position is
that at this cohort size the slice-restricted trade-off is unmeasurable, so neither
transfer nor failure of transfer is established.

**That is still decision-relevant, and arguably more so.** P5's budgeted formulation
needs a quantity estimated on 5–10% of the pipeline. On this cohort that is 92–183
cases against a per-case standard deviation of 0.41. The estimation problem, not the
transfer question, is the binding constraint, and no amount of method design fixes a
standard error. P5 needs either a materially larger cohort, an outcome with lower
variance, or a formulation that does not require a slice-restricted mean.

**Where to look next, direction declared:** gain concentrates where the two models
disagree, and disagreement is observable *without the outcome* — it is
`|p_base − p_full|`, which requires the block but not the label. If the share of
decision changes is predictable from base-state features, that reopens targeting
without reopening the per-case gain model EXP-005 closed, because predicting *whether
the action changes* is a different and easier quantity than predicting whether the
change helps. Stated as a hypothesis; the obvious objection is that knowing the
action changes says nothing about the direction, which is exactly what EXP-005 found
unpredictable.

## Threats to validity

**Ten bins, no multiplicity correction.** One decile interval excludes zero, which is
the expected count under the null. The shape classification rests on the aggregated
middle-versus-extremes contrast rather than on any single bin, which is why that
contrast was declared in advance.

**The control is one draw.** A single random ordering was used per utility. A stronger
design would draw many random orderings and report the distribution of divergences,
which would give a calibrated threshold instead of one comparison point. That is a
real weakness of this experiment and the fix is cheap.

**Realised gain uses the outcome**, as in EXP-005 and EXP-007. Everything here
describes where gain *is*, not where it can be predicted to be.

**One block, one cohort, weak proxy.** Agenda check (c) — a second, qualitatively
different information block — is not addressed. It remains the standing threat to
this whole line, and nothing in EXP-007 or EXP-008 reduces it.

## Reproduction

```bash
python code/exp008_where_gain_lives.py
```

Deterministic given the seed in `experiments/EXP-001C/config.json`.
