# Chapter 12 — Technology Roadmap & Architecture

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Roadmap.md §3, §3b`
**Level:** 🧭 NORTH STAR

---

## Abstract

Where Chapter 11 sequenced the *science*, this chapter sequences the *technology* and describes the
*software architecture* that would implement it. The technology stages progress from tabular ML to a
decision-intelligence layer; the architecture organises the system into six layers, from raw data to
the human interface, with **uncertainty as a cross-cutting concern** at every level. The stages are a
*logical* order (each depends on the previous), presented against indicative years rather than as
commitments.

---

## 12.1 Technology stages

| Stage | Technology | What it unlocks | Ties to |
|---|---|---|---|
| 1 | **Tabular ML** | interpretable baselines on structured features (the paper) | Ch.8 §8.1 |
| 2 | **Graph Neural Networks** | learning over entities/relationships (syndicate as learned feature) | Ch.6, 8 §8.2 |
| 3 | **Multimodal** | fuse CSV + PDF + deck + website + code into one representation | Ch.8 §8.3 |
| 4 | **Foundation Models** | pretrained, reusable representations of private-market entities | Ch.8 §8.4 |
| 5 | **Agentic Systems** | orchestrated specialists for sourcing, DD, monitoring | Ch.9 |
| 6 | **World Models** | the Simulator — virtual VC fund, counterfactuals | Ch.11 §11.4 |
| 7 | **Reasoning Systems** | from prediction to structured reasoning over decisions | Ch.10 |
| 8 | **Decision Intelligence** | the integrating layer: represent → reason → decide → learn | Ch.10 §10.9 |

> ⚠️ **Read the years as a logical sequence, not a schedule.** The ordering is what matters: each
> stage is motivated by the previous result (Chapter 8, §8.7). Actual timing depends on data,
> funding, and how the field moves.

## 12.2 The six-layer software architecture

The engineering counterpart to the science:

```
┌─────────────────────────────────────────────┐
│ Human Interface Layer   (analysts, IC, memos)│  ← how humans see & steer
├─────────────────────────────────────────────┤
│ Decision Layer          (Decision Graph)     │  ← choices, alternatives, rationale, outcome
├─────────────────────────────────────────────┤
│ Reasoning Layer         (LLMs, agents)       │  ← reason over evidence, not raw docs
├─────────────────────────────────────────────┤
│ Representation Layer    (Digital Twins,      │  ← per-entity dynamic state + uncertainty
│                          embeddings)         │
├─────────────────────────────────────────────┤
│ Knowledge Layer         (Knowledge Graph,    │  ← what is true: entities/relations/events
│                          Ontology)           │
├─────────────────────────────────────────────┤
│ Data Layer              (sources, ingestion) │  ← PitchBook, Crunchbase, GitHub, SEC, ...
└─────────────────────────────────────────────┘
```

Mapping to earlier chapters: Data Layer → Chapter 7; Knowledge Layer → Chapters 5–6;
Representation Layer → Chapters 6, 8; Reasoning Layer → Chapters 9–10; Decision Layer → Chapters 6,
10; Human Interface → Chapter 9 (memos) and Chapter 13 (products).

## 12.3 Uncertainty as a cross-cutting concern

Uncertainty is not a layer; it runs through all of them. The Data Layer records provenance and
confidence (Chapter 7, §7.3); the Knowledge/Representation Layers carry belief distributions
(Chapter 6); the Reasoning and Decision Layers produce and consume the decision object of Chapter 10;
the Human Interface presents ranges and reasons, not point answers. A system that loses uncertainty
at any layer cannot present it faithfully at the top.

## 12.4 Build vs. integrate

The programme's advantage is representation and decision intelligence, not commodity components.
- **Build:** the ontology, knowledge/decision graphs, Digital Twins, the decision layer, and the
  interpretability/uncertainty machinery — the parts that constitute the moat (Chapter 4, §4.8).
- **Integrate:** data connectors, base LLMs, graph databases, embedding models, orchestration
  frameworks — mature, commoditised, and not where the differentiation lies.

## 12.5 Engineering principles

- **Reproducibility** — public-only baselines runnable end to end (Chapter 7, §7.6; `code/`).
- **No proprietary data in shareable artifacts** — licensed data stays out of repos, benchmarks,
  and released models (Chapter 7, §7.7).
- **Auditability** — bitemporal storage so "what we knew when" is always recoverable (Chapters 5–6).
- **Interpretability & uncertainty by default** — non-negotiable at every layer (Chapters 8, 10).

## 12.6 Non-functional requirements (to specify)

Latency (monitoring alerts vs. deep diligence have different needs), scale (millions of entities and
events), provenance/lineage, access control (especially for licensed and personal data), and
evaluation hooks (so any component can be scored on PrivateBench, Chapter 11).

---

## Open questions carried forward
- Which graph database / serving stack best supports a temporal, multimodal, bitemporal graph?
- How to keep interpretability tractable as the Reasoning Layer grows more capable?
- Where is the human-in-the-loop boundary enforced architecturally (Decision Layer)?

> **Figure F12** (`figures/figures.md#f12`): the six-layer architecture with uncertainty as a
> cross-cutting concern.

## To do for this chapter
- [x] Figure F12 drafted (`figures/figures.md`).
- [ ] Specify non-functional requirements (§12.6) concretely.
- [ ] Map each technology stage (§12.1) to the architecture layers it advances.
