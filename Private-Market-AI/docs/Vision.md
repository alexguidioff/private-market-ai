# Decision Intelligence for Private Capital Markets
## Research & Technology Vision — v0.2

**Author:** Alessandro Guidi
**Status:** Living document (updated continuously)
**Level:** 🧭 **[NORTH STAR — private]** — do not present this in full to professors. See §0.0.

> **Mission:**
> We build the scientific foundations of **Decision Intelligence for Private Capital Markets**.
> *(Sub-theme: understand, represent, and augment human decision-making under uncertainty.)*

> **Guiding research question (public version):**
> How should AI *represent* private companies and *support* investment decisions under uncertainty?

---

## 0.0 Grand Challenge

The most fundamental question — the one that outlives any specific technology (LLMs included):

> **How do investors make decisions under extreme uncertainty — and how can AI represent,
> augment, and improve that process?**

Framed this way, **venture capital is the initial domain, not the whole thing.** The same
science later extends to M&A, corporate development, drug-discovery investing, sovereign wealth
funds, infrastructure, and climate investing. This is a *lab-scale* question, not a product idea.

**But — the wedge is non-negotiable.** We do not float free as "a decision-science lab". We
earn credibility in **private capital markets** first: real data, real operators, a real
accepted paper. Ambition (Decision Intelligence) + concreteness (private markets) is the whole
strategy. Neither alone is fundable.

---

## 0.1 Disclosure discipline (how to use this document)

This is the NORTH STAR. It exists so the research does not degenerate into disconnected papers.
It is **not** the thing you show.

- **To a professor, now:** accepted paper → one clear question → concrete idea for **Paper #2**.
  Maybe two possible directions. Stop. No "Bloomberg of private markets", no 2033, no PrivateBench.
- **Why:** professors don't fund 10-year plans; they fund *an excellent first step and the
  ability to nail the second*. The bigger the vision, the less you say early.
- The only documents you actually share: `Outreach_Brief.md` + the WI2026 one-pager.

Natural conversation to have:
> "I wrote a paper on startup valuation. I realized the more interesting problem isn't valuation
> but *how you represent a startup*. Could that become a research line?"

If the professor says *"have you thought about knowledge graphs?"* — you smile. You already know
it's Paper #3. You don't say so.

---

## 0. Executive Summary

This document defines a long-term research and technology vision for building the
scientific and technical foundations of AI systems that support investment decisions in
private capital markets. The current master thesis and the accepted WI2026 paper are the
**first step** of a much broader research agenda.

The core reframing behind this program:

- We are **not** building "software that estimates startup valuations."
- We are building the **representation and decision-intelligence layer** for private markets
  — a domain where, unlike public markets (served by Bloomberg, Refinitiv, FactSet), no
  unified, machine-reasoning-ready model of the world yet exists.
- **Valuation becomes one use case**, downstream of a deeper problem: *how do we digitally
  represent a company, its ecosystem, and the events and signals that describe it, so that
  AI systems can reason about investment decisions?*

---

## 1. Background

### 1.1 Who
Alessandro Guidi — MSc in Management (ESCP Business School), Product Manager @ Amazon,
PMP certified. Rare combination of business background (ESCP), industrial experience
(Amazon, Capgemini), and applied ML skills, plus a peer-reviewed publication in a niche
research area.

### 1.2 Origin of the research
- **Accepted paper (Guidi, Rashid & Zhong):** *Can Non-Financial Signals Price Private Companies?
  A Machine Learning Approach to Startup Valuation* — **WI2026 Student Track**.
- **Master Thesis:** *Machine Learning for Startup Valuation.*
- **Method:** progressive 3-layer design (OLS financial baselines → non-financial ML →
  full-data ML), 3,403 PitchBook deals + GEM macro data, strict out-of-time holdout across the
  2022 correction; interpretable via SHAP.
