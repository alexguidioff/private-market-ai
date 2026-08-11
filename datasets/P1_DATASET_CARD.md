# P1 SEC Form D Dataset Card — v1 real-data core

**Built:** 2026-07-21 · **Canonical local path:** `datasets/processed/sec_form_d_v2/`
**Source:** official [SEC Form D quarterly datasets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets).
Raw and processed data are local and git-ignored; code, definitions and audit results are versioned.

## Scope and size
- 62 quarterly archives, 2008 Q1–2023 Q2; no missing quarter.
- 594,422 privacy-minimized filings from 274,947 issuers.
- Full technology-related panel: 19,751 anchors, 12,381 issuers, 42 columns.
- Model-ready first-anchor cohort: 12,381 rows and 12,381 unique CIKs.
- Split: train 2016–2018 = 8,455; validation 2019 = 2,095; test 2020 = 1,831.
- Panel label prevalence 34.04%; model-ready prevalence 28.87%.

## Population
US primary issuers whose non-amendment Form D filing is categorized as Other Technology, Computers,
Telecommunications or Business Services. Pooled funds and business-combination offerings are
excluded. This is a **technology-related exempt-offering cohort**, not a verified startup, software,
seed or venture-backed cohort.

## Time and label
The anchor's `filing_time` is the public filing date at day precision; it is derived from the SEC
quarterly dataset's `FILING_DATE`, not from a sub-day acceptance timestamp. `decision_time` is 12
months later. The weak label is one when the same CIK has a later non-amendment Form D filing in the
following 18 months. It means **subsequent exempt-offering notice**, not priced institutional Series A,
fundraising success or company success. The archive extends to 2023 Q2 so every 2020 anchor has its
complete label window.

## Point-in-time features
Anchor fields include industry, legal form, geography, incorporation information, revenue range,
exemptions, security type, amount offered/sold, investor count and filing lag. Enriched fields use
only filings available by `decision_time`: filing/new-notice/amendment/equity/debt counts, cumulative
and maximum amounts, latest known amounts and investor count, recency and issuer observed age.

## Leakage and quality audit
- 0 duplicate accessions; 0 duplicate CIKs in the model-ready cohort.
- 0 positive events at/before decision time; 0 positive events after the label window.
- 0 negatives with an in-window event; all rows have at least one known filing at decision time.
- Annual panel label rates are stable: 2016 34.64%, 2017 35.38%, 2018 32.25%, 2019 32.99%, 2020 35.13%.
- Sale date is missing for 6.83%; filing time remains the authoritative availability timestamp.

## Privacy and exclusions
The pipeline does not load or retain RELATEDPERSONS, SIGNATURES or RECIPIENTS. Phone numbers and
street addresses are dropped. Corporate issuer name, CIK, state and jurisdiction are retained for
entity resolution and audit. No LinkedIn scraping or proprietary data is used.

## Files and reproduction
- Builder: `code/build_sec_formd_dataset.py`
- PiT enrichment: `code/enrich_formd_cohort.py`
- Audit: local `audit.json`; canonical metrics are reproduced above.
- Outputs: `p1_cohort_enriched.csv`, `p1_first_anchor_model_ready.csv`, `formd.sqlite`.

## Future locked cohort
The SEC archive has also been extended locally through 2026 Q1 to prepare a separate company-disjoint
2021–2023 evaluation cohort. With a three-month late-filing buffer and incomplete-window censoring,
the model-ready counts are 2,369 development (2021), 2,243 validation (2022) and 914 process-locked
test (2023), with zero CIK overlap against the historical cohort. Test outcomes are isolated and
uninspected; see `P1_FUTURE_COHORT_LOCK.md`. This does not alter the canonical v1 metrics above.

## Known limitations and next enrichment
Form D is self-reported and can be amended. CIK identifies issuer records but not necessarily an
economic company across restructurings/SPVs. The industry filter is broad. A deterministic review
queue of 200 unique CIKs (100/100 by SEC weak-proxy class) has been generated locally under
`datasets/processed/sec_form_d_v2/gold/`; it is a balanced annotation design, not a prevalence sample.
The protocol, schema and sampler are `P1_OPEN_SOURCE_LABEL_PLAN.md`,
`../schemas/p1-gold-label.schema.json` and `../code/sample_p1_gold_labels.py`. Review must establish
canonical companies and stronger labels from public evidence before VC-specific claims. OpenAlex is
the first candidate acquisition block; GitHub and news features remain gated on defensible historical
availability, identity matching and source rights.

Content from SEC documentation was rephrased for compliance with licensing restrictions.
