# EXP-009 — A calibrated null for slice estimates, and why change-targeting fails anyway

**Date:** 2026-07-29
**Script:** `code/exp009_change_targeting.py` · **Artefacts:** `results.json`, `stdout.txt`
**Completes:** EXP-008's two open items — a proper null for slice claims, and the
objection to the change-targeting hypothesis
**Sharpens:** P1's v0.4 claim, in a way that makes it harder to dismiss

## Part A — the calibrated null, and what it does to EXP-007

EXP-008 compared one real ordering against one random ordering. Four hundred random
orderings per utility give a threshold instead of a comparison point.

| utility | slice | n | null sd | median \|divergence\| | 95th pct | max |
|---|---|---:|---:|---:|---:|---:|
| balanced | 5% | 92 | 0.0427 | **0.0284** | 0.0882 | 0.1262 |
| balanced | 10% | 183 | 0.0267 | 0.0202 | 0.0530 | 0.0803 |
| balanced | 20% | 366 | 0.0190 | 0.0126 | 0.0366 | 0.0680 |

**The cleanest statement of the sample-size problem this project has produced:** the
cohort mean gain under `balanced` is **+0.0284**, and the *median* divergence of an
arbitrary top-5% slice is **0.0284**. At the slice size a budget works, the typical
meaningless deviation is exactly the size of the entire quantity being estimated.

EXP-007's −0.0230 does not come close to the 0.0882 threshold. That confirmation is
now quantitative rather than a single comparison.

**Across 27 ordering-by-slice cells, 3 clear the null.** All three sit under
`false_positive_averse`: offering size at 5% (+0.1004) and 10% (+0.0559), and base
probability at 10% (+0.0668). With a 5% threshold on 27 cells the expected false
count is 1.35, so 3 is not compelling. Two of them are the same ranking at two nested
slice sizes with the same sign, which is mildly more interesting than a single hit and
still weak, because nested slices share most of their data. Recorded as a lead, not a
finding: **deal size may carry slice-level structure under a false-positive-averse
utility.**

## Part B — the objection, tested first as declared

My predictions were written into the script docstring before running.

| utility | action changes | E[gain \| change] | helped |
|---|---:|---|---:|
| balanced | 20.4% (n=374) | +0.139 | 64% |
| false_positive_averse | 13.4% (n=245) | −0.0602 [−0.1980, +0.0796] | **42.0%** |
| opportunity_averse | 4.9% (n=89) | +0.0618 [−0.0927, +0.2079] | 82.0% |

Predicted: positive under `balanced`, negative under `false_positive_averse`, and
"roughly 42%" helped in the latter. All three correct, the last one to the decimal,
because it was derived arithmetically from EXP-005's reported 5.6% against 7.8%
rather than guessed. The product check reproduces the cohort mean exactly in all three
cases, which is the decomposition's internal consistency test.

So the objection is **not** fatal in the form I stated it. A decision change is worth
something, the sign is stable within a utility, and the utility is chosen by the
investor before acquiring. The hypothesis survives its first test.

## Part B — the hypothesis holds its premise, and still loses

The premise was that predicting *whether* the action changes is easier than predicting
whether the change helps, because it discards the direction. That is not a small
effect:

| utility | change-indicator AUC | EXP-005's corr(predicted, realised gain) |
|---|---:|---:|
| balanced | **0.770** | +0.015 |
| false_positive_averse | 0.679 | −0.070 |
| opportunity_averse | **0.950** | +0.000 |

The intermediate quantity is predictable, in one case almost perfectly.

**And the policy wins 0 of 15 cells.** Best advantage anywhere is +0.0025 with an
interval spanning zero, against a declared margin of 0.005.

| utility | cost | acquires | vs strongest | advantage |
|---|---:|---:|---|---|
| balanced | 0.0 | 94.6% | cheapest | −0.0005 [−0.0025, +0.0008] |
| balanced | 0.025 | 75.8% | cheapest | +0.0025 [−0.0025, +0.0065] |
| balanced | 0.05 | 15.2% | none | −0.0027 [−0.0134, +0.0082] |
| false_positive_averse | 0.01 | 26.1% | none | +0.0022 [−0.0109, +0.0149] |
| opportunity_averse | 0.025 | 5.9% | none | +0.0025 [−0.0023, +0.0076] |

