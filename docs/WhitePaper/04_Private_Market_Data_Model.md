# Chapter 4 — The Private Market Data Model

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Private_Market_Data_Model.md`, `Ontology.md`
**Level:** 🧭 NORTH STAR — the intellectual core (Paper #2 / Paper #0 of the agenda).

---

## Abstract

This chapter presents the central proposal of the programme: a **Private Market Data Model** — a
unified, temporal, multimodal representation of private companies and their ecosystem, designed so
that AI systems can *reason* over it rather than merely retrieve from it. The model is organised
in six layers (entities, relationships, events, signals, documents, reasoning objects), treats
time and uncertainty as first-class, and is deliberately source-agnostic. The claim is that this
representation layer — not any single model or dataset — is the missing foundation on which
valuation, ranking, due diligence, monitoring, and committee support become special cases.

---

## 4.1 Motivation: databases store, they do not represent

Chapter 2 showed that today's incumbents are databases (PitchBook, Crunchbase, Dealroom, Orbis,
Capital IQ) and point predictors. A database answers *"what value is in this field?"* It does not
answer *"what is true about this company, how did we come to believe it, how confident are we, and
how has it changed?"* Those are representation questions, and they are prerequisites for reasoning.

The distinction is standard in computer science and was resolved, in other domains, by explicit
models of the world: knowledge graphs for web-scale heterogeneous data `[hogan2021kg]`, and shared
biomedical ontologies such as UMLS `[bodenreider2004umls]`. Private markets have no equivalent. A
**private investment is not a number; it is a dynamic system** — company, founders, investors,
funds, partners, deals, markets, products, customers, patents, documents, and events — all
connected and evolving. The data model must represent that system.

## 4.2 Design principles

1. **Representation over storage** — model entities, relationships, events, and signals explicitly,
   not as flat records.
2. **Temporal by default** — every fact carries a time; state changes are driven by events.
3. **Multimodal** — text, tables, time series, images, code, and documents are first-class.
4. **Reasoning-ready** — expose objects an AI can reason *about* (risks, hypotheses), not just raw data.
5. **Source-agnostic** — integrate any feed; **integration is the moat**, not any single source.
6. **Open and extensible** — designed as a candidate open standard (Chapter 5).

These principles are what separate a *model of the domain* from a schema for a particular dataset.

## 4.3 The six-layer architecture

### Layer 1 — Entities
The fundamental objects and their core attributes: **Company** (sector, stage, geography,
business model), **Founder** (experience, education, prior exits, network), **Investor** (type,
AUM, dry powder, track record), **Fund** (vintage, strategy, LPs, ticket), **Partner**, **Market**
(macro, rates, funding climate), **Deal** (round, valuation, amount, terms, lead, date),
**Product** (repository, website, technology, patents), **Customer** (segment, retention, growth).
*(Full attribute catalog in Chapter 5 / `Ontology.md`.)*

### Layer 2 — Relationships
Typed edges form the ontology: `FOUNDED`, `INVESTED_IN`, `OWNS`/`MANAGED_BY`, `OPERATES_IN`,
`COMPETES_WITH`, `WORKED_AT`, `SITS_ON_BOARD`. This layer is what turns a table of companies into
a graph of an ecosystem — and it is exactly where the founding paper's key driver lives: the
**investor syndicate** is a *relationship structure*, and its "certification effect"
`[hochberg2007]` is a property of the graph, not of any single node. A representation that makes
relationships explicit captures what the paper found predictive `[guidi2026wi]`.

### Layer 3 — Events (the dynamic layer)
Databases are static; the VC world is not. Events — funding round, hiring, product launch, founder
departure, new CEO, acquisition, IPO, customer win/loss, lawsuit, grant, open-source release,
GitHub activity — **change entity state over time**. Modelling events explicitly is what makes the
representation temporal rather than a snapshot, and is a precondition for the out-of-time,
regime-aware analysis that the founding paper showed matters.

### Layer 4 — Signals (behavioral)
A signal is not a datum; it describes *behavior* over time: hiring velocity, employee churn,
GitHub commit cadence, founder posting frequency, investor syndication, patent velocity, release
frequency, customer growth, web traffic. Signals have strength, cost, timeliness, correlation, and
gameability (Chapter 10). Today they live scattered across sources; the model gives them a home.

### Layer 5 — Documents (multimodal)
Pitch decks, financial statements, news, blogs, patents, code, emails, videos, podcasts — the
unstructured majority of what investors actually read. These become embeddings attached to the
entities and events they concern, making the representation multimodal rather than tabular.

### Layer 6 — Reasoning objects
An AI does not reason directly over raw documents; it reasons over **objects**: hypothesis, risk,
opportunity, competition, market fit, technology risk, execution risk, capital efficiency, founder
quality, governance. These are the bridge between evidence (layers 1–5) and judgment (Chapter 10),
and they are *objects in the model*, not transient outputs.

## 4.4 Time and uncertainty as first-class citizens

Two cross-cutting commitments distinguish this model from a schema.

- **Time.** Every fact, event, and signal is timestamped; entity state is the accumulation of
  events. This supports the regime-aware, out-of-time evaluation that the founding paper showed is
  essential for honest performance estimates.
- **Uncertainty.** Every fact carries confidence and provenance, and every model output is
  distributional rather than a point:
  `output = { P10, P50, P90, confidence, reasons[], missing_information[], value_of_information }`.
  Uncertainty is designed in, not bolted on — the theoretical basis is Chapter 10.

## 4.5 From representation to reasoning: the interfaces

The model is useful only if AI systems can consume it. It exposes three interfaces:
- **LLMs** — retrieval over documents and reasoning objects.
- **GNNs** — learning over the entity/relationship graph (Chapter 6, 8).
- **Agents** — tools to query entities/events/signals and to *write* reasoning objects (Chapter 9).

This is where the model connects to the rest of the agenda: the knowledge and decision graphs
(Chapter 6) are built on it, representation learning (Chapter 8) learns over it, and agentic
systems (Chapter 9) act through it.

## 4.6 A worked example

To make the six layers concrete, we model a single company across all of them. The company below —
**"NimbusAI"** — is **illustrative and synthetic**: the values are representative, not real, so that
no unverified claim is made about an actual firm. In a real instantiation, every field would be
populated from the public sources of Chapter 7 (OpenVC, Crunchbase where licensed, GitHub, SEC,
GDELT) with provenance and confidence attached. This example doubles as the seed for a PrivateBench
task (Chapter 11).

> ⚠️ Illustrative data. Replace with a real, public-source-populated company for the final cut and
> for PrivateBench; keep this synthetic version in the text to avoid asserting unverified facts.

**Layer 1 — Entities**
```
Company:  NimbusAI — sector: dev-tools/AI infra, founded: 2021, country: CH,
          business_model: open-core SaaS, stage: Series A, status: active