- **Key findings:** ML on **non-financial signals alone** matches the best financial baselines
  (Layer-2 Random Forest: best MAE 0.888, R² 0.557) and generalizes more robustly across market
  regimes; adding financial + macro data adds negligible value ("information saturation");
  **investor-syndicate capacity** is the dominant pricing driver (SHAP).

### 1.3 The problem identified
As a *product*, "an ML model that estimates valuation" is weak: the space is crowded
(PitchBook, Dealroom, CB Insights, Carta, AngelList, Harmonic, Crunchbase AI, internal VC
tools), and even a strong model leaves substantial residual uncertainty — hard to sell as
"the right price."

As a *technology base*, the framework is strong: it already integrates firm, investor, deal,
and macro conditions, and it is interpretable. This is the seed of something much bigger.

---

## 2. State of the Art

Today's landscape is fragmented. **Everyone is building pieces; no one is building the
complete system.**

- **PitchBook** — deep structured data; integrating AI for sourcing, due diligence,
  benchmarking, research (incl. enterprise LLM integrations).
- **Crunchbase** — APIs with fundamentals, LLM-generated insights, predictive models meant
  to be consumed by downstream AI.
- **Dealroom / CB Insights / Orbis / Capital IQ** — databases with partial coverage.
- **AI Due Diligence startups** (e.g. ToltIQ, Xapien, and similar) — automate *single pieces*
  of the investment process.

**The key gap:** all of these are *databases* or *point solutions*. None is a **conceptual
model of the domain** — an explicit representation of the entities, relationships, events,
and signals that a reasoning system needs. This is a well-known distinction in computer
science: databases describe data; they do not necessarily represent the world.

**Implication:** the durable competitive advantage will not be a single dataset. It will be
**integration + representation** — the layer on top of which knowledge graphs, multimodal
models, and agentic systems can be built.

---

## 3. Vision

### 3.1 Reframing
| From (initial idea) | To (this program) |
|---|---|
| Startup-valuation startup | Decision Intelligence for Private Capital Markets |
| A model | A theory + an infrastructure |
| One prediction | Hundreds of decisions per investment |
| Prediction | Decision-making under uncertainty |
| A product | A platform (the "Bloomberg of private markets") |

### 3.1.1 Research Philosophy
Most labs build *algorithms*. This one aims to build a **theory** plus the infrastructure to
test it — so it survives the churn of models (today LLMs, tomorrow something else). Five
commitments distinguish it:

1. **Theory over algorithms** — an *Investment Intelligence Theory* (see `Theory.md`): what a
   decision is, what a signal is, what uncertainty is, how they combine.
2. **Uncertainty over point estimates** — never "valuation = 18M"; instead P10/P50/P90 +
   confidence + reasons + missing information + value of information.
3. **Causality over correlation** — which signals *cause* a good outcome, not merely predict it.
4. **Human-AI over automation** — AI that *participates* in the investment committee, not one
   that replaces it. When do humans trust it? When do they override it?
5. **Benchmarks & simulation over anecdotes** — shared evaluation (`PrivateBench`) and a
   virtual-fund simulator (see `Research_Infrastructure.md`).

### 3.2 Why valuation is only the first use case
A fund makes hundreds of decisions per investment — sourcing, screening, partner review,
due diligence, investment committee, structuring, portfolio monitoring, follow-on, exit.
Valuation is *one* of these. The roadmap should therefore flow:

```
Decision Intelligence
    → Deal Intelligence
        → Valuation
        → Due Diligence
        → Portfolio Intelligence
        → Investment Committee Intelligence
```

not the other way around.

### 3.3 10-year vision
The goal is not an algorithm and not a single product. It is the **foundational scientific
and technological infrastructure** on which future AI systems for VC, PE, Growth Equity,
Family Offices, and M&A can be built.

---

## 4. Long-Term Research Agenda

A coherent line of research, each item a potential paper. **This full list is NORTH STAR** —
externally you only ever discuss P0 (done) and P1 (next).

