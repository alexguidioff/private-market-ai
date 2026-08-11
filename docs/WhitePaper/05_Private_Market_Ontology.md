# Chapter 5 — Private Market Ontology

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Ontology.md`, `Private_Market_Data_Model.md §3`
**Level:** 🧭 NORTH STAR

---

## Abstract

Chapter 4 argued that private markets need a representation, not just a database, and sketched a
six-layer model. This chapter makes the representation precise: it defines the **ontology** — the
formal vocabulary of entities, relationships, events, signals, and reasoning objects — at a level
of detail sufficient to be implemented as a schema (RDF/OWL, a labeled property graph, or a
JSON schema) and proposed as an **open standard**. The ambition is explicit: to be, for private
markets, what UMLS `[bodenreider2004umls]` is for biomedicine — a shared, machine-reasoning-ready
model of the domain that many parties can adopt and extend.

---

## 5.1 Why an ontology (not just a schema)

A schema serves one database; an ontology serves a *field*. Ontologies make the concepts and
their relationships explicit and shareable, so that different systems, datasets, and teams can
interoperate and reason over the same model of the world — the property that underpins knowledge
graphs at scale `[hogan2021kg]`. Medicine industrialised this idea: UMLS integrates millions of
concept names and relations across dozens of source vocabularies `[bodenreider2004umls]`, giving
machines a common semantics for clinical concepts. Private markets have **no such standard**.
Defining one is both a scientific contribution (a model of a domain) and a strategic asset (a
common layer others build on, hard to displace).

### 5.1.1 Relationship to FIBO (position, don't ignore)
Finance is not a blank slate: the **Financial Industry Business Ontology (FIBO)** — maintained by
the EDM Council and OMG — is a mature, open OWL/RDF ontology of financial *things* (instruments,
legal entities, contracts, ownership), organised in packages (Foundation, Loans, Investments/
Capital Markets, Business & Commerce). A prior-art scan (`papers/notes/Prior_Art_Scan.md`) flags
this as the **single most likely reviewer objection** to a "private-market ontology": *"why not
FIBO?"*.

The answer — and the positioning of this chapter — is that FIBO models **public/regulated
instruments and legal entities**, not the private-market-native concepts this programme needs:
*startup, funding round, founder, investor syndicate, growth signal, behavioural event*, nor a
**temporal, multimodal, uncertainty-native** design. The correct stance is therefore
**"aligned with, and extending, FIBO"** — reuse its entity/legal-structure backbone where it fits,
and add the private-market layer on top. Aligning to FIBO is itself a credibility signal; claiming
to be the first financial ontology would not survive review.

## 5.2 Entity catalog

Each entity has an identity, a set of typed attributes, and a temporal validity. The core
entities and representative attributes:

- **Company** — sector, sub-sector, founded_year, country, business_model, stage, status.
- **Founder** — education[], prior_companies[], prior_exits[], role, tenure, network_centrality.
- **Investor** — type {VC, PE, CVC, angel, family-office, growth}, aum, dry_powder, track_record, portfolio[].
- **Fund** — vintage, strategy, size, geography, average_ticket, lps[].
- **Partner** — investor_id, focus[], board_seats[].
- **Market** — country, sector, tam, funding_climate, interest_rates, competition_index.
- **Deal** — round, date, amount, valuation_pre, valuation_post, lead_investor_id, participants[], terms{}.
- **Product** — repository, website, technology_stack[], apis[], patents[].
- **Customer** — segment {enterprise, SMB, consumer}, retention, growth.

## 5.3 Relationship catalog

Typed, directed, and time-stamped edges — the heart of the ontology:

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

This layer is where the founding paper's central result lives: the **investor syndicate** is a
relationship structure (`INVESTED_IN` co-participation, `LED_BY`), and its predictive power
`[guidi2026wi]` — the "certification effect" `[hochberg2007]` — is a property of the graph. An
ontology that makes syndication explicit captures, at the schema level, what the paper found
empirically.

## 5.4 Event catalog

Events are the mechanism of state change. Schema:
`{ id, type, entity_id, timestamp, payload{}, source, confidence }`.
Types: `FundingRound · Hiring · Departure · FounderLeft · NewCEO · ProductLaunch · PatentFiling ·
Acquisition · IPO · CustomerWin · CustomerLoss · Lawsuit · Grant · OpenSourceRelease ·
GitHubActivity · PressMention`. Modelling events explicitly is what makes the ontology *temporal*
and enables the regime-aware, out-of-time analysis shown to matter in `[guidi2026wi]`.

## 5.5 Signal catalog

Signals are behavioral summaries over time:
`{ id, entity_id, metric, value, window, timestamp, source }`.
Metrics: `hiring_velocity · employee_churn · github_commits · founder_posting_frequency ·
investor_syndication · patent_velocity · release_frequency · customer_growth · web_traffic ·
developer_activity · conference_talks`. Signals are first-class so that models consume a stable
vocabulary rather than re-deriving features per study (the fragmentation noted in Chapter 2).

## 5.6 Reasoning-object catalog

The bridge from evidence to judgment:
`{ id, type, entity_id, statement, evidence[], confidence, author }`.
Types: `Hypothesis · Risk · Opportunity · Competition · MarketFit · TechnologyRisk ·
ExecutionRisk · CapitalEfficiency · FounderQuality · Governance`. Reasoning objects link evidence
(entities, events, signals, documents) to claims, and are what agents (Chapter 9) read and write.

## 5.7 Design decisions to settle

- **Serialization:** RDF/OWL (standards-based, reasoning tooling) vs. labeled property graph
  (Neo4j-style, pragmatic) vs. JSON-schema-first (developer-friendly). Likely a property-graph
  core with an OWL export for interoperability.
- **Time model:** bitemporal (valid-time + transaction-time) so that "what we knew when" is
  recoverable — essential for auditability and out-of-time evaluation.
- **Identity resolution:** deduplicating companies/founders across PitchBook, Crunchbase, GitHub,
  LinkedIn — the hardest engineering problem (Chapter 7).
- **Confidence & provenance:** attached to every fact, event, signal, and reasoning object.

## 5.8 Toward an open standard

The path to adoption mirrors how technical standards mature: publish a versioned specification,
provide a reference implementation on public data, and invite comments (an RFC posture, per
`Private_Market_Data_Model.md`). **Align to FIBO** where the two overlap (legal entities, ownership,
instruments) so the standard slots into existing financial-semantics infrastructure rather than
competing with it (§5.1.1). Adoption by even one external group or dataset would be the first
success criterion (Chapter 3, §3.5).

---

## Open questions carried forward
- What is the *minimal* ontology that both academics and practitioners would actually adopt?
- How to version the ontology as the domain evolves (new signal types, new deal structures)?
- How to reconcile competing source vocabularies (PitchBook vs. Crunchbase taxonomies)?

> **Figure F5** (`figures/figures.md#f5`): entities + relationships as a property graph.
> **Machine-readable schema:** v0.2 drafted in `../Ontology_v0.2.md` (JSON Schema, draft 2020-12),
> with the Ch.4 worked example encoded.

## To do for this chapter
- [x] Machine-readable v0.2 schema drafted (JSON-schema-first) → `../Ontology_v0.2.md`.
- [ ] Validate the schema, add cardinality constraints, generate an RDF/OWL export.
- [x] Figure F5 drafted (`figures/figures.md`).
- [ ] Map a public subset (OpenVC / Crunchbase / GitHub) onto the ontology as proof of concept.
- [ ] Cross-reference §5.2 attributes with the worked example in Chapter 4 §4.6.
- [ ] Study FIBO's Investments/Capital-Markets package; specify exactly which classes to reuse vs.
      extend (§5.1.1) — the concrete differentiation a reviewer will demand.
