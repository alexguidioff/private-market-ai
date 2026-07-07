# Research Infrastructure
## Buildable, citable assets that make the lab defensible

**Author:** Alessandro Guidi — v0.1
**Level:** 🧭 **[NORTH STAR — private]** — the *how* and the moat. Not for early outreach.

Theory (`Theory.md`) needs instruments. This document defines four assets that turn a research
program into a **reference point** others build on. They are the potential "ImageNet moment" of
AI for private markets.

---

## 1. PrivateBench — a benchmark for AI in venture capital

> ⚠️ **Correction (prior-art scan, `papers/notes/Prior_Art_Scan.md`):** a shared VC benchmark
> **already exists** — **VCBench** (arXiv:2509.14448; vcbench.com) — "the first benchmark for
> predicting founder success". The claim below that "no standard benchmark exists" is **outdated**.
> Reposition any benchmark work as *beyond* VCBench, not first.

**Problem (refined):** VCBench covers **founder-success prediction**, but there is no shared
benchmark for the things this programme cares about: representation quality, calibration/uncertainty,
**decision quality** (process vs. outcome), and **value of information**. Prediction is measured;
decision-making is not.

**Proposal:** a benchmark *beyond VCBench* — a public (or partly public) suite that:
- **Reuses / cites VCBench** where founder-success prediction is relevant (don't reinvent it).
- **Adds tasks it lacks** — calibration of distributional outputs (P10/P50/P90), decision-quality
  (process vs. outcome), value-of-information (does the system pick the right next datum?), and
  multi-task evaluation over a shared representation.
- **Datasets** — curated, de-identified, public-source-first (OpenVC, Crunchbase where licensed,
  GitHub, SEC, OpenAlex, GDELT), plus **point-in-time** reconstruction (Research_Agenda P1).
- **Leaderboard** — reproducible baselines (including the WI2026 model).

**Why it matters:** defining the *decision-quality* evaluation vocabulary (not another prediction
benchmark) is the high-leverage, still-open contribution — a natural collaboration hook with a
data-capable group (SDSC, HSG). Secondary to the core papers, not a headline on its own.

> ⚠️ Legal/licensing care: only redistribute what terms allow; prefer public sources and
> derived/de-identified artifacts.

---

## 2. The Simulator — a virtual VC fund

**Idea:** a simulated environment with startups, founders, investors, markets, and
macroeconomics, in which an agent makes sequential investment decisions and receives outcomes
over time.

**What it enables:**
- Compare **human partner vs. AI vs. hybrid** decision-making under identical conditions.
- Study decision *processes* (not just outcomes) — impossible with real one-shot histories.
- Train and stress-test agents; run counterfactuals ("what if the fund had passed?").
- Generate data for decision-quality research where real labels are scarce.

**Why it matters:** a powerful research environment and a compelling demo. Connects to RL,
world models, and evaluation. Can start simple (tabular, stochastic) and grow toward a
learned world model.

---

## 3. Digital Twin theory — a startup as a living object

Formalize each company as a **Digital Twin**: a time-evolving object carrying
```
state · events · embeddings · documents · relationships · uncertainty
```
The twin updates as new events/signals arrive; it exposes belief distributions over latent
qualities (team, market, product) rather than static fields. This is the dynamic, per-entity
counterpart to the (schema-level) Private Market Data Model.

**Research questions:** how to update beliefs online; how to fuse multimodal evidence into a
single coherent state; how to quantify and propagate uncertainty through the twin.

---

## 4. The Decision Graph — beyond the Knowledge Graph

A **Knowledge Graph** captures *what is true* (entities, relations, events). It is necessary but
not sufficient. We also need a **Decision Graph** capturing *how choices were made*:

```
Decision node
  ├── information used     (which signals / documents / twin state)
  ├── alternatives considered
  ├── rationale            (why this over the others)
  ├── decision-maker       (human / AI / hybrid)
  └── outcome              (linked back when it materializes)
```

**Why it matters:**
- Makes decisions *auditable* and *learnable* — you can study process quality (see `Theory.md §2.2`).
- Enables organizational memory: funds forget why they passed on winners; the graph remembers.
- Bridges the epistemological question — it records whether the AI decided or merely supported.

---

## 5. How the four assets fit together

```
Data (sources)
  → Knowledge Graph        (what is true)         ← Ontology + Data Model
  → Digital Twins          (per-entity dynamic state, with uncertainty)
  → Decision Graph         (how choices were made)
  → PrivateBench           (how we measure any of it)
  → Simulator              (where we generate & test decisions)
```

Together they let the lab study the *full loop*: represent → reason → decide → observe → learn.

---

## 6. Sequencing (realistic, not all at once)
1. **PrivateBench v0** on public data — smallest useful version; publishable; collaboration hook.
2. **Uncertainty output** on the existing valuation model — cheap, high-signal, product-relevant.
3. **Decision Graph schema** — design alongside the Data Model / Ontology.
4. **Simulator v0** — tabular, stochastic; grow later.
5. **Digital Twin** formalization — after the graph + uncertainty work.

> Reminder: none of this is early-outreach material. It's the compass that decides *which brick
> to publish next*, one at a time.
