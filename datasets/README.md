# Datasets — Inventory & Access Notes

> ⚠️ **Never commit proprietary or licensed data (PitchBook, Orbis, etc.) to this repository.**
> Store only descriptions, schemas, and derived/shareable artifacts.

## Real dataset built (2026-07-21)
The official SEC core is now materialized and audited; see `P1_DATASET_CARD.md`.
- Complete archive: 2008 Q1–2023 Q2, 594,422 filings, 274,947 issuers.
- Technology-related panel: 19,751 anchors; model-ready first-anchor cohort: 12,381 unique issuers.
- Point-in-time history features: 42 columns; train/validation/test = 8,455/2,095/1,831.
- Label remains the weak subsequent-Form-D proxy, not priced institutional Series A.

## Open-only labeling layer (2026-07-21)
The open-source protocol and source gates are in `P1_OPEN_SOURCE_LABEL_PLAN.md`.
- A deterministic, blinded queue of 200 unique issuers has been generated locally: 100 weak-proxy
  positives and 100 weak-proxy negatives, stratified by year, SEC industry and amount quartile.
- Review data remain under `datasets/processed/sec_form_d_v2/gold/` and are ignored by Git.
- The strong-label record contract is `../schemas/p1-gold-label.schema.json`; the sampler is
  `../code/sample_p1_gold_labels.py`.
- Sampling is complete; manual double review, entity resolution and adjudication remain open.

## Source inventory

| Category | Source | Type | Access | Notes |
|---|---|---|---|---|
| Deals | PitchBook | Proprietary | License | Optional only; do not redistribute |
| Deals | Dealroom | Proprietary / Freemium | Account | Not a reproducible-core dependency |
| Deals | Crunchbase | Licensed API | API key / agreement | Optional; not part of public core |
| Financials | Orbis | Proprietary | License | Optional; do not redistribute |
| Founders | LinkedIn | Restricted platform | Restricted | No scraping; excluded from core |
| Code | GitHub | Public platform/API | Conditional | Current Events API lacks complete 2016–2020 history |
| Patents | Google Patents | Public interface | Conditional | Audit bulk access, PiT and reuse before use |
| Research | OpenAlex | CC0 data/API/snapshot | Open | First candidate acquisition block |
| News | GDELT | Open index/data access | Open | Discovery; verify underlying source evidence/rights |
| Web | Common Crawl | Open crawl repository | Open access | Discovery/archive; underlying content retains rights |
| Funding | SEC Form D | Public government filing data | Open access | Reproducible anchor and weak proxy |
| Advisers | SEC IAPD/Form ADV | Public government filing data | Open access | Adviser corroboration, not deal participation |
| Registries | State business registries | Public, jurisdiction-specific | Conditional | Terms, coverage and timestamps vary |
| Companies | OpenCorporates | Public interface/API | Conditional | Run-specific access and redistribution audit required |
| VC discovery | OpenVC | Free service | Conditional / not established open data | Excluded from reproducible core |
| Entity support | Wikidata | Open structured data | Open | Candidate aliases only; not gold evidence |
| Macro | World Bank/OECD/FRED | Public APIs/data | Open/conditional | Require vintage/revision semantics |
| Macro | GEM | Dataset | Academic | License-dependent; optional |

## For each dataset, document:
- Schema / fields used
- Coverage (geography, time, stage)
- Freshness / update cadence
- License / ToS constraints
- Identity-resolution approach (how entities are matched across sources)