> **Revised after a 7-pass prior-art scan** (`papers/notes/Prior_Art_Scan.md`; sequenced in
> `Research_Agenda.md`, v0.3). Ordered by *whitespace*, not technology. Prediction (graphs/agents/
> founder-success) is crowded → treated as components, not headline papers.

0. **Explainable ML for Startup Valuation** *(done — WI2026)* — the seed.
1. **Value of Information for VC Diligence** ⭐ — which datum, at what cost, most improves the
   decision (BOED/EIG/EDDI methods; VC application open). **Built on a point-in-time, FIBO-aligned
   representation** absorbed as its foundation. ← **the one you pitch next.**
2. **Decision Quality for VC** — process vs. outcome; anchored to the Management Science (2024)
   expert-decision-quality framework.
3. **Human-AI at the Investment Committee** — how AI participation changes decisions/trust/overrides
   *(stretch; needs subjects/partner)*.
4. **Gaming-Robustness of VC Signals** — strategic classification, empirically grounded in real
   private-market signals + causality *(continuation)*.
5. **Portfolio-Level Value of Information** — budgeted diligence across the whole pipeline *(continuation)*.
→ **Decision Intelligence for Private Capital Markets** — the integrating framework.

*Components (crowded as standalone; serve the papers above):* standalone ontology / knowledge graph /
GNN, multimodal representation, conformal valuation intervals, agentic DD, a benchmark *beyond VCBench*.

The single most important next scientific step is **P1**: value of information, with the point-in-time
representation as its foundation. Everything downstream reuses that representation.

> **Companion documents (NORTH STAR):** the *why* lives in `Theory.md`; the paper plan + feasibility
> in `Research_Agenda.md`; buildable assets (simulator, digital twin, decision graph, benchmark) in
> `Research_Infrastructure.md`; prior-art evidence in `papers/notes/Prior_Art_Scan.md`.

---

## 5. Technology Roadmap (2026–2035)

```
2026  Explainable ML for Startup Valuation      (tabular ML)
2027  Private Market Data Model                 (unified representation)
2028  Knowledge Graph for Private Markets        (temporal graph)
2029  Multimodal Startup Representation           (multimodal AI)
2030  AI Due Diligence Copilot                    (retrieval + agents)
2031  Investment Committee Copilot                (reasoning / decision support)
2033+ Private Market Operating System             (decision-intelligence platform)
```

Technology stages:
1. **Tabular ML** — the thesis.
2. **Multimodal AI** — CSV + PDF + deck + website.
3. **Knowledge Graph** — everything becomes a graph.
4. **LLM reasoning** — not prediction, reasoning.
5. **Multi-agent systems** — orchestrated specialists (likely the future of DD).

---

## 6. The Private Market Data Model (summary)

*(Full treatment in `Private_Market_Data_Model.md`.)*

A private investment is not a number — it is a **dynamic system**. Represent it in six layers:

1. **Entities** — Company, Founder, Investor, Fund, Partner, Deal, Market, Product,
   Customer, Technology, Patent, Employee, Document, Event.
2. **Relationships** — FOUNDED, INVESTED_IN, OWNS, OPERATES_IN, COMPETES_WITH, WORKED_AT,
   SITS_ON_BOARD (an ontology).
3. **Events** — funding round, hiring, product launch, founder left, new CEO, acquisition,
   IPO, customer win/loss, lawsuit, grant, open-source release, GitHub activity.
4. **Signals** — hiring velocity, employee churn, GitHub commits, founder posting frequency,
   investor syndication, patent velocity, release frequency, customer growth, web traffic.
5. **Documents** — pitch deck, financials, news, blog, patent, code, email, video, podcast
   (→ embeddings; multimodal).
6. **Reasoning objects** — hypothesis, risk, opportunity, competition, market fit, technology
   risk, execution risk, capital efficiency, founder quality, governance.

