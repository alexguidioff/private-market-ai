# Chapter 9 — Agentic Investment Systems

**Status:** ✍️ draft v0.1 (prose; chapter written from scratch) · **Related:** `Startup_Ideas.md`,
`Roadmap.md`, `Research_Infrastructure.md`
**Level:** 🧭 NORTH STAR

---

## Abstract

Representation (Chapters 4–8) is the foundation; this chapter is about *action*. It asks how AI
systems — increasingly, orchestrated collections of specialised agents — can support the venture
workflow end to end: sourcing, screening, due diligence, memo drafting, and portfolio monitoring.
The central design commitment, consistent with the programme's philosophy (Chapter 1), is
**augmentation, not automation**: agents that *participate* in the investment process and are
grounded in the represented world (the knowledge and decision graphs), while human judgment remains
central. The chapter also confronts the failure modes — hallucination, anchoring, automation bias,
gameability — that make naïve deployment dangerous.

---

## 9.1 The venture workflow as a pipeline

A fund's work decomposes into stages, each a decision point (developed in `Startup_Ideas.md §2`):

```
sourcing → screening → partner review → due diligence → investment committee
        → deal structuring → portfolio monitoring → follow-on → exit
```

Two observations shape where agents help. First, most stages are **information-synthesis under time
pressure** — exactly what LLM-based systems do well. Second, the highest-leverage stages
(screening, partner review, investment-committee support) are the *least* served by existing tools
(Chapter 2), which cluster around single-step due-diligence automation.

## 9.2 Why agents, and why grounded

A single model prompt cannot run a diligence process; the task is multi-step, tool-using, and
requires memory. **Multi-agent systems** decompose it into specialists — a market agent, a team
agent, a technology agent, a financials agent — coordinated by an orchestrator. A recent literature
is forming around exactly this idea for startup evaluation and venture due diligence
🟡 `[ssff2024]`, 🟡 `[dialectic2026]`, 🟡 `[vcdd2026]` (verify before final citation).

The programme's distinctive requirement is **grounding**: agents do not free-associate over the
open web; they read from and write to the represented world of Chapters 4–6 — querying the
knowledge graph and Digital Twins, and recording their conclusions as **reasoning objects** and
**Decision nodes**. Grounding is what connects agentic action back to an auditable representation,
and it is what most current point solutions lack.

## 9.3 A reference architecture (to refine)

```
Orchestrator agent
  ├── Sourcing agent        → ranks/clusters opportunities over the KG
  ├── Specialist agents     → market · team · technology · financials · legal
  │        (each reads KG / Digital Twin, writes Risk/Opportunity reasoning objects)
  ├── Synthesis agent       → drafts the investment memo from reasoning objects
  └── Critic / red-team agent → challenges conclusions, surfaces missing information
Outputs: memo + reasoning objects + a Decision node (with rationale, alternatives, uncertainty)
```

The critic/red-team agent is deliberate: it operationalises the uncertainty commitment (Chapter 10)
by forcing "what don't we know, and what is it worth to find out?" into the workflow, rather than
producing a single confident narrative.

## 9.4 Where agents add most value

From `Startup_Ideas.md §2`, ranked by effort/impact:

| Stage | Human time | AI today | Agentic opportunity |
|---|---|---|---|
| Sourcing | High | Medium | ⭐⭐⭐⭐⭐ ranking/clustering over the KG |
| Screening | High | High | ⭐⭐⭐⭐⭐ grounded first-pass assessment |
| Partner review | High | Almost none | ⭐⭐⭐⭐⭐ structured pro/con with evidence |
| Due diligence | Enormous | Medium | ⭐⭐⭐⭐ specialist agents + memo drafting |
| Investment committee | Enormous | Almost none | ⭐⭐⭐⭐⭐ AI as a participant (Ch.10) |
| Portfolio monitoring | High | Medium | ⭐⭐⭐⭐⭐ event-driven alerts via Digital Twins |

## 9.5 Human-AI collaboration, not replacement

The recurring commitment (Chapters 1, 10): the goal is an AI that *participates*. In the investment
committee, this means an agent that contributes evidence-grounded arguments and flags what is
unknown — not one that outputs a verdict. This raises the research questions of Chapter 10: when do
humans trust the agent, when do they (rightly or wrongly) override it, and does its participation
improve *process* quality? The Decision Graph (Chapter 6) is what makes these questions measurable,
by recording who decided and on what basis.

## 9.6 Failure modes and guardrails

Agentic systems in a high-stakes domain demand explicit safeguards:
- **Hallucination** → grounding in the KG + citation of reasoning-object evidence; no ungrounded claims.
- **Anchoring / automation bias** → the critic agent and uncertainty-first outputs; present ranges
  and dissent, not a single confident answer.
- **Gameability** → founders optimise to whatever agents reward; prefer causal signals (Chapter 10)
  over easily-gamed proxies.
- **Provenance & compliance** → agents respect the data limits of Chapter 7 (no proprietary data in
  shareable outputs; personal-data rules).
- **Evaluation** → agentic pipelines are measured on PrivateBench tasks (Chapter 11), not anecdotes.

## 9.7 Relation to the products

This chapter is the research counterpart to the commercialization arc in `Startup_Ideas.md`: the
Due Diligence Copilot (V2) and Investment Copilot (V3) are productised agentic systems. Research
comes first: the science of grounded, uncertainty-aware, human-augmenting agents is what would make
such products trustworthy rather than merely impressive.

---

## Open questions carried forward
- How to evaluate a *process* (a diligence run), not just a final prediction?
- What is the right division of labour between human and agent at each stage?
- How to prevent multi-agent systems from producing confident consensus that hides uncertainty?

> **Figure F9** (`figures/figures.md#f9`): the grounded multi-agent architecture (specialists +
> synthesis + critic), reading the KG and writing reasoning objects and a decision node.

## To do for this chapter
- [x] Agentic-DD literature verified & cited: `[dialectic2026]` (EACL 2026), `[vcdd2026]`, `[drugdd2025]`.
- [x] Figure F9 drafted (`figures/figures.md`).
- [ ] Connect §9.6 guardrails to concrete PrivateBench evaluation tasks (Chapter 11).
- [ ] Survey more 2024–2026 agentic-DD papers into `papers/notes/` as they are read.
