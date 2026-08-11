# P1 Source Audit — public point-in-time vertical slice

**Date:** 2026-07-21 · **Status:** SEC core passed; strong label and multi-source enrichment open

## SEC Form D — anchor source
- Official SEC quarterly datasets expose structured notices for exempt offerings under Regulation D
  and related exemptions: [SEC Form D Data Sets](https://www.sec.gov/about/dera_form-d).
- The filing deadline can be 15 calendar days after first sale, and a notice can also be filed before
  sale. Therefore `available_time` must be based on filing acceptance—not first-sale date:
  [SEC Form D FAQ](https://www.sec.gov/about/divisions-offices/division-corporation-finance/frequently-asked-questions-answers-form-d).
  The current quarterly ingestion uses `FILING_DATE` at day precision; it does not claim a sub-day
  acceptance timestamp.
- The data are issuer-submitted and the SEC does not guarantee their accuracy. Quarterly flattened
  data include amendments and can place late-quarter submissions in the next release:
  [SEC Form D dataset guide](https://www.sec.gov/files/Form_D.pdf).

**Decision:** conditional pass as public financing anchor for 2016–2020. Required ingestion rules:
retain accession/filing/first-sale dates separately; preserve amendments; use acceptance timestamp
for PiT availability; never treat first-sale date as the date the market could observe the filing.

## Implemented SEC core
All official quarters from 2008 Q1 through 2023 Q2 were downloaded and normalized. The complete
results, fields and quality audit are in `P1_DATASET_CARD.md`. The weak Form-D-only label is now
usable for reproducible method development; the strong priced/institutional outcome remains blocked.

## Label blocker
A later Form D can support a reproducible label such as **subsequent exempt financing notice within
18 months**. It does not by itself establish that the event was priced, institutional or a Series A.
The stronger priced/institutional outcome considered by the broader research programme remains a
target construct, not an available full-cohort label. It requires a second lawful source or manually
verified public evidence; `programme.yaml` and the current P1 protocol correctly use the weak proxy.

**Gate options, to choose before data extraction:**
1. Use the weaker Form-D-only proxy and scope the claim accordingly.
2. Add a second source with explicit round type/investor evidence and document rights/coverage.
3. Build a manually verified public benchmark subset, reporting selection limits.

## OpenAlex — blocked as first acquisition block
OpenAlex states that its complete data are reusable under CC0 and provides public snapshots:
[OpenAlex developers](https://docs.openalex.org/how-to-use-the-api/api-overview) and
[snapshot overview](https://docs.openalex.org/download/overview). However, the privacy-minimized SEC
cohort contains issuer identity but no reviewed founder identities. OpenAlex institution search is
not a defensible substitute: most startups are not scholarly institutions, and name-only matching
would create unmeasurable false links. Current snapshots also do not establish when corrected entity
links first became available.

**Decision:** fail as the first P1 block. Reopen only after a lawful, reviewed founder-to-author gold
mapping exists, with publication/availability cutoffs and revision-bias analysis. Do not infer
founders from SEC related-person tables merely to rescue this block.

## SEC issuer-history diligence — accepted first acquisition block
The implemented SEC core already separates anchor fields from filing history observable by
`decision_time`. The first real acquisition experiment may therefore treat retrieval and analysis of
prior/intervening issuer filings as one open-only diligence action. Baseline state uses anchor filing
fields; the acquired block uses prior notice/amendment/security counts, cumulative amounts, recency,
issuer observed age and latest known amount/investor fields. All are derived only from filings with
`filing_time <= decision_time`.

**Decision:** pass for an exploratory acquisition experiment. It tests the value of processing issuer
history, not an external proprietary signal. Costs remain normalized sensitivity assumptions until
buyer interviews provide analyst-time and delay estimates.

## SBIR/STTR awards — candidate audited, temporal gate failed
SBIR.gov exposes complete award downloads, an API and documented company/award fields:
[SBIR data resources](https://www.sbir.gov/data-resources). A development/validation-only audit used
company name, state, UEI/DUNS, proposal-award date and notification date; contact, address, abstract
and personal fields were not retained. Exact normalized name plus state produced 622 candidate
matches among 10,550 issuers (5.90%); 350 had a proposal-award date no later than decision time.
Detailed method and results: `P1_SBIR_BLOCK_AUDIT.md`.

The current complete dump does not establish when each record first became public. Proposal-award
and applicant-notification dates are event/process dates, not SBIR.gov publication timestamps, and
current records may contain later correction or backfill. Filtering by award date therefore does not
satisfy `available_time <= decision_time`.

**Decision:** fail the current data gate; do not run a VoI experiment. Reopen only with archived
release history or another defensible first-publication rule plus entity-resolution review. Sparse
coverage alone is not the binding rejection, and an SBIR award is not venture financing or success.

## USPTO/PatentsView pre-grant — access-gated after ODP audit
Pre-grant publications are qualitatively different from Form D history and official publication date
can define `available_time`. USPTO maps `pg_published_application` and
`pg_assignee_disambiguated` to ODP product `pvpgpubdis`. Documentation and schemas are public, but
product metadata and files returned HTTP 401/403 without an API key. ODP requires a USPTO.gov account;
API access additionally requires ID.me verification and a personal key. See
[registration requirements](https://data.uspto.gov/support/universal-registration),
[product API](https://data.uspto.gov/apis/bulk-data/product), and `P1_USPTO_BLOCK_AUDIT.md`.

**Decision:** access-gated candidate, not an approved block. Do not store credentials, use unofficial
mirrors or force name-only matching. Reopen only after the project owner independently provisions
access; then freeze product/file version, verify redistribution terms and audit assignee-to-issuer
resolution and retrospective disambiguation revisions.

## SEC Form C — identity/PiT pass, coverage gate failed
The official SEC Crowdfunding Offerings quarterly data sets contain as-filed structured Form C
submissions with filing dates and SEC issuer CIKs. An audit of 31 archives (2016 Q2–2023 Q4) used
exact CIK matching and retained only filings dated no later than each decision time. Signature tables
and outcome columns were not read. See `P1_FORMC_BLOCK_AUDIT.md`.

Only 52/2,369 development issuers (2.20%) and 57/2,243 validation issuers (2.54%) had a Form C known
by decision time. The structured disclosures are rich when present, but the predeclared minimum of
100 development matches was not reached.

**Decision:** coverage gate fail; do not run a VoI experiment. Form C passes identity and temporal
semantics but is too sparse in this Form-D-derived cohort for the planned learned acquisition policy.

## Audited open-source roles
- SEC IAPD/Form ADV is suitable for corroborating adviser identity or registration/reporting status,
  not for proving participation in a specific issuer financing: [IAPD](https://adviserinfo.sec.gov/)
  and [Form ADV data](https://www.sec.gov/foia/docs/form-adv-archive-data.htm).
- GDELT and Common Crawl are discovery/archive layers, not primary truth sources and not transfers
  of rights in underlying articles: [GDELT data](https://gdeltproject.org/data.html),
  [Common Crawl access](https://commoncrawl.org/get-started), and
  [terms](https://commoncrawl.org/terms-of-use).
- The current GitHub Events API is unsuitable for reconstructing complete 2016--2020 histories
  because it exposes only a short recent window: [GitHub Events API](https://docs.github.com/rest/activity/events).
- OpenCorporates is conditional on run-specific API/access and redistribution review; OpenVC is not
  treated as an openly licensed dataset. Neither is a dependency of P1.

The executable source hierarchy, 200-issuer annotation design and release controls are in
`P1_OPEN_SOURCE_LABEL_PLAN.md`.

## Not yet audited
Macro vintage semantics, a defensible USPTO assignee-to-issuer crosswalk, adjudicated negative-class
construction and final gold-label censoring remain blockers. SBIR requires archived first-publication
semantics before reconsideration. OpenAlex historical availability and revision bias, despite its CC0
snapshot, require experiment-specific checks.

*External-source content was paraphrased for compliance with licensing restrictions.*
