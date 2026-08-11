# P1 USPTO/PatentsView Pre-Grant Block Audit

**Date:** 2026-07-21 · **Decision:** access-gated candidate; no extraction or matching performed

## Candidate block
Pre-grant patent publications could provide technical-activity evidence qualitatively different from
Form D history. The intended unit is a published application linked to a corporate assignee. The
minimum point-in-time cutoff would be the official publication date, never application or priority
date. Current PatentsView documentation covers publications from 2001 onward and includes published
application and disambiguated-assignee tables.

## Access audit
PatentsView migrated to the USPTO Open Data Portal (ODP) in 2026. The official transition guide maps
pre-grant baseline/disambiguated tables to product `pvpgpubdis`:
[transition guide](https://data.uspto.gov/support/transition-guide/patentsview).

The ODP pages are publicly readable, but operational data access is authenticated:
- ODP website access requires a free USPTO.gov account from 18 June 2026;
- API access requires an ID.me-verified account and personal API key;
- product metadata and file endpoints returned HTTP 401/403 without a key;
- bulk file downloads require a key and are limited to 20 downloads of the same file per year.

Official references: [registration requirements](https://data.uspto.gov/support/universal-registration),
[product metadata API](https://data.uspto.gov/apis/bulk-data/product), and
[bulk download API](https://data.uspto.gov/apis/bulk-data/download).

## Remaining methodological gates
Even with access, the SEC cohort has no patent/application identifier. A defensible join requires:
1. immutable ODP product/file version and checksums;
2. publication date as `available_time`;
3. raw versus retrospectively disambiguated assignee fields kept separate;
4. exact name/location candidates followed by reviewed entity-resolution precision/recall audit;
5. explicit handling of corrected/re-published applications and disambiguation revisions;
6. licence/redistribution confirmation for the downloaded ODP product.

## Decision
Do not request, infer or store user credentials in this repository. Do not use undocumented mirrors or
name-only matching to bypass the gate. Reopen when the project owner independently provisions an ODP
API key or USPTO restores anonymous immutable bulk access. Until then this source is open-data in
content but operationally access-gated for reproducible automation.

No 2020 or future holdout outcomes were accessed, and no VoI experiment was run.

*External-source content was paraphrased for compliance with licensing restrictions.*