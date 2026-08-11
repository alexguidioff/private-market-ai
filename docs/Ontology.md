# Private Market Ontology (draft)

**Author:** Alessandro Guidi — v0.1
**Goal:** An open, shared vocabulary for private markets — a candidate standard analogous to
SNOMED CT / UMLS in medicine.

> This is the technical companion to `Private_Market_Data_Model.md`. It defines the concepts,
> their attributes, and the relations between them precisely enough to be implemented as a
> schema (RDF/OWL, property graph, or JSON schema).

---

## 1. Entity catalog

### Company
- `id`, `name`, `sector`, `sub_sector`, `founded_year`, `country`, `hq_city`
- `business_model` ∈ {SaaS, marketplace, hardware, biotech, fintech, ...}
- `stage` ∈ {pre-seed, seed, series-A, series-B, ..., growth, pre-IPO}
- `status` ∈ {active, acquired, IPO, closed}

### Founder
- `id`, `name`, `education[]`, `prior_companies[]`, `prior_exits[]`
- `role` ∈ {CEO, CTO, COO, ...}, `tenure`, `network_centrality`

### Investor
- `id`, `name`, `type` ∈ {VC, PE, CVC, angel, family-office, growth}
- `aum`, `dry_powder`, `track_record`, `portfolio[]`

### Fund
- `id`, `name`, `vintage`, `strategy`, `size`, `geography`, `average_ticket`, `lps[]`

### Partner
- `id`, `name`, `investor_id`, `focus[]`, `board_seats[]`

### Market
- `id`, `country`, `sector`, `tam`, `funding_climate`, `interest_rates`, `competition_index`

### Deal
- `id`, `company_id`, `round`, `date`, `amount`, `valuation_pre`, `valuation_post`
- `lead_investor_id`, `participants[]`, `terms{}`

### Product
- `id`, `company_id`, `repository`, `website`, `technology_stack[]`, `apis[]`, `patents[]`

### Customer
- `id`, `company_id`, `segment` ∈ {enterprise, SMB, consumer}, `retention`, `growth`

---

## 2. Relationship catalog

| Subject | Predicate | Object | Cardinality |
|---|---|---|---|
| Founder | `FOUNDED` | Company | n:m |
| Founder | `WORKED_AT` | Company | n:m |
| Investor | `INVESTED_IN` | Company (via Deal) | n:m |
| Fund | `OWNS` / `MANAGED_BY` | Investor | n:m |
| Partner | `WORKS_FOR` | Investor | n:1 |
| Partner | `SITS_ON_BOARD` | Company | n:m |
| Company | `OPERATES_IN` | Market | n:m |
| Company | `COMPETES_WITH` | Company | n:m |
| Company | `ACQUIRED` | Company | n:m |
| Deal | `FOR_COMPANY` | Company | n:1 |
| Deal | `LED_BY` | Investor | n:1 |

---

## 3. Event catalog

Each event: `{ id, type, entity_id, timestamp, payload{}, source, confidence }`

Types:
`FundingRound · Hiring · Departure · FounderLeft · NewCEO · ProductLaunch ·
PatentFiling · Acquisition · IPO · CustomerWin · CustomerLoss · Lawsuit ·
Grant · OpenSourceRelease · GitHubActivity · PressMention`

Events are the mechanism by which entity **state** changes over time.

---

## 4. Signal catalog

Each signal: `{ id, entity_id, metric, value, window, timestamp, source }`

Metrics:
`hiring_velocity · employee_churn · github_commits · founder_posting_frequency ·
investor_syndication · patent_velocity · release_frequency · customer_growth ·
web_traffic · developer_activity · conference_talks`

---

## 5. Reasoning-object catalog

Each reasoning object: `{ id, type, entity_id, statement, evidence[], confidence, author }`

Types:
`Hypothesis · Risk · Opportunity · Competition · MarketFit · TechnologyRisk ·
ExecutionRisk · CapitalEfficiency · FounderQuality · Governance`

These link *evidence* (documents, signals, events) to *judgments* — the bridge between data
and decision.

---

## 6. Design decisions to settle
- Serialization: RDF/OWL vs. labeled property graph (Neo4j-style) vs. JSON-schema first.
- Time model: bitemporal (valid-time + transaction-time)?
- Identity resolution: how to dedupe companies/founders across sources.
- Confidence/provenance: attach to every fact, event, and signal.

---

## 7. Next steps
- [x] Formalize v0.2 as a machine-readable schema → **`Ontology_v0.2.md`** (JSON Schema, draft 2020-12).
- [ ] Validate the v0.2 schema and split into `.json` files; add cardinality constraints.
- [ ] Map a public subset (Crunchbase/OpenVC/GitHub) onto it as proof of concept.
- [ ] Generate an RDF/OWL export for interoperability.
- [ ] Publish for comments to target research groups.