## Why it loses, and why this matters more than EXP-005

EXP-005's negative result was open to one dismissal: *your gain model was bad*. That
dismissal is unavailable here. The intermediate quantity is predicted at AUC 0.77 to
0.95 and the policy still does not convert it into decision value.

The reason is structural and specific. The policy scores each case as

```text
expected gain = P(action changes) x E[gain | change]
```

with the second term a population constant. It therefore concentrates acquisition on
cases where the action is *likely to change* — but among changes, 64% help and 36%
hurt under `balanced`, and that mix does not vary with P(change). Buying more
probability-of-change buys proportionally more helpful *and* more harmful changes. The
policy purchases action, not correctness.

**This sharpens P1's v0.4 claim in a way worth writing into the paper.** The claim
currently reads: selective value of information requires per-case gain to be more
predictable than the outcome. EXP-009 makes it more precise and more useful:

> It is not enough for the **incidence** of a decision change to be predictable. The
> **direction** must be. Incidence can be predicted at AUC 0.95 while direction stays
> at r ≈ 0, and targeting on incidence then scales the harmful changes at the same
> rate as the helpful ones.

That is a transferable statement about any value-of-information application, and it is
sharper than the original because it names the quantity that looks like a solution and
explains why it is not.

**Symptom worth recording.** The policy has almost no dynamic range: at cost 0 it
acquires 94.6% of cases, at cost 0.05 it acquires 15.2%, at cost 0.1 it acquires 0.1%.
Since the score is `P(change)` times a constant, it is a tightly-distributed quantity
crossing the whole cost grid over a narrow band, so the policy is close to
all-or-nothing with a threshold, which is precisely what EXP-005 said the right policy
in this regime is.

## What follows

* **The change-targeting route is closed**, and closed more informatively than the
  per-case gain route. Log it so it is not silently resumed.
* **P1's discussion gains a sharper version of its central condition**, stated above.
  This is the strongest single sentence to come out of EXP-005 through EXP-009 and it
  belongs in the working paper.
* **One lead survives from Part A:** offering size clears the calibrated null at two
  nested slices under `false_positive_averse`. Weak, unadjusted for multiplicity, and
  the only structure in 27 cells. Worth one targeted test, not a research direction.
* **The slice-size arithmetic is now unambiguous.** Median null divergence equals the
  cohort mean at 5%. No method fixes this; P5 needs a larger cohort, a lower-variance
  outcome, or a formulation that avoids slice-restricted means.

## Threats to validity

**Multiplicity in Part A.** 27 cells at a 5% threshold, 3 clearing, 1.35 expected. No
correction applied, and the three hits are reported as a lead precisely because they
would not survive one.

**E[gain | change] intervals are wide.** Under `false_positive_averse` the interval
[−0.1980, +0.0796] spans zero, so the negative sign is a point estimate. The
prediction was right about the sign; the evidence for it is weak on its own and rests
partly on agreeing with EXP-005's independent decomposition.

**The policy uses a constant value-of-change estimated on train.** A richer policy
could model `E[gain | change, x]` — but that is per-case gain conditional on a change,
which is the quantity EXP-005 found unpredictable, restricted to a smaller sample. The
structural argument says this does not help; it has not been run.

**Realised gain uses the outcome** in Parts A and the objection test. The policy in
the hypothesis test does not: it is evaluated on NDV with a train-fitted change model,
so that part is a legitimate out-of-sample policy comparison.

**One block, one cohort, weak proxy.** Unchanged and still the standing threat.
Nothing in EXP-007, EXP-008 or EXP-009 addresses it.

## Reproduction

```bash
python code/exp009_change_targeting.py
```

Deterministic given the seed in `experiments/EXP-001C/config.json`.
