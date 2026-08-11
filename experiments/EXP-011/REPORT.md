# EXP-011 — Splink and classical record linkage on our pairs, and our matcher on theirs

**Date:** 2026-07-30 · **Script:** `code/exp011_market_tools.py` · **Artefacts:** `results.json`
**Answers the open item recorded in EXP-006:** whether a real probabilistic matcher with blocking
closes the gap. It does not. It performs worse.

Versions: splink 4.0.16, recordlinkage 0.16, duckdb 1.5.5, scikit-learn 1.8.0, Python 3.13.2.
`dedupe` could not be installed: it needs a C++ toolchain to build affinegap, PyLBFGS and
dedupe-Levenshtein-search, absent on this machine. The Fellegi-Sunter ECM classifier stands in for the
same family. **Installing dedupe remains open.** Note the install downgraded pandas 3.0.3 to 2.3.3.

## Method corrections applied to EXP-006

1. **Train/test split.** EXP-006 chose its threshold on the same pairs it scored, so 81.1% was
   in-sample. Here every method fits on a stratified train half (6,886 pairs) and is scored on a
   held-out test half (6,887).
2. **Blocking counts against recall.** Splink only scores pairs its blocking rules generate. Pairs it
   never proposes are scored as non-matches, because that is what production does.
3. **Threshold-free metrics added.** ROC-AUC and average precision, which depend on neither a
   threshold nor the strata. This turned out to matter, see the circularity finding below.

## A. Market tools on our data (13,773 SEC-CIK pairs, out-of-sample)

| Method | bal. acc | ROC-AUC | Avg. precision | F1 | pos_hard | neg_hard | sec |
|---|---:|---:|---:|---:|---:|---:|---:|
| **ours** (token-set + sequence, suffixes stripped) | **80.7%** | 0.869 | 0.605 | 0.588 | 0.0% | 78.3% | 1.2 |
| **Splink 4** (Fellegi-Sunter, EM, blocking) | 77.3% | 0.806 | 0.578 | 0.553 | 0.0% | 79.5% | 9.1 |
| recordlinkage Fellegi-Sunter ECM | 77.5% | 0.824 | 0.542 | 0.584 | 0.0% | **84.6%** | 0.3 |
| recordlinkage logistic (**supervised**) | 80.3% | **0.873** | **0.688** | 0.568 | 0.0% | 75.3% | 0.0 |

### What this settles

**Splink does not close the gap, it widens it.** 77.3% balanced accuracy and AUC 0.806 against our
80.7% and 0.869. The EXP-006 ceiling was therefore not an artefact of using homemade matchers, which
was the live objection. The market-standard open-source tool is worse on this data.

**The in-sample optimism was small.** Our matcher scores 79.7% train and 80.7% test, so the previously
reported 81.1% was not materially inflated by threshold selection. Worth recording because the
correction could have gone the other way.

**But we lose on the metric that matters commercially.** The supervised logistic baseline reaches
average precision **0.688 against our 0.605**. Average precision is ranking quality, and the product
described in `Startup_Ideas.md` is a triage queue: rank ambiguous pairs so a human clears the top.
On that metric an off-the-shelf classical classifier given labels beats us. Any public benchmark must
report this rather than lead with balanced accuracy, where we happen to win.

**Splink is roughly 8x slower** than the ECM classifier and 7x slower than ours on this size, and
[its own vendor benchmark from Tilores](https://tilores.io/content/splink-vs-tilores-benchmark) notes
Splink wins on raw batch throughput at scale, so this ordering should not be extrapolated.

### Splink blocking coverage — the production-relevant number

Splink generated **1,222,545 candidate pairs** and covered **38.2%** of our labelled pairs:

| Stratum | Coverage |
|---|---:|
| positive_easy | 89.4% |
| **positive_hard** | **14.0%** |
| negative_hard | 64.3% |
| negative_easy | 0.7% |

In production Splink would never even score 86% of the rebrand-and-restructure cases. Low coverage of
easy negatives is correct behaviour, not a defect: blocking is supposed to discard obvious non-matches.

## ⚠️ B circularity finding: our "hard positive" stratum is defined by the metric we evaluate

`build_pairs` labels a positive as hard when `combined(a, b) < 0.60`, and `combined` is the function
under test. Any method correlated with string similarity must therefore score near zero on that
stratum **by construction**. The confirming evidence is that all four methods, including two that never
call `combined`, report exactly 0.0% there.

The FEBRL run makes it unambiguous: **hard positives are 0.0% on FEBRL too**, a completely different
dataset of person records. A finding that reproduces on unrelated data with the same definitional
structure is a property of the definition, not of private markets.

**Consequence.** "Hard positives sit at 0-11%" cannot be published as an empirical result about
company entity resolution. It is close to a tautology. This is the fourth circularity caught in this
project, after the 846 overlapping CIKs in EXP-002, the 1770/1770 CIK lookup in EXP-006, and the
zero-file records in the agentic PR work. The stated pattern holds: every result that looked clean
turned out to be circular.

**What survives and is not circular:**
- the threshold-free comparison (AUC 0.869 ours, 0.873 supervised, 0.824 ECM, 0.806 Splink)
- the non-nominal attribute separation of 26-54 points from EXP-006, which uses information outside
  the definition of the stratum
- the difficulty gap between datasets in section C below

**What must be rebuilt before any public benchmark ships:** a hardness definition independent of the
scoring function. Candidates: time gap between the two names' filing windows, disagreement on state or
industry, or number of intervening filings. All are non-nominal, so none can be gamed by the metric.

## C. Our matcher on their data (FEBRL4, standard benchmark)

40,000 candidate pairs after blocking, positive rate 2.66%.

| Method | bal. acc | ROC-AUC | Avg. precision | F1 | neg_hard |
|---|---:|---:|---:|---:|---:|
| **ours** | 91.5% | 0.922 | 0.742 | 0.769 | 99.0% |
| recordlinkage logistic (supervised) | 91.6% | 0.916 | 0.742 | 0.781 | 99.1% |

**Our matcher is not weak.** It reaches 91.5% balanced accuracy and AUC 0.922 on a standard benchmark,
statistically level with a supervised classical baseline. So the 80.7% on company names is not the
matcher being bad; company entity resolution with legal forms, funds and corporate events is harder
than person-record linkage. That is the claim direction B was run to test, and it holds.

## Threats to validity

- **FEBRL is person records, not companies.** It establishes that the matcher is competent, not that
  the company result transfers. The product-oriented benchmarks (DBLP-ACM, Abt-Buy, Amazon-Google,
  WDC) require download and were not run; see also the
  [critical re-evaluation of those datasets](https://arxiv.org/html/2307.01231v1) before using them.
- **Splink was given three blocking rules and one comparison template.** A specialist would tune it
  further. The honest claim is "Splink with reasonable default-style configuration", not "Splink at its
  best". The Tilores benchmark publishes its rule configuration; ours should too.
- **dedupe is missing**, so the supervised active-learning approach the market also uses is untested.
- **Ground truth is SEC CIK.** Same caveat as EXP-005-ER: the label is regulator-assigned identity, and
  the information path from label to features must stay disjoint.
- Exit code 1 on completion appears to come from library teardown after `results.json` is written; all
  reported numbers are produced before it.

## Reproduction

```bash
python code/exp011_market_tools.py
```

Seed 20260730 for the split, 20260728 for pair construction.
