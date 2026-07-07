# The Private Market Data Model
## A Unified Representation for Artificial Intelligence in Venture Capital and Private Equity

**Author:** Alessandro Guidi
**Status:** RFC — v0.1 (Request for Comments)
**Type:** Foundational document (Paper #0)

> **Scientific question:**
> How should private companies, investors, markets, and transactions be represented to enable
> AI systems to *support investment decisions*?

Note: this is about **representation**, not prediction. That is what raises the level of the
research. The model must work for Venture Capital, Growth Equity, Private Equity, Venture Debt,
Family Offices, and Corporate VC — hence "private markets", not "startups".

---

## 1. Motivation — why existing databases are not enough

Today we have PitchBook, Crunchbase, Dealroom, Orbis, Capital IQ, LinkedIn, GitHub, news feeds.
They are all **databases**. None is a **conceptual model of the domain**: an explicit
representation of the entities, relationships, and events that a *reasoning* system needs.

This is a classic computer-science distinction: databases *store* data; they do not necessarily
*represent* the world in a way a machine can reason over. In medicine, standards like
**SNOMED CT** and **UMLS** provide shared representations of clinical concepts and relations.
Private markets have **no equivalent standard**. Building one could be a primary scientific
contribution.

A private investment is not a number. It is a **dynamic system**: companies, founders,
investors, funds, partners, deals, markets, technology, competition, customers, employees,
patents, documents, and events — all connected and evolving over time.

---

## 2. Design principles

1. **Representation over storage** — model entities, relations, events, signals explicitly.
2. **Temporal by default** — every fact has a time; state changes via events.
3. **Multimodal** — text, tables, time series, images, code, documents.
4. **Reasoning-ready** — expose objects an AI can reason about (risks, hypotheses).
5. **Source-agnostic** — integrate any feed; integration is the moat, not any single source.
6. **Open and extensible** — designed as a candidate open standard.

---

## 3. Architecture — six layers

### Layer 1 — Entities
The fundamental objects.

| Entity | Example attributes |
|---|---|
| **Company** | id, name, sector, founded_year, country, business_model, stage |
| **Founder** | experience, education, previous_exits, network, role |
| **Investor** | type, AUM, dry_powder, track_record, portfolio |
| **Fund** | vintage, strategy, LPs, geography, average_ticket |
| **Partner** | role, focus, board_seats |
| **Market** | country, macro, interest_rates, competition, funding_climate |
| **Deal** | round, valuation, amount, terms, lead, date |
| **Product** | repository, website, technology, API, patents |
| **Customer** | segment (enterprise/SMB/consumer), retention, growth |

### Layer 2 — Relationships (ontology)
```
Founder   -[FOUNDED]->        Company
Investor  -[INVESTED_IN]->    Company
Fund      -[OWNS]->           Investor
Company   -[OPERATES_IN]->    Market
Company   -[COMPETES_WITH]->  Company
Founder   -[WORKED_AT]->      Company
Partner   -[SITS_ON_BOARD]->  Company
```
This is effectively an **ontology** of private markets.

### Layer 3 — Events (the dynamic layer)
Databases are static; the VC world is dynamic. Every event **changes state**.
```
FundingRound · Hiring · Patent · ProductLaunch · FounderLeft · NewCEO ·
Acquisition · IPO · CustomerWin · CustomerLoss · Lawsuit · Grant ·
OpenSourceRelease · GitHubActivity
```

### Layer 4 — Signals (behavioral)
A signal is not a datum — it describes *behavior* over time.
```
HiringVelocity · EmployeeChurn · GitHubCommits · FounderPostingFrequency ·
InvestorSyndication · PatentVelocity · ReleaseFrequency · CustomerGrowth ·
WebTraffic · DeveloperActivity · ConferenceTalks
```
Today these live scattered across many sources.

### Layer 5 — Documents (multimodal)
```
PitchDeck · FinancialStatements · News · Blog · PDF · Patent · Code ·
Slack · Emails · Videos · Podcast
```
All become embeddings.

### Layer 6 — Reasoning objects
An AI does not reason directly over raw documents; it reasons over **objects**:
```
Hypothesis · Risk · Opportunity · Competition · MarketFit · TechnologyRisk ·
ExecutionRisk · CapitalEfficiency · FounderQuality · Governance
```
These are *objects*, not outputs.

---

## 4. The Temporal Multimodal Knowledge Graph

From the six layers emerges the core representation: a **Temporal Multimodal Knowledge Graph**.
Each node carries:
- text
- tables
- embeddings
- time series
- images
- events

Edges are typed (the ontology) and time-stamped (events). This is the substrate on which
GNNs, LLMs, and agents operate.

---

## 4b. The Decision Graph (complement to the Knowledge Graph)

The Knowledge Graph captures *what is true*. It is necessary but not sufficient. To study and
improve investing, we also need a **Decision Graph** that captures *how choices were made*:

```
Decision node
  ├── information used     (which signals / documents / twin state)
  ├── alternatives considered
  ├── rationale            (why this over the others)
  ├── decision-maker       (human / AI / hybrid)
  └── outcome              (linked back when it materializes)
```

This makes decisions auditable and learnable, gives a fund organizational memory (why did we
pass on the winner?), and lets us evaluate *process quality* rather than only outcomes.
See `Research_Infrastructure.md` and `Theory.md §2.2`.

## 4c. Uncertainty as a first-class citizen

Every fact, event, signal, and reasoning object carries **confidence + provenance**, and every
model output is **distributional**, not a point:

```
output = { P10, P50, P90, confidence, reasons[], missing_information[], value_of_information }
```

Uncertainty is not metadata bolted on later — it is part of the representation from the start.

---

## 5. Data sources & quality

| Category | Source | Type |
|---|---|---|
| Deals | PitchBook | Proprietary |
| Deals | Dealroom | Proprietary / Freemium |
| Deals | Crunchbase | API |
| Financials | Orbis | Proprietary |
| Founders | LinkedIn | Public / limited API |
| Code | GitHub | API |
| Patents | Google Patents | Public |
| Research | OpenAlex | API |
| News | GDELT | API |
| Web | Common Crawl | Public |
| Hiring | LinkedIn Jobs | Limited API |
| Funding | SEC | Public |
| Macro | World Bank | API |
| Macro | OECD | API |
| VC | OpenVC | Public |

Data-quality dimensions to model explicitly: coverage, freshness, provenance, confidence.

---

## 6. Interface toward AI systems

The model should expose clean interfaces for:
- **LLMs** — retrieval over documents/reasoning objects.
- **GNNs** — graph learning over entities/relationships.
- **Agents** — tools to query entities, events, signals, and to write reasoning objects.

---

## 7. Evolutionary roadmap

```
v0.1  RFC — motivation, principles, ontology sketch, data sources        ← this document
v0.2  Formal ontology (entities, relations, events) + reference schema
v0.3  Temporal graph reference implementation on public data
v1.0  Open standard proposal + evaluation on downstream tasks
```

---

## 8. Open questions

- Minimal viable ontology that both academics and practitioners would adopt?
- How to represent confidence/provenance as first-class citizens?
- How to evaluate a *representation* (downstream task performance vs. intrinsic quality)?
- Legal/ethical boundaries when integrating LinkedIn/PitchBook-derived data?

---

## 9. Why this matters

If we define the universal data model of a private company — entities, relationships, events,
structured and unstructured signals — **everything else in the roadmap is built on top of it**:
knowledge graphs, multimodal models, agentic systems, and eventually a platform. This is a
*scientific* problem, not just a product idea, which makes it a strong topic to discuss with
professors in AI, Information Systems, and Finance — and hard to copy.
