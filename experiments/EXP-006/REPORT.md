# EXP-006 — Does a stronger matcher close the entity-resolution gap?

**Date:** 2026-07-29 (re-run and written up 2026-07-29)
**Script:** `code/exp006_stronger_baseline.py` · **Artefacts:** `results.json`, `stdout.txt`
**Predecessor:** `experiments/EXP-005-ER/` (name-matching difficulty, hypothesis H3)

> **Bookkeeping note, recorded rather than tidied away.** Two different experiments
> were both numbered EXP-005 and both wrote `experiments/EXP-005/results.json`:
> the value-of-information diagnosis and the entity-resolution difficulty test.
> Whichever ran second destroyed the other's artefact, and the VoI one is what
> survived. The entity-resolution experiment now writes to `EXP-005-ER` and has
> been re-run to restore its results. The VoI folder keeps the original number
> because the research agenda and the P1 working paper cite it by path. This is
> logged because a silent artefact overwrite is exactly the failure that makes a
> thesis irreproducible, and because it means any earlier reading of
> `EXP-005/results.json` for entity-resolution numbers was reading the wrong file.

## Question

EXP-005-ER found that `max(Jaccard, sequence ratio)` after stripping legal suffixes
reaches roughly 73% accuracy on hard negatives and close to 0% on hard positives.
Before treating that as a real limitation of string matching, the obvious objection
has to be tested: perhaps the matcher was simply weak. This experiment runs six
matchers plus their pointwise maximum on the same pairs, and then asks whether
attributes other than the name separate the cases strings cannot decide.

## Result

| matcher | balanced acc. | threshold | hard neg. | hard pos. | easy pos. |
|---|---:|---:|---:|---:|---:|
| jaccard, suffix stripped | 77.4% | 0.39 | 68.7% | 4.4% | 83.6% |
| jaccard, suffix kept | 79.2% | 0.39 | 60.2% | 7.5% | 92.4% |
| sequence ratio | 80.1% | 0.77 | 78.3% | 0.0% | 85.2% |
| **character 3-grams** | **80.8%** | 0.41 | 74.4% | 1.0% | 89.1% |
| idf-weighted tokens | 78.3% | 0.41 | 66.1% | 3.4% | 87.4% |
| idf plus head token | 76.0% | 0.36 | 62.9% | 7.5% | 83.1% |
| best of all seven | 80.2% | 0.77 | 78.2% | 0.0% | 85.3% |

**The objection does not survive, and neither does the hope behind it.** The best
single matcher reaches 80.8% balanced accuracy and the pointwise maximum of all
seven reaches 80.2% — taking the best of everything does not beat the best one,
which is the signature of a ceiling rather than of a badly chosen similarity.

Hard positives are the collapse: between 0.0% and 7.5% across every matcher. These
are the same company under names with no lexical overlap — `DOR BIOPHARMA INC` and
`SOLIGENIX, INC.`, `IB3 Networks, Inc.` and `LANGUAGE ACCESS NETWORK, INC.` No
string similarity can recover a rename, because the information is not in the
string. The matcher that does best on hard positives (suffix kept and idf-plus-head, 7.5%) is the one
that does worst on hard negatives (60.2% and 62.9% respectively): the two error types trade off against
each other along the same axis, which is what a single-signal ceiling looks like.

## The constructive half

Non-name attributes were available for 99.8% of pairs, and they separate exactly
where strings fail:

| attribute | agreement, same entity | agreement, different entity | gap |
|---|---:|---:|---:|
| state | 90.7% | 37.8% | **+52.9** |
| entity type | 94.5% | 56.1% | **+38.4** |
| industry | 87.3% | 60.8% | **+26.5** |

Measured on the hard strata specifically, that is, on the pairs string similarity
cannot decide. Location gives the widest separation, which is intuitive in
hindsight and was not assumed: a renamed issuer keeps filing from the same state,
while two similarly-named funds usually do not share one.

## What follows

* **String matching is at its ceiling around 81%.** Reporting a better similarity
  function is not a contribution and further search there should stop.
* **The gap is a missing-signal problem, not a weak-model problem.** The three
  attributes above carry separation on precisely the hard cases, so the next step is
  a combined decision rule, not a seventh string metric.
* **Consequence for the thesis, stated narrowly.** This supports the white paper's
  claim (Ch. 7 §7.4) that identity resolution is the hardest engineering problem in
  the stack, and it now supports it with a measured ceiling rather than an
  assertion. It does not establish that the combined rule works: that is untested.

## Threats to validity

**Ground truth is the SEC CIK, which defines the task rather than describing the
world.** Two filings sharing a CIK are the same registrant by construction. A
company that re-registers under a new CIK counts as two entities here and would be
one to an analyst, so the hard-positive stratum is bounded by what CIK reuse
happens to capture.

**Hard strata are constructed, not sampled.** Pairs were selected to be lexically
similar yet different, or lexically dissimilar yet same. The accuracies therefore
describe difficulty inside a deliberately adversarial slice and must not be read as
population accuracy.

**The attribute separation is observational and in-sample.** No held-out split was
used for the attribute gaps, and no combined classifier was fitted or evaluated.
Treating the three gaps as evidence that a combined rule will work would be
exactly the overreach this file is trying to avoid.

## Reproduction

```bash
python code/exp005_entity_resolution.py   # writes experiments/EXP-005-ER/
python code/exp006_stronger_baseline.py   # writes experiments/EXP-006/
```

---

## Reproducibility correction, 2026-07-29

**This experiment did not reproduce between runs, and the figures above are the corrected values.**

`code/verify_p1_reproducibility.py` hashes each result artefact, re-runs the experiment and compares.
On its first execution, five of seven P1 diagnostic experiments reproduced byte-identically and two did
not: this one and `EXP-005-ER`, which supplies its pairs. Three separate executions had reported a best
matcher of **81.1%**, **81.0%** and **80.8%** balanced accuracy.

**Cause.** `build_pairs` in `code/exp005_entity_resolution.py` iterated over Python sets of strings —
the per-CIK name sets and the token sets from `tokens()`. String hashing is randomised per interpreter
process, so the blocking dictionary was assembled in a different order on every run, and because the
hard negatives are then shuffled and truncated with `[:6000]`, a different subset survived each time.

**Why this is worth recording rather than silently fixing.** The code was correctly seeded. `SEED` was
declared, `random.Random(SEED)` was used, and every shuffle and sample drew from that generator. A
reader auditing the file for reproducibility would have concluded it was deterministic. The defect sits
one level below the seed, in the iteration order of the container being sampled *from*, and no amount of
seed discipline addresses it. Sorting the three iteration points fixes it.

**Effect on the conclusions: none qualitative, small quantitative.** Across all three runs the best
single matcher sat between 80.8% and 81.1%, the pointwise maximum of all seven never beat it, hard
positives never exceeded 11%, and the attribute separations stayed within a point or two. The claim this
experiment supports — that string matching is at a ceiling and the gap is missing signal rather than a
weak model — held in every draw. What was not safe was quoting a specific figure to one decimal place,
which the working paper did.

**Verification after the fix.** Both experiments now reproduce byte-identically, confirmed by two
independent double-runs and then by the full manifest: 7 of 7 identical,
`experiments/P1_REPRODUCIBILITY.json`.

**Propagated to:** working paper §6.1 and §10, `docs/Idea_Falsification_Log.md` (H3 second test),
`docs/Research_Agenda.md`, `papers/README.md`.
