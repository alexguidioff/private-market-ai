# Research · Technology · Commercialization Roadmap (2026–2035)

**Author:** Alessandro Guidi — v0.2
**Level:** 🧭 **[NORTH STAR — private]** — the full roadmap. For outreach, show only the accepted
foundational study → P1 cost-aware Value of Information (use `Outreach_Brief.md`). This document is
your compass, not a pitch deck.

> **Mission:** We build the scientific foundations of **Decision Intelligence for Private Capital Markets**.
> **Research question (public):** How should AI *represent* private companies and *support*
> investment decisions under uncertainty?

This connects the *scientific* agenda, the *technology* stack, the *software architecture*, and
the *commercialization* path.

---

## 1. One-page overview

```
2026  Explainable ML for Startup Valuation      → foundational study (WI2026 accepted)
P0    Formal problem + PiT contract + harness    → executable design and gates
P1    Cost-aware Value of Information            → flagship empirical paper
P2    Decision Quality for VC                     → conditional on P1 assets
P3    Human-AI Investment Committee               → stretch; subjects/partner
P4/5  Gaming robustness + portfolio VoI           → continuations
Later Productization                              → only after buyer and evidence gates
```

---

## 2. Research pillars

| Pillar | Core question | Key methods |
|---|---|---|
| **Representation** | How do we digitally represent a company + its ecosystem? | data model, ontology, embeddings |
| **Explainability (XAI)** | How do we make an investment decision explainable? | SHAP, feature importance, counterfactuals |
| **Decision Intelligence** | How does an investor combine heterogeneous info? | decision modeling, human-in-the-loop |
| **Knowledge Graphs** | How do we connect founders, investors, deals, events? | temporal multimodal KG, GNNs |
| **Agentic Systems** | How do we orchestrate the DD/IC workflow? | multi-agent LLM systems, retrieval |

---

## 3. Technology roadmap (detailed, by year)

| Year | Technology stage | What it unlocks |
|---|---|---|
| 2026 | **Tabular ML** | the thesis — structured features, interpretable baselines |
| 2027 | **Graph Neural Networks** | learning over entities/relationships (founders, investors, deals) |
| 2028 | **Multimodal** | fuse CSV + PDF + deck + website + code into one representation |
| 2029 | **Foundation Models** | pretrained representations of companies / private-market entities |
| 2030 | **Agentic Systems** | orchestrated specialists for sourcing, DD, monitoring |
| 2031 | **World Models** | the Simulator — virtual VC fund, counterfactuals |
| 2032 | **Reasoning Systems** | from prediction to structured reasoning over decisions |
| 2033 | **Decision Intelligence** | the integrating layer: represent → reason → decide → learn |

Data infrastructure is the backbone: without integrated data, none of this works.
**First the data model, then the algorithms.**

> **Note (post prior-art scan):** this stack is the *enabling technology* ("how it's built"), not
> the *publication sequence* ("what's novel"). The research contributions (§4) sit on top of it and
> are chosen for whitespace — value of information, decision quality, human-AI — not for the
> technology stage. Graphs/multimodal/agents are components here, not the headline claims.

---

## 3b. Software architecture (6 layers)

The engineering counterpart to the science — what the platform would look like:

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

Cross-cutting concern at every layer: **uncertainty** (confidence, provenance, missing info).
Details of Decision Graph / Digital Twin / Simulator / PrivateBench: see `Research_Infrastructure.md`.

---

## 4. Research roadmap (papers)

> **Revised after a 5-pass prior-art scan** (`papers/notes/Prior_Art_Scan.md`). The sequence is now
> organised by *whitespace* (where the field is open), not by *technology*. Prediction with
> graphs/agents is crowded (VCBench, GNN & LLM founder-success papers) and is **not** the core.
> Full rationale + feasibility in `Research_Agenda.md`.

```
Paper 0  Explainable ML for Startup Valuation            (done — WI2026; the seed)
   ↓
Paper 1  Value of Information for VC Diligence            ⭐ flagship — with a point-in-time,
         (point-in-time FIBO-aligned representation           FIBO-aligned representation as its
          absorbed as its foundation)                         foundation (not a standalone paper)
   ↓
Paper 2  Decision Quality for VC (process vs. outcome)
   ↓
Paper 3  Human-AI at the Investment Committee            (stretch; needs subjects/partner)
   ↓
Paper 4  Gaming-Robustness of VC Signals                 (strategic classification, empirically
                                                           grounded in real signals + causality)
   ↓
Paper 5  Portfolio-Level Value of Information            (budgeted diligence across the pipeline)
   ↓
        Decision Intelligence for Private Capital Markets (integrating framework)
```

**PhD core = the trilogy P1–P3;** P4/P5 are continuation papers. Full rationale, feasibility, and the
"cite & differentiate" list per paper are in `Research_Agenda.md` and `papers/notes/Prior_Art_Scan.md`.

Open whitespace (from the 7-pass scan): value of information (single-deal & portfolio), decision
quality, human-AI committees, empirically-grounded gaming-robustness. Crowded → avoided as core:
founder-success prediction, generic agentic DD, conformal valuation intervals, standalone ontology,
abstract "signals are gameable" (strategic classification already exists).

---

## 5. Commercialization roadmap (products)

```
V1  Valuation Assistant        — "similar startups price at 15–22M; this looks +35% overpriced"
V2  Due Diligence Copilot      — reads deck, compares to thousands of deals, drafts memo
V3  Investment Copilot         — sourcing + screening + valuation + DD + IC support
V4  Private Market OS          — the decision-intelligence platform (the "Bloomberg")
```

Only *after* the research foundations. Not before.

---

## 6. Career roadmap

```
Amazon → WI2026 paper → Swiss research group → RA / Research Engineer
      → 2–3 papers → BRIDGE / Innosuisse → spin-off → company
```

Realistic timing:
- **Level 1 — Collaboration:** ~2 weeks (nearly immediate).
- **Level 2 — Research Assistant:** 2–6 months (very realistic).
- **Level 3 — Grant:** 6–12 months.

---

## 7. Funding roadmap

| Stage | Instrument | Notes |
|---|---|---|
| Host found | (informal collaboration / RA) | prerequisite for everything |
| Research→innovation | **BRIDGE** | ~12 mo (+6), periodic calls, ~3 mo decision |
| Applied innovation | **Innosuisse** | year-round submission, needs academic host |
| Translation | ETH Pioneer / EPFL Innogrant | later stage |
| Company | Venture Kick | pre-seed, milestone-based |

---

## 8. Milestones & success criteria

- **M1 (P0):** formal problem, protocol, PiT contract, schema, evidence register and smoke harness.
- **M2 (data gate):** source rights/access, cohort audit and utility ranges verified.
- **M3 (EXP-001):** learned cost-aware policy evaluated against frozen baselines on locked PiT data.
- **M4 (external):** replication/partner validation and at least one design partner.
- **M5 (translation):** paid-pilot and regulatory/data-rights gates assessed; no automatic spin-off.
