# Chapter 6 — Knowledge Graph & Decision Graph

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Private_Market_Data_Model.md §4–4b`,
`Research_Infrastructure.md §3–4`
**Level:** 🧭 NORTH STAR

---

## Abstract

The ontology of Chapter 5 defines the vocabulary; this chapter defines the *structures* built from
it. Two are needed. The **Temporal Multimodal Knowledge Graph** represents *what is true* about the
private-market ecosystem — entities, relationships, and events over time, with multimodal content
on every node. The **Decision Graph** represents *how choices were made* — the decisions, the
information used, the alternatives, the rationale, and the outcome. The first is necessary but not
sufficient; investing is a sequence of decisions, and a system that seeks to support (and learn
from) them must represent the decisions themselves, not only the facts.

---

## 6.1 The Temporal Multimodal Knowledge Graph

A knowledge graph is the natural home for the ontology `[hogan2021kg]`: entities become nodes,
relationships become typed edges, and the whole is queryable and learnable. Two properties make
this graph specific to private markets:

- **Temporal.** Every edge and node carries time; the graph is not a snapshot but a history, with
  state produced by the accumulation of events (Chapter 5, §5.4). This is what allows the
  out-of-time, regime-aware analysis that the founding paper showed is essential `[guidi2026wi]`.
- **Multimodal.** Each node carries more than fields — text, tables, embeddings, time series,
  images, events. A company node links its filings, its pitch deck, its GitHub activity, and its
  hiring time series, not just its sector code.

This graph is the substrate on which the later technical chapters operate: representation learning
and GNNs (Chapter 8) learn over it; agents (Chapter 9) query it.

## 6.2 Digital Twins: the per-entity dynamic view

Where the knowledge graph is the global structure, a **Digital Twin** is the per-entity view: a
time-evolving object for a single company (or founder, or fund) that carries its
`state · events · embeddings · documents · relationships · uncertainty`
(from `Research_Infrastructure.md §3`). The twin updates as new events arrive and exposes *belief
distributions* over latent qualities — team strength, market fit, execution risk — rather than
static fields. It is the natural unit for monitoring and for the uncertainty-aware outputs of
Chapter 10.

## 6.3 The Decision Graph: representing how choices were made

A knowledge graph captures facts; it does not capture *decisions*. Yet investing is a sequence of
choices, and the object of the programme is to support and improve them. The **Decision Graph**
represents each decision explicitly:

```
Decision node
  ├── information used     (which signals / documents / twin state)
  ├── alternatives considered
  ├── rationale            (why this option over the others)
  ├── decision-maker       (human / AI / hybrid)
  └── outcome              (linked back when it materializes)
```

This is, to our knowledge, largely absent from existing private-market tooling, and it is where
several strands of the programme converge.

## 6.4 Why the Decision Graph matters

- **Auditability and learning.** Because decisions link to the information available *at the time*
  (via the bitemporal knowledge graph, Chapter 5 §5.7) and to outcomes when they materialise, the
  Decision Graph makes it possible to study **process quality** — whether the reasoning was sound
  given what was knowable — rather than only realised returns (the distinction developed in
  Chapter 10, §2.2 of `Theory.md`).
- **Organizational memory.** Funds routinely forget *why* they passed on a company that later
  succeeded. The Decision Graph records the rationale and the counterfactual, turning tacit
  judgment into a queryable asset.
- **The human-AI boundary.** By recording the `decision-maker` (human / AI / hybrid), the graph
  makes explicit the question of Chapter 10: did the AI *decide*, or merely *support*? This is the
  substrate for studying trust, overrides, and the effect of AI participation (Chapter 9).

## 6.5 Querying and learning over the graphs

The graphs are designed to be consumed by three kinds of system (Chapter 4, §4.5):
- **GNNs** learn over the knowledge graph — e.g. propagating investor-quality signals along
  `INVESTED_IN` edges, operationalising the certification effect `[hochberg2007]` as a learned
  graph feature.
- **LLMs / retrieval** operate over node documents and reasoning objects.
- **Agents** traverse both graphs, read reasoning objects, and write new ones and new Decision
  nodes (Chapter 9).

## 6.6 Relationship between the structures

```
Ontology (Ch.5)  →  Knowledge Graph      (what is true; global, temporal, multimodal)
                 →  Digital Twins         (per-entity dynamic state + uncertainty)
                 →  Decision Graph         (how choices were made; links info → outcome)
```

The knowledge graph and Digital Twins are the *world model*; the Decision Graph is the *record of
action* within it. Together they close the loop the programme is built on — represent → reason →
decide → observe → learn.

---

## Open questions carried forward
- Concrete schema for the Decision node, and how outcomes are linked back over time (bitemporal).
- How to bootstrap a Decision Graph without access to a fund's private decision history? (synthetic
  / simulator seeding, Chapter 11)
- How to evaluate whether the graph representation improves downstream decisions, not just predictions?

> **Figure F6** (`figures/figures.md#f6`): knowledge graph + Digital Twins + Decision Graph and the
> represent → reason → decide → observe → learn loop.

## To do for this chapter
- [x] Figure F6 drafted (`figures/figures.md`).
- [ ] Specify the Decision node schema formally (align with Chapter 5 conventions).
- [ ] Connect §6.5 (GNN over syndicate edges) to a concrete Paper #3 experiment sketch.
