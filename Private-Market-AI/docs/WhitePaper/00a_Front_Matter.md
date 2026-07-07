# Decision Intelligence for Private Capital Markets
## Foundations, Representation, and Systems

**A Research & Technology White Paper**

**Author:** Alessandro Guidi
**Version:** v0.1 (full draft) · **Level:** 🧭 [NORTH STAR — private]
**Contact:** alexguidioff@gmail.com · alessandroguidi.site · github.com/alexguidioff · linkedin.com/in/alessandroguidi1

> Built on: *Can Non-Financial Signals Price Private Companies? A Machine Learning Approach to
> Startup Valuation* (Guidi, Rashid & Zhong — WI2026 Student Track, accepted).

> ⚠️ **Disclosure discipline.** This is the programme's *north star*, not an outreach document. To
> professors, present only the accepted paper and the next paper (the Private Market Data Model);
> see `../Outreach_Brief.md`. The bigger the vision, the less of it you show early (Chapter 1, §0.1).

---

## Abstract

Public capital markets are served by a mature information infrastructure built on a shared,
machine-readable representation of the world. Private capital markets — venture capital, growth and
private equity, family offices — have no equivalent: decisions worth trillions are made on scarce,
heterogeneous, and deeply uncertain information, using tools that store data rather than represent
the domain. This white paper sets out a long-term research and technology programme to build the
scientific foundations of **Decision Intelligence for Private Capital Markets**.

The programme begins from a concrete, published result. Using 3,403 PitchBook deals and macro data,
the founding paper shows that machine-learning models trained *only on non-financial signals*
(firmographics, deal context, investor syndicate) price private companies competitively with — and
more robustly than — the best financial baselines, that adding financial data yields negligible
improvement ("information saturation"), and that investor-syndicate capacity is the dominant pricing
driver. That result reframes the problem: the durable challenge is not *predicting* a valuation but
*representing* the company and its ecosystem, and *supporting the decisions* made about it under
uncertainty.

From this reframing the paper develops: (i) a six-layer **Private Market Data Model** and an
**ontology** of entities, relationships, events, signals, and reasoning objects; (ii) the temporal,
multimodal **knowledge graph** and a **decision graph** that records how choices are made; (iii) a
technology arc from tabular ML through graph and multimodal learning toward foundation models, and
**agentic systems** that augment rather than replace investors; and (iv) a **theory of decision
intelligence** in which the unit of output is not a point estimate but a decision object — a
distribution with confidence, reasons, missing information, and the value of acquiring it. It closes
with a research roadmap (a benchmark, PrivateBench, and a virtual-fund Simulator), a software
architecture, and a commercialization and funding path — deliberately placed last, after the science.

---

## Executive Summary

**The gap.** Incumbents (PitchBook, Crunchbase, Dealroom, and a wave of AI point tools) are
databases or single-step automations. None is a conceptual, reasoning-ready model of the domain —
the private-markets analogue of what knowledge graphs and shared ontologies (e.g. UMLS in medicine)
provide elsewhere. The durable advantage is **integration and representation**, not any single
dataset.

**The reframing.** Valuation is the first *use case*, not the product; private markets are the
non-negotiable *wedge*, not one case study among many. Ambition (decision intelligence) disciplined
by concreteness (a real domain, real data, a real paper) is the whole strategy.

**Five commitments** distinguish the programme from ordinary predictive modelling: theory over
algorithms; uncertainty over point estimates; causality over correlation; human-AI collaboration
over automation; and shared benchmarks and simulation over anecdotes.

**What gets built.**
- A **representation layer** — data model, ontology, temporal multimodal knowledge graph, per-entity
  Digital Twins, and a Decision Graph that records information, alternatives, rationale, and outcome.
- A **learning arc** — tabular ML → graph neural networks → multimodal → foundation models —
  motivated at each step by the previous result (relational signals dominate → learn on the graph).
- **Agentic systems** — grounded, uncertainty-aware, human-augmenting copilots for sourcing,
  screening, diligence, and committee support.
- A **decision theory** — the decision object (P10/P50/P90 + confidence + reasons + missing
  information + value of information) and the distinction between a good decision and a good outcome.

**How it is pursued.** A paper arc (#1 done → #2 representation → #3 graph → #4 multimodal → …), with
two enabling assets: **PrivateBench** (a shared benchmark to make a fragmented field comparable) and
a **Simulator** (a virtual VC fund for controlled human-vs-AI comparison and decision-quality
research). A 4-year PhD would draw papers #2–#4 from the front of this arc.

**Where it could lead.** Products from an uncertainty-first valuation assistant to a private-market
operating system; a Swiss academic and funding path (RA/Research Engineer → BRIDGE/Innosuisse →
possible spin-off). Science first, company last.

---

## Reading Guide

The document has four movements. Read by interest:

| If you are… | Read first | Then |
|---|---|---|
| A professor gauging fit (AI / IS) | Ch. 1, 3, 4 | Ch. 5–6, 8 |
| A finance / entrepreneurial-finance researcher | Ch. 2, 10 | Ch. 3, 4 |
| An engineer / systems reviewer | Ch. 4, 6, 7, 12 | Ch. 8–9 |
| A grant evaluator (BRIDGE/Innosuisse) | Executive Summary, Ch. 11, 13 | Ch. 3, 10 |
| Yourself (north-star / planning) | all, in order | revisit `STATUS_MEMO.md` |

**The four movements**
1. **Why (Ch. 1–3)** — vision & philosophy, state of the art, grand challenge & research questions.
2. **What to represent (Ch. 4–7)** — data model, ontology, knowledge & decision graphs, data engineering.
3. **How to reason & decide (Ch. 8–10)** — representation learning, agentic systems, decision intelligence.
4. **How it is pursued (Ch. 11–13)** — research roadmap, technology & architecture, commercialization & funding.

> **Remember (disclosure):** for a first professor contact, none of this is sent. Only the WI2026
> one-pager and the 5-pager go out (`../Outreach_Brief.md`, `../WI2026_OnePager.md`).

---

## Status of this draft
Full prose draft (v0.1) of all 13 chapters, with 13 Mermaid figures and a worked example. Pending:
a real public-source worked example (Ch. 4 §4.6), deeper citations (decision science; verify the
agentic-DD references), a machine-readable ontology (v0.2), and a final consistency pass. See
`00_Index.md` for the chapter-by-chapter status and the global TODO.
