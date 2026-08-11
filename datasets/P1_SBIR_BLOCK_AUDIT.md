# P1 SBIR/STTR Candidate Block Audit

**Date:** 2026-07-21 · **Decision:** conditional candidate; data gate not passed

## Scope
The official SBIR/STTR award dump was joined only to 2016–2019 Form D development/validation
anchors. The repeatedly inspected 2020 cohort was excluded. No outcome model or VoI policy was run.
The executable audit is `../code/audit_sbir_acquisition_block.py`; row-level outputs remain local and
git-ignored under `processed/sec_form_d_v2/sbir_audit/`.

## Source and matching
SBIR.gov provides complete award downloads plus an API and documents company, award, identifier and
date fields: [SBIR data resources](https://www.sbir.gov/data-resources). The audit used the official
no-abstract CSV and retained only company name, state, UEI/DUNS and award/notification dates. Contact,
address, abstract and personal fields were not retained.

Matching was deliberately conservative: exact normalized company name plus two-letter state. Legal
suffixes and punctuation were normalized; no fuzzy or person-based matching was used.

## Results
- Development/validation issuer rows: **10,550**.
- Exact name+state candidate matches: **622 (5.90%)**.
- Candidate keys mapping to one source firm identifier: **622**; ambiguous keys: **0**.
- First proposal-award date no later than decision time: **350**.
- Missing first notification date among candidates: **4.50%**.
- Local summary SHA-256: `7cff6f0044b79b9d1625e75a7636b5cef9954a38e31b5f887df2ce5ad6c2872c`.

## Gate decision
**Fail for immediate P1 acquisition use.** Coverage is sparse but potentially usable as an
availability/absence block; the binding problem is temporal. `Proposal Award Date` is event time and
`Date of Notification` is applicant notification time. Neither establishes the date on which the
record first appeared publicly on SBIR.gov. A current complete dump may contain later corrections or
backfill, so filtering it by award date alone could leak retrospective knowledge.

Reopen only if an archived snapshot/release history or another defensible public-availability rule is
established, and after precision/recall-oriented entity-resolution review. Until then, do not add SBIR
features to EXP-001C, do not inspect 2020, and do not describe an award as venture financing or
company success.

*External-source content was paraphrased for compliance with licensing restrictions.*