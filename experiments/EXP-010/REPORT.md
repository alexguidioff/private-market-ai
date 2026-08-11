# EXP-010 — Is the §8.6 condition a mechanism, or an artefact of one cohort?

**Date:** 2026-07-29
**Script:** `code/exp010_condition_sweep.py` · **Artefacts:** `results.json`, `stdout.txt`
**Tests:** the largest declared threat to P1's central claim — that §8.6 rests on one
information block, one cohort and one weak proxy
**Design:** 15 grid cells × 40 synthetic worlds × 1,500 cases; two costs per cell

## Question and gate

§8.6 claims selective value of information requires the *direction* of a decision
change to be predictable, not merely its incidence. A second real information block
is blocked on four independent source gates, so the claim's generality cannot be
tested with real data. In synthetic worlds the hidden truth is ours to set, so the
two quantities the condition names can be varied independently.

Two knobs, both swept: `lam` scales how strongly the base features predict the
acquirable signal, and `base_strength` scales how much the base features explain the
outcome. The falsification gate was declared before running:

> A cell **refutes** §8.6 if the learned selective policy beats the strongest
> non-VoI baseline by more than 0.010 with a paired bootstrap interval over worlds
> excluding zero, *while* corr(predicted, realised gain) exceeds 0.05.

## Result: 0 of 30 tests refute, and the margin is not close

| base_str | lam | base AUC | changed | prize | corr | learned adv. (cost 0) |
|---:|---:|---:|---:|---:|---|---|
| 0.30 | 0.0 | 0.614 | 21.0% | +0.0276 | +0.060 [+0.033, +0.090] | −0.0040 [−0.0069, −0.0017] |
| 0.30 | 0.5 | 0.625 | 19.8% | +0.0279 | +0.016 [−0.013, +0.046] | −0.0036 [−0.0056, −0.0018] |
| 0.30 | 1.0 | 0.656 | 16.9% | +0.0277 | +0.006 [−0.023, +0.031] | −0.0026 [−0.0045, −0.0011] |
| 0.30 | 1.5 | 0.661 | 14.8% | +0.0204 | +0.014 [−0.009, +0.040] | −0.0061 [−0.0093, −0.0033] |
| 0.30 | 2.5 | 0.652 | 13.7% | +0.0129 | +0.025 [+0.005, +0.044] | −0.0042 [−0.0066, −0.0020] |
| 0.65 | 0.0 | 0.742 | 15.6% | +0.0231 | +0.056 [+0.032, +0.082] | −0.0018 [−0.0035, −0.0002] |
| 0.65 | 0.5 | 0.711 | 14.0% | +0.0160 | +0.049 [+0.029, +0.072] | −0.0041 [−0.0083, −0.0012] |
| 0.65 | 1.0 | 0.718 | 14.3% | +0.0228 | +0.038 [+0.020, +0.059] | −0.0046 [−0.0070, −0.0026] |
| 0.65 | 1.5 | 0.726 | 13.4% | +0.0193 | +0.024 [−0.002, +0.051] | −0.0027 [−0.0046, −0.0009] |
| 0.65 | 2.5 | 0.731 | 11.1% | +0.0124 | +0.007 [−0.012, +0.026] | −0.0043 [−0.0070, −0.0020] |
| 1.20 | 0.0 | 0.824 | 12.3% | +0.0141 | +0.027 [+0.009, +0.047] | −0.0054 [−0.0077, −0.0033] |
| 1.20 | 0.5 | 0.801 | 12.3% | +0.0125 | +0.030 [+0.012, +0.047] | −0.0052 [−0.0083, −0.0027] |
| 1.20 | 1.0 | 0.840 | 10.0% | +0.0111 | +0.037 [+0.020, +0.053] | −0.0030 [−0.0050, −0.0013] |
| 1.20 | 1.5 | 0.827 | 8.8% | +0.0138 | +0.029 [+0.012, +0.048] | −0.0048 [−0.0073, −0.0025] |
| 1.20 | 2.5 | 0.834 | 8.8% | +0.0099 | +0.001 [−0.023, +0.027] | −0.0064 [−0.0091, −0.0039] |

The learned advantage is **negative in all 15 cells at both costs**, with the
bootstrap interval over worlds excluding zero in every one. The selective policy is
not merely failing to beat the best fixed baseline; it is reliably worse than it
across the entire grid, in worlds where the model class is correctly specified.