From these emerges a **Temporal Multimodal Knowledge Graph**, where each node carries text,
tables, embeddings, time series, images, and events.

---

## 7. Data Sources

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

No one has *all* of it. The advantage is **integration**, not any single feed.

---

## 8. Research Questions

- How should private companies be represented digitally?
- Which signals matter most, and how stable are they over time?
- How can AI *explain* an investment decision?
- How should heterogeneous, multimodal data be integrated?
- How does a human investor combine such information?
- Can an AI *participate* in investment-committee reasoning (not replace it)?
- Can we define an open ontology/standard for private markets (analogous to SNOMED CT / UMLS
  in medicine)?

---

## 9. Startup Vision

Product evolution — *after* the research foundations, not before:

```
V1  Valuation Assistant
V2  Due Diligence Copilot
V3  Investment Copilot
V4  Private Market Operating System
```

Moats to build over time: proprietary data, user feedback loops, uploaded documents,
network effects (every fund that uses it improves the model), and verticalization
("AI for venture capital", not "startup valuation").

---

## 10. Academic Strategy

Target institutions (Switzerland-first):
1. University of St. Gallen (HSG)
2. ETH Zurich (incl. ETH AI Center)
3. Swiss Data Science Center (SDSC)
4. EPFL
5. University of Zurich (UZH)

Also relevant in Europe: TUM, JKU, Bocconi, Oxford, Cambridge, Imperial.

Outreach principle: **do not ask for supervision.** Ask for *methodological feedback*.
> "Our paper was accepted at the WI2026 Student Track. I'm seeking methodological feedback
> from researchers working on Explainable AI and startup finance."

Goal of the first months: become *recognizable* as an applied researcher on **AI for Venture
Capital and Private Markets**, then convert 1–2 warm contacts into collaboration / RA roles.

*(Full outreach playbook in `Professors.md`.)*

---

## 11. Funding Strategy

- **BRIDGE** (SNSF/Innosuisse) — turns research into innovation; ~12 months (+6 extension);
  periodic calls; decision ~3 months after submission.
- **Innosuisse Innovation Projects** — submittable year-round; needs a motivated academic host.
- **ETH Pioneer Fellowship**, **EPFL Innogrant**, **Venture Kick** — later-stage options.

Key insight: grants require a **host/group first**, then the proposal. Find the group, then
write the grant — not the reverse.

*(Full treatment in `Funding.md`.)*

---

## 12. Action Plan

### Next 30 days
- Academic CV, Research Statement, WI2026 one-pager.
- Google Scholar, ORCID, personal website, clean public GitHub (no proprietary data).
- Build database of 15–30 target groups; read ≥2 papers each.
- Send first 5 personalized emails; schedule first calls.

### Next 6 months
- Convert calls into collaboration / RA / Research Engineer conversations.
- Draft **Private Market Data Model v0.1** as an RFC.
- Begin Paper #2 (representation).

### Next 2 years
- 2–3 additional papers.
- Secure host group → apply for BRIDGE / Innosuisse.
- Prepare ground for a possible spin-off.

---

## 13. Open Questions

- What is the minimal viable ontology that professors and practitioners would adopt?
- Which decisions in the VC/PE workflow have the best effort/impact ratio for AI?
- How to build proprietary data advantage ethically and legally (LinkedIn/PitchBook terms)?
- How to measure "decision quality" as an evaluation target, not just prediction error?

---

## 14. The Path (career)

```
Amazon
  → WI2026 paper
    → Swiss research group (HSG / ETH / EPFL)
      → Research Assistant / Research Engineer
        → 2–3 papers
          → BRIDGE / Innosuisse
            → Spin-off
              → Private Market AI company
```

---

*This is deliberately a v0.1 — a working base, not the final document. The long-term ambition
is a 50–100 page technical white paper (structured like a research-lab manifesto) that can be
shown to professors, used for grants, and eventually become the manifesto of a company.*
