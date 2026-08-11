# EXP-007 — Does the cohort-level acquisition estimate reach the slice a budget works?

**Date:** 2026-07-29
**Script:** `code/exp007_topk_transfer.py` · **Artefacts:** `results.json`, `stdout.txt`
**Answers:** the compounding caution logged under P5 in `docs/Research_Agenda.md`
**Depends on:** EXP-005 (per-case gain unpredictable, population mean estimable),
EXP-002 (average and tail behaviour diverge on this cohort)

> ## ⚠️ Corrected by EXP-008 on 2026-07-29 — read this first
>
> This report's headline is **too strong** and the correction is left here rather than
> edited away.
>
> EXP-008 added a **random ordering as a control**. Under `balanced` a random top-5%
> slice diverges from the cohort mean by **−0.0936** with an interval excluding zero,
> which is *larger* than the −0.0230 reported below for the probability ordering.
> Across all utilities, real orderings diverge in 4 of 36 cells and the random control
> in 1 of 9 — the same rate. With 92 cases and a per-case standard deviation of 0.41,
> the standard error on a top-5% mean is about 0.043.
>
> **What this report should have concluded:** not that the slice mean *differs* from
> the cohort mean, but that at this slice size it **cannot be estimated**. A precision
> statement, not a bias statement. The arithmetic was already in the threats section
> below — "the standard error is about 0.042, five times the cohort mean being tested"
> — and I failed to apply it to my own headline, applying it only to the one utility
> where it was inconvenient.
>
> **Also corrected:** the monotonic rise described below as a "structural regularity"
> tests at Spearman −0.479 with **p = 0.174**, so no monotone trend is established. The
> decile profile in EXP-008 shows a peak in the lower-middle of the probability range
> instead, and that peak does not replicate under the other two utilities.
>
> The measurements below are reproducible and unchanged. The interpretation is
> superseded by `experiments/EXP-008/REPORT.md`.

## Question

P5 was promoted on the strength of one EXP-005 finding: per-case value of
information is not selectable, but the **population mean gain is estimable**, and it
changes sign with the utility. A budgeted pipeline needs the population trade-off,
not the per-case one.

EXP-002 established on the same cohort that average and tail behaviour diverge:
ROC-AUC 0.61 alongside 1.45x enrichment in the top 5%. A fund with limited attention
only ever works the top slice.

So P5's justifying quantity is measured over the whole cohort while the decision it
informs is taken inside a small slice of it. This experiment asks whether the number
survives the restriction.

Same two models as EXP-001C and EXP-005, unchanged. Test cohort 1,831 cases, base
rate 29.2%. Pipeline ranked by the base model's predicted probability, descending,
because that is the ordering available at the decision time without buying anything.

**Declared before running, and recorded here because it turned out right:** the top
of a probability ranking is where the base model is already confident, gain is
nonzero only where acquiring changes the action, and confident cases are the hardest
to move — so the slice mean should be *smaller* in magnitude than the cohort mean,
possibly changing sign where the cohort mean is already near zero.

Thresholds fixed before running: slices 5/10/20/50/100%, transfer margin 0.010 in
normalised NDV units (the same margin EXP-005 used), minimum slice size 30.

## Result

**7 sign flips, 2 magnitude shifts, 6 transfers out of 15 slice-utility cells. The
all-or-nothing decision changes in 20 of 75 cost-by-utility-by-slice cells.**

### `balanced` — the estimate shrinks fivefold, and this one is established

| slice | n | mean gain | vs cohort | verdict |
|---|---:|---|---|---|
| 5% | 92 | +0.0054 [+0.0000, +0.0163] | **−0.0230 [−0.0434, −0.0019]** | magnitude shift |
| 10% | 183 | +0.0055 [+0.0000, +0.0137] | **−0.0229 [−0.0434, −0.0044]** | magnitude shift |
| 20% | 366 | +0.0082 [−0.0041, +0.0191] | −0.0202 [−0.0404, +0.0003] | transfers |
| 50% | 916 | +0.0104 [−0.0087, +0.0300] | −0.0180 [−0.0366, +0.0016] | transfers |
| 100% | 1831 | +0.0284 [+0.0098, +0.0472] | — | — |

The cohort says the block is worth +0.0284 per case. Inside the top 5% it is worth
+0.0054, a fifth as much, and the interval on the difference excludes zero at both
5% and 10%. This is the only cell where the divergence is statistically established
rather than merely directional, and it is enough on its own: at a cost of 0.01 or
0.025 the cohort estimate says acquire and every slice down to 20% says do not.

