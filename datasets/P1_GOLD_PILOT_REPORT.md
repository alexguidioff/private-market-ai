# P1 Open-Source Gold-Label Pilot — 20 Issuers

**Date:** 2026-07-21  
**Status:** AI-assisted double-review feasibility pilot, accepted by the project owner without an
independent human source review; not a publication-grade human gold benchmark.  
**Protocol:** `P1_OPEN_SOURCE_LABEL_PLAN.md`.

## Purpose

Test whether stronger real-world financing labels can be reconstructed from public evidence without
paid databases, how often cases remain unknown, and which annotation rules must be fixed before
reviewing the remaining 180 issuers.

The pilot was selected deterministically from the 200-issuer queue: two cases per anchor year and
hidden SEC weak-proxy class, for 20 unique issuers total. Reviewer-facing files did not expose the
weak proxy. Two independent AI-assisted review passes searched issuer/investor announcements, SEC
records, regulatory sources and reputable reporting. Search and commercial profile pages were
considered discovery, not primary proof.

## Results

| Measure | Result |
|---|---:|
| Issuers | 20 |
| Identity high/usable in both reviews | 18/20 |
| Exact label agreement | 15/20 (75%) |
| Positive agreement | 7 |
| No-public-evidence agreement | 4 |
| Unknown agreement | 4 |
| Unresolved disagreement | 5 |
| Conservative pilot labels: positive | 7 (35%) |
| Conservative pilot labels: no public evidence | 4 (20%) |
| Conservative pilot labels: unknown/unresolved | 9 (45%) |

Agreement is raw agreement, not a claim of human inter-rater reliability. With 45% unknown/unresolved,
the protocol is feasible for a benchmark but not yet reliable enough to label all 200 mechanically.

## Main disagreements

1. **Form D as strong evidence:** a new notice with a first-sale date in-window proves a reported
   exempt offering, but may not establish the intended stronger construct without corroboration.
2. **Publication after the outcome cutoff:** later filings can audit that an event occurred in-window,
   but were not observable by the cutoff. Outcome evidence and point-in-time features need separate
   availability rules.
3. **Amendments:** cumulative amount increases cannot be assigned to the window when individual sale
   dates are absent.
4. **Entity boundary:** legal CIK, operating company, parent and financing SPVs cannot be merged
   without canonical-company adjudication.
5. **Absence semantics:** `no_public_evidence` depends on a defined search protocol; it is not a true
   negative and must not be called company failure.
6. **Priced round:** “Series A/F” or equity Form D does not by itself prove price per share/valuation
   terms. Reviewers applied inconsistent interpretations.

## Go/no-go decision

**GO for method development using Layer A, with explicit evidence-status limitations.** The project
owner accepted the conservative model-reviewed outcomes without performing a separate human source
review. Applying the revised Layer A rules to the five conflicts produces 9 `positive`, 4
`no_public_evidence` and 7 `unknown` records. The original reviewer decisions and disagreements remain
preserved and must be reported.

These accepted labels can support pipeline development, source-coverage analysis and a real-data
baseline sensitivity check. They must not be described as expert-adjudicated or publication-grade
human gold labels. Layer B remains `unknown` unless separately documented; the pilot does not justify
extending strong-round labels mechanically to the remaining 180.

## Required safeguards for use

- Keep Layer A and Layer B separate.
- Preserve `event_in_window` and `evidence_available_by_window_end`.
- Treat `no_public_evidence` as an evidence-search result, not failure.
- Keep the original reviewer disagreement fields in every analysis.
- Run sensitivity analyses that map all `unknown` records once to negative and once to positive.
- Do not estimate population prevalence from the balanced pilot.

## Next execution sequence

1. Use the 20 owner-accepted Layer-A labels to validate analysis plumbing and label sensitivity.
2. Run the full SEC weak-proxy baseline separately on the 12,381 issuer cohort.
3. Freeze utility ranges and costs before inspecting the locked test comparison.
4. Add one defensible acquisition block only after the baseline is reproducible.
5. Return to the remaining 180 only if stronger labels become necessary for a paper claim or partner.

## Claim boundary

This pilot shows that open-only adjudication is plausible. It does **not** validate the SEC weak
label, establish population prevalence, demonstrate the VoI policy, or create a completed gold set.
The balanced 10/10 SEC sampling design cannot estimate a real-world positive rate.

Evidence URLs and record-level decisions are stored locally in the git-ignored comparison artifact:
`datasets/processed/sec_form_d_v2/gold/pilot20/pilot_review_comparison.csv`.
Web-source content was paraphrased for licensing compliance.