**The conclusion does not depend on the gate's conjunction.** The gate required a
large advantage *and* a correlation above the floor, which is a conjunction that a
low-correlation cell cannot satisfy however it behaves. That would be a weakness if
the advantage branch ever fired. It does not: zero cells reach an advantage above
+0.010 irrespective of correlation, so the result is driven by the advantage alone.

**A prize existed in every cell.** The oracle advantage runs from **+0.0217 to
+0.0562**, acquiring 60% to 76% of cases. So a winning selective policy exists in
principle everywhere on the grid, exactly as EXP-005 found on real data. The
synthetic worlds reproduce the real-data structure — large oracle gap, zero learned
gap — which is itself the point of running them.

## One declared prediction confirmed, one refuted

**Confirmed: the prize falls on both axes.** The share of cases where acquiring
changes the decision falls from 21.0% to 13.7% as `lam` rises at low base strength,
and from 21.0% to 12.3% as `base_strength` rises at `lam` = 0. Mean realised gain
falls correspondingly, from +0.0276 to +0.0099 across the grid's diagonal. Both
directions were declared in advance.

**Refuted: my stated mechanism was wrong.** I predicted the correlation between
predicted and realised gain would *rise* with `lam`, on the reasoning that a base
state anticipating the block would make the direction of a change predictable. It
does the opposite. At `base_strength` 0.65 the correlation falls monotonically
across the whole sweep — 0.056, 0.049, 0.038, 0.024, 0.007 — and the pattern is
flat-then-falling at the other two strengths.

The corrected mechanism is **worse for selective acquisition than the one I
proposed**, which is why the error is worth recording rather than smoothing over. I
had hypothesised a trade-off frontier: predictable direction with a small prize at
one end, a large prize with a blind selector at the other. There is no frontier.
When the base state anticipates the block, the prize shrinks *and* the direction
becomes **less** predictable, because the quantity being predicted becomes rare and
its estimate is then dominated by noise. Both terms degrade together.

**Where the small correlation actually comes from.** The largest correlations sit at
`lam` = 0, where the base state carries no information about the signal at all —
the cell where my mechanism predicts the *lowest* correlation. The coherent reading
is that this residue is incidence rather than direction: with `lam` = 0 the signal
is independent of the base state, acquiring changes the decision in 21% of cases,
and those cases are the ones near the decision boundary, which *is* predictable from
the base state alone. So the gain model is partly detecting which cases will change,
not which changes will help. That is EXP-009's finding reproduced in a setting where
we control the generator, and it is the strongest corroboration in this experiment:
the same 0.05-ish correlation that fails to convert on real data also fails to
convert here, and for the same reason.

## What this establishes, and what it does not

**Establishes:** the condition in §8.6 behaves as a mechanism across a
two-dimensional sweep of the quantities it names, with the learned policy
significantly worse than the best fixed baseline in 30 of 30 tests while an oracle
prize existed in all of them. The condition is not an artefact of the SEC cohort's
particular block, base rate or proxy.

**Does not establish** that it holds for a qualitatively different real block. The
generator is logistic and so is the learner, so the model class is correctly
specified — a luxury real data does not provide. A misspecified base model could in
principle leave a structured residual that a gain model exploits, and this design
cannot see that. The second real block remains the outstanding test and this
experiment does not substitute for it.

## Threats to validity

**Correctly specified model class.** The strongest limitation, stated first. Both
the outcome and the signal are generated by logistic models and both learners are
logistic, so no functional-form mismatch exists anywhere in the grid.

**One gain estimator.** Ridge on base features plus the base probability and its
entropy, matching EXP-001C. A different estimator is not tested, and the same
caveat EXP-001C carries applies here.

**One utility matrix.** The payoff matrix is EXP-001A's, so the sweep varies the
world and not the preferences. EXP-005 showed the real-data diagnosis holds across
three matrices, but this experiment does not re-establish that.

**Grid boundaries are declared, not searched.** `lam` up to 2.5 and
`base_strength` up to 1.2, giving base AUC from 0.614 to 0.840, which spans and
exceeds the 0.59–0.65 range observed on real data. No cell was added after seeing a
result. A refutation could still live outside these bounds.

**Bootstrap unit is the world**, not the case, which is the correct unit for a claim
about worlds and gives wider intervals than a case-level bootstrap would.

## Reproduction

```bash
python code/exp010_condition_sweep.py
```

Deterministic given `SEED = 20260729` in the module.