Founders: F1 (ex-Google, 2nd-time founder, CS PhD), F2 (ex-startup CTO)
Investor: Alpha Ventures (VC, early-stage, strong dev-tools track record)
Fund:     Alpha Fund III (vintage 2022, EUR 250M, European seed/Series A)
Market:   European AI-infrastructure — large TAM, cooling funding climate (2023)
Deal:     Series A — amount EUR 12M, pre-money EUR 40M, lead: Alpha Ventures, date: 2023-03
Product:  GitHub repo (OSS core) + hosted platform + public API
```

**Layer 2 — Relationships**
```
F1 -[FOUNDED]-> NimbusAI            F2 -[FOUNDED]-> NimbusAI
F1 -[WORKED_AT]-> Google            Alpha Ventures -[LED_BY]-> Series A deal
Alpha Fund III -[MANAGED_BY]-> Alpha Ventures
NimbusAI -[OPERATES_IN]-> European AI-infrastructure market
NimbusAI -[COMPETES_WITH]-> {two incumbents}
Alpha Ventures -[co-invests with]-> {two known dev-tools investors}   <- the syndicate
```
Note the syndicate substructure: it is precisely this pattern (a lead with a strong track record,
co-investing with reputable dev-tools investors) that the founding paper found to be the dominant
pricing driver `[guidi2026wi]` — a *relationship*, not a firm attribute (Chapter 5, §5.3).

**Layer 3 — Events (timeline)**
```
2021-06  FundingRound (pre-seed)      2022-01  Hiring wave (eng.)
2022-04  OpenSourceRelease (v1.0)     2022-09  CustomerWin (first enterprise)
2023-03  FundingRound (Series A)      2023-05  Hiring (senior GTM)
2023-08  ProductLaunch (hosted API)
```
State is the accumulation of these events; each has a timestamp, source, and confidence.

**Layer 4 — Signals (behavioral, over time)**
```
github_commits:       rising through 2022, plateau early 2023
hiring_velocity:      +40% headcount in 12 months (verify window)
investor_syndication: lead + 2 reputable co-investors (high "certification")
web_traffic:          steady growth post-OSS release
```

**Layer 5 — Documents (multimodal -> embeddings)**
```
- Series A pitch deck (PDF)          - GitHub README + code
- 2 news articles (funding, launch)  - founders' public talks (video/transcript)
```
Each is embedded and linked to the entity/events it concerns.

**Layer 6 — Reasoning objects**
```
Hypothesis:     "Open-core distribution will convert to enterprise revenue."
Opportunity:    "Strong developer adoption (GitHub signal) precedes monetization."
Risk (Tech):    "Thin moat vs. incumbents bundling similar features."
Risk (Exec):    "GTM hire recency -> unproven enterprise motion."
FounderQuality: "2nd-time founder + relevant domain -> above-baseline."
```

**Cross-cutting — the decision object (Chapter 10) this supports**
```
Fair-value range (Series A):  P10 EUR 30M · P50 EUR 42M · P90 EUR 58M
Confidence:                   medium
Top reasons:                  syndicate quality; founder track record; OSS traction
Missing information:          revenue/retention detail; enterprise pipeline
Value of information:         churn & pipeline data would most reduce the range
```
The pre-money of EUR 40M sits just below P50 — "roughly fair, mildly attractive if the missing
information resolves positively" — exactly the range-with-reasons output the programme argues for,
rather than a single confident number.

## 4.7 Evolutionary roadmap

```
v0.1  RFC — motivation, principles, six-layer sketch, data sources           ← current
v0.2  Formal ontology (types, attributes, cardinalities) + reference schema  ← Chapter 5
v0.3  Temporal graph reference implementation on public data                 ← proof of concept
v1.0  Open-standard proposal + evaluation on downstream tasks                ← adoption
```

## 4.8 Why this is the core

If the representation is defined well, **everything downstream becomes a special case**: valuation
is a query plus a model over the graph; due diligence is structured traversal and reasoning-object
generation; monitoring is event subscription; committee support is reasoning over shared objects.
This is why Paper #2 targets representation, not another predictor — and why it is a *scientific*
contribution (a model of a domain) rather than a product feature. It is also the hardest part to
copy, because the advantage is integration and design, not a single dataset.

---

## Open questions carried forward
- Serialization: RDF/OWL vs. labeled property graph vs. JSON-schema-first? (Chapter 5)
- How to represent confidence/provenance efficiently at scale?
- How to evaluate a *representation* — intrinsic quality vs. downstream task performance? (Chapter 11)
- Legal/ethical limits of integrating LinkedIn/PitchBook-derived data? (Chapter 7)

> **Figure F4** (`figures/figures.md#f4`): the six-layer stack with time + uncertainty as
> cross-cutting concerns.

## To do for this chapter
- [x] §4.6 worked example drafted (synthetic "NimbusAI" across all six layers + decision object).
- [ ] Replace the synthetic example with a **real, public-source-populated** company for the final
      cut and for PrivateBench (OpenVC/Crunchbase/GitHub/SEC/GDELT), with provenance + confidence.
- [x] Figure F4 drafted (`figures/figures.md`).
- [ ] Pull the formal attribute catalog from `Ontology.md` into Chapter 5 and cross-reference.
- [ ] Add a short note connecting Layer 2 (relationships) to the paper's syndicate finding with a diagram.