### `false_positive_averse` — the sign flips, but not significantly

| slice | n | mean gain | vs cohort | verdict |
|---|---:|---|---|---|
| 5% | 92 | +0.0679 [−0.0571, +0.1902] | +0.0760 [−0.0446, +0.1945] | sign flip |
| 10% | 183 | +0.0587 [−0.0232, +0.1407] | +0.0668 [−0.0105, +0.1417] | sign flip |
| 20% | 366 | +0.0034 [−0.0492, +0.0608] | +0.0115 [−0.0325, +0.0601] | sign flip |
| 100% | 1831 | −0.0081 [−0.0265, +0.0104] | — | — |

EXP-005's most quotable finding was that under this utility the block *destroys*
value before it is even paid for: mean −0.0081. Inside the top 10% the point
estimate is **+0.0587**, the opposite sign. The decision flips from do-not-acquire
to acquire at every cost up to 0.05.

**The flip is directional, not established.** Every interval on the difference
contains zero. With 92 cases and a per-case standard deviation of 0.41, the standard
error is about 0.042 — five times the cohort mean being tested. That is the
precision problem in its rawest form, and it is the finding as much as the flip is.

### `opportunity_averse` — the block never touches the top half

Every slice from 5% to 50% has a mean gain of exactly 0.0000: acquisition does not
change the decision for a single case in the top half of the ranking. EXP-005 found
this utility changes the decision in only 4.9% of cases; those cases all live in the
bottom half. The cohort mean of +0.0030 is entirely generated outside the slice a
budget would work.

## What follows for P5

**P5 cannot inherit EXP-005's population mean.** The quantity that justified
promoting P5 is measured on a population the budgeted decision never sees. Under
`balanced` it overstates the value of acquisition fivefold inside the top decile;
under `opportunity_averse` it is generated entirely outside the slice; under
`false_positive_averse` it has the wrong sign there.

**The compounding caution logged in the agenda is confirmed and quantified.** It was
recorded as an anticipated risk; it is now a measurement. The two dependencies do
compound: EXP-005 says only the population mean is estimable, EXP-002 says averages
mislead in the tail, and the tail is where the budget operates.

**This does not kill P5 — it fixes its formulation.** The budgeted problem must
estimate the trade-off *inside* the slice, which is a harder estimation problem than
the one EXP-005 licensed, on roughly 5–10% of the sample. That is a statement about
what P5 has to do, and it is more specific than the original framing.

**Constructive residue, and it is the interesting part.** The slice mean is not
noise around the cohort mean — it moves monotonically with slice size under
`balanced` (+0.0054, +0.0055, +0.0082, +0.0104, +0.0284). Gain concentrates where
the base model is *least* confident. That is a structural regularity, it points the
opposite way from a triage heuristic that works the most promising deals first, and
it suggests the right P5 question is not "how much budget" but "where in the ranking
should the budget be spent". Untested, and stated as a hypothesis.

## Threats to validity

**Realised gain uses the outcome.** As in EXP-005's oracle, the quantity computed
here is the realised gain, so this shows the cohort number is the *wrong* number
inside the slice. It does not show that anyone can estimate the right one from
information available at the decision time. That is the open problem it hands to P5.

**One ranking.** The pipeline is ordered by the base model's probability. A fund
might triage on deal size, sector, or partner conviction, and the divergence is a
property of the ranking as much as of the block. Ranking by the acquired model's
score is not admissible, since it requires buying the block first.

**Wide intervals where the result is most striking.** The sign flip under
`false_positive_averse` is a point-estimate flip whose interval contains zero. Only
the `balanced` magnitude shift clears its declared margin with an interval excluding
zero. Reading the sign flip as established would be exactly the overreach this
experiment was built to detect.

**Same single block, same weak proxy, same cohort.** 2016–2020 anchors, outcome is a
later non-amendment Form D notice within 18 months, one information block. The
agenda's standing threat — that the whole diagnosis rests on one block — applies
here unchanged and is not addressed by this experiment.

**Slice sizes are declared, not optimised.** 5/10/20/50/100% were fixed before
running. No slice was added or removed after seeing a result, and the minimum size
of 30 voided nothing at this cohort size.

## Reproduction

```bash
python code/exp007_topk_transfer.py
```

Deterministic given the seed in `experiments/EXP-001C/config.json`.
