# Company-name entity resolution: a public benchmark with regulator-assigned ground truth

**Alessandro Guidi** · alexguidioff@gmail.com · github.com/alexguidioff
**Draft external note, 2026-07-30.** Extends the public Splink comparison to company entities.

> Written for an external technical reader. Nothing here about commercial plans or applications.

---

## Why company names are a separate problem

Public entity-resolution benchmarks are mostly person records (FEBRL, census linkage) or product
listings (Abt-Buy, Amazon-Google, WDC). Company names behave differently: legal-form suffixes dominate
token overlap, fund and partnership structures reuse a sponsor's name across unrelated vehicles, and
corporate events rename an entity outright.

Two examples from the data below, with a standard string score:

| Record A | Record B | max(token-set, sequence) | Truth |
|---|---|---:|---|
| GOBI INVESTMENT PARTNERS LP | GOBI INVESTMENT FUND LTD | **1.00** | **different** companies |
| Cyalume Technologies | Vector Intersect Security Acquisition | **0.19** | **same** company, post-SPAC |

The first corrupts a database silently. The second duplicates an entity. Neither is reachable by
tuning a threshold, because they sit on opposite sides of every threshold.

## The dataset

SEC Form D filings carry a **CIK**, an identity assigned by the regulator, while the issuer name is
free text entered by the filer. Same CIK with different name strings gives known positives; different
CIKs give known negatives. The label costs nothing and nobody had to hand-annotate it.

- 35,366 CIKs, of which 1,654 carry more than one name variant
- **13,773 labelled pairs**, with negatives blocked on a shared identity token so they are not trivially
  separable
- fully public and reproducible from SEC bulk data

## Protocol

Three choices that differ from how these comparisons are usually run:

1. **Stratified 50/50 train/test split.** Thresholds and parameters are fitted on the train half only.
   An earlier in-sample version of this work reported 81.1%; the out-of-sample figure is 80.7%, so the
   optimism was small but it should not be assumed.
2. **Blocking non-coverage counts as a non-match.** Splink only scores pairs its blocking rules
   propose. Pairs it never proposes are scored as predicted non-matches, since that is the production
   outcome. Coverage is reported separately rather than hidden.
3. **Threshold-free metrics reported alongside accuracy**: ROC-AUC and average precision.

## Results, out-of-sample

| Method | bal. acc | ROC-AUC | Avg. precision | F1 | sec |
|---|---:|---:|---:|---:|---:|
| token-set + sequence ratio, suffixes stripped | **80.7%** | 0.869 | 0.605 | 0.588 | 1.2 |
| **Splink 4.0.16** (Fellegi-Sunter, EM, blocking) | 77.3% | 0.806 | 0.578 | 0.553 | 9.1 |
| recordlinkage 0.16 Fellegi-Sunter ECM | 77.5% | 0.824 | 0.542 | 0.584 | 0.3 |
| recordlinkage logistic regression (supervised) | 80.3% | **0.873** | **0.688** | 0.568 | 0.0 |

**Splink blocking coverage of the labelled pairs: 38.2%.** By stratum: 89.4% of easy positives, 64.3%
of hard negatives, 0.7% of easy negatives (correct behaviour, blocking is meant to discard those).

Note the supervised classical baseline wins on **average precision**, 0.688 against 0.605. For a
review queue, where a human clears the top of a ranked list, average precision is the metric that
matters more than balanced accuracy. Reporting only the metric where a new method wins is the obvious
failure mode of vendor benchmarks, so both are given.

**These numbers are not comparable to the F1 0.9949 reported in the published Splink comparison.**
Different dataset, different difficulty. The point of this note is that company names with legal forms
and corporate events sit far below what person and product benchmarks produce.

## A circularity worth flagging, because it affects my own design first

I stratified positives as "hard" when their string similarity fell below 0.60, then evaluated string
matchers on that stratum. Every method scores **0.0%** there, including two that never call my
similarity function. The stratum is defined by the quantity under test, so failure on it is close to
definitional rather than empirical.

The cross-check that settles it: running the same protocol on **FEBRL**, an unrelated benchmark of
person records, also produces **0.0% on hard positives**. A result that reproduces on unrelated data
with the same definitional structure is a property of the definition.

So "hard positives are unsolved" should not be reported as an empirical finding about company data,
mine included. Any hardness definition needs to be independent of the scoring function. Candidates
that are: time gap between the two names' filing windows, disagreement on registered state or industry
classification, number of intervening filings.

## Cross-check that the matcher is not simply weak

Same matcher, same protocol, on FEBRL4 (40,000 candidate pairs after blocking, 2.66% positive rate):

| Method | bal. acc | ROC-AUC | Avg. precision | F1 |
|---|---:|---:|---:|---:|
| token-set + sequence ratio | 91.5% | 0.922 | 0.742 | 0.769 |
| recordlinkage logistic (supervised) | 91.6% | 0.916 | 0.742 | 0.781 |

91.5% on person records against 80.7% on company names, with the same code. The gap is the domain, not
the matcher.

## What separates the cases strings cannot

Non-name evidence already present in the filings, registered state, industry classification and entity
type, separates same-entity from different-entity pairs by **26 to 54 percentage points** on exactly
the pairs where name similarity is uninformative. Attributes are keyed by `(cik, name)` rather than by
CIK, so each side of a pair is described only by the filings that carried its own name string. Keying
by CIK alone produced 100% agreement, which was circular: a positive pair is defined as two names
sharing a CIK, so the label was the lookup key. Verified and corrected; 1770 of 1770 positive pairs had
resolved to a single CIK before the fix.

## Limitations, stated plainly

- **Splink was given three blocking rules and one comparison template.** A specialist would tune it
  further. The claim is "Splink with reasonable default-style configuration", not Splink at its best.
  Happy to run any configuration suggested.
- **`dedupe` is missing.** It needs a C++ toolchain to build affinegap, PyLBFGS and
  dedupe-Levenshtein-search, unavailable on the machine used. The ECM classifier stands in for the
  supervised probabilistic family.
- **Ground truth is regulator-assigned identity**, not commercial identity. Two CIKs can belong to one
  economic group.
- One jurisdiction, one filing type, English-language names only.

## Environment

splink 4.0.16 · recordlinkage 0.16 · duckdb 1.5.5 · scikit-learn 1.8.0 · pandas 2.3.3 · Python 3.13.2.
Seeds fixed. Code and pair construction are reproducible end to end from public SEC data.
