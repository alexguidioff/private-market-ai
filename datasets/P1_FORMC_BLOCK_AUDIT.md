# P1 SEC Form C Candidate Block Audit

**Date:** 2026-07-22 · **Decision:** coverage gate failed; no VoI experiment

## Scope and source
The audit used the official SEC Crowdfunding Offerings quarterly data sets from 2016 Q2 through
2023 Q4. These provide flattened, as-filed XML data from Form C offering statements, updates, annual
reports and terminations. The executable audit is `../code/audit_formc_acquisition_block.py`.
Raw archives and row-level outputs remain local and git-ignored.

Only the company-disjoint 2021 development and 2022 validation cohorts were analyzed. The script
loads an explicit five-column cohort allowlist and excludes `locked_test` before matching. It does
not load any outcome column or the 2023 label vault.

## Identity and temporal rules
- Match: exact SEC issuer CIK only; no company-name or person matching.
- Availability: Form C `FILING_DATE <= decision_time`.
- Amendments and other submission types remain separate accessions.
- Signature and issuer-signature tables are neither read nor retained.

This passes the identity and point-in-time design gates. The SEC states that the files contain
as-filed structured submissions, are released quarterly, and may place filings after the final
quarter-day cutoff in the subsequent release.

## Results
- Official quarterly archives: **31**.
- Form C submission rows: **25,434**.
- Unique Form C CIKs: **6,786**.
- Development 2021: **52/2,369 matched issuers (2.20%)**.
- Validation 2022: **57/2,243 matched issuers (2.54%)**.
- Form C rows known by issuer-specific decision time: **410**.
- Submission types observed: `C`, `C/A`, `C-AR`, `C-AR/A`, `C-TR`, `C-U`, `C-W`.

The structured disclosure is rich when present: core financial fields have approximately 94.6%
non-missingness among known Form C rows. The binding limitation is issuer coverage, not field quality.

## Gate decision
The predeclared operational threshold was at least 100 matched development issuers. Only 52 are
available. **Form C therefore fails the coverage gate and must not be used for the next VoI
experiment.** Its small matched subset could support descriptive work, but not the planned learned
selective-acquisition test or a confirmatory claim.

This result does not imply that Regulation Crowdfunding disclosures lack information. It means they
are too uncommon in this Form-D-derived cohort for the declared design.

## Reproducibility
- Summary SHA-256: `11172581fe5583059596468689f0c615cb91a5cba3550b8461d7e76fe807fc7f`
- Cohort SHA-256: `c5246f206751e8ac721eb4f8eb6bd65917d4c58e3957fd5dc0afd8b320254627`
- Script SHA-256 at run: `39047d5bfe4dbf8e1197dfa8fcee5d5f6bb0ace95bf0410f9126c66250cff957`
- Archive-level URLs, sizes and checksums are recorded in local `summary.json`.

Official source: [SEC Crowdfunding Offerings Data Sets](https://www.sec.gov/data-research/sec-markets-data/crowdfunding-offerings-data-sets).
External-source content was paraphrased for licensing compliance.