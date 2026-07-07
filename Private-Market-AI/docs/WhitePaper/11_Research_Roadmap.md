# Chapter 11 — Research Roadmap 2026–2035

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Roadmap.md §4`, `Vision.md §4`,
`Research_Infrastructure.md`
**Level:** 🧭 NORTH STAR

---

## Abstract

This chapter turns the ideas of the preceding chapters into a *sequence of publications* and the
*research infrastructure* that makes the programme cumulative rather than a set of disconnected
papers. It presents the paper arc (from the completed valuation paper to a decision-intelligence
framework), the two enabling assets — a shared benchmark (PrivateBench) and a virtual-fund
Simulator — and a realistic view of dependencies and sequencing. A disclosure note applies
throughout: this full arc is the private "north star"; only the next paper is ever pitched
externally (Chapter 1, §0.1).

---

## 11.1 The paper arc

> **Revised after a 7-pass prior-art scan** (`papers/notes/Prior_Art_Scan.md`; sequenced in
> `Research_Agenda.md`, v0.3). Organised by *whitespace*, not technology. Prediction with graphs/agents is
> crowded (VCBench, GNN & LLM founder-success work) and is deliberately a *component*, not a headline.

Each paper builds on the last, and each sits in a space the scan confirmed is open:

0. **Paper #0 — Explainable ML for Startup Valuation** *(done, WI2026)* `[guidi2026wi]` — the seed.
1. **Paper #1 — Value of Information for VC Diligence** ⭐ (Chapters 9–10). Which missing datum, at
   what cost, most improves the decision. Methods exist (Bayesian optimal experimental design /
   expected information gain / active feature acquisition); the **VC application is academically empty**.
   **Built on a point-in-time, FIBO-aligned representation** (Chapters 4–5) absorbed as its
   foundation — *not* a standalone ontology paper (FIBO / Crunchbase-RDF already exist). *The paper
   pitched to professors now.*
2. **Paper #2 — Decision Quality for VC** (process vs. outcome) (Chapter 10). Was the decision good
   *given what was knowable*? Anchored to the *Management Science* (2024) expert-decision-quality
   framework; evaluated via the Simulator + point-in-time data.
3. **Paper #3 — Human-AI at the Investment Committee** (Chapters 9–10). How AI participation changes
   committee decision quality, trust, and overrides. *Stretch — needs human subjects / a partner fund.*
4. **Paper #4 — Gaming-Robustness of VC Signals** *(continuation)* (Chapter 10). Which signals
   founders game, at what cost, and whether gaming-robust signals coincide with causal ones. Grounds
   **strategic classification** theory in real private-market signals — *not* a from-scratch idea.
5. **Paper #5 — Portfolio-Level Value of Information** *(continuation)* (Chapters 9–11). Budgeted
   information acquisition across a whole deal pipeline to maximise *fund-level* decision quality.
   → **Decision Intelligence for Private Capital Markets** — the integrating framework (Chapter 10).

Deprioritised to *components* (crowded as standalone contributions): standalone ontology,
knowledge-graph/GNN prediction, multimodal representation, conformal valuation intervals, generic
agentic DD. They serve the papers
above but are not the novel claims.

The arc is one question answered in layers (Chapter 3): *how to represent private companies and
support decisions under uncertainty.* A PhD draws its thesis from **P1–P2 (+P3)**; **P4–P5** are
continuation papers (see `Research_Agenda.md`, `Career_Options.md §1`).

## 11.2 As a PhD dissertation vs. a long-term programme

- **A 4-year PhD** would realistically deliver **Papers #2–#4** (representation → graph →
  multimodal), a coherent, examinable thesis. #5+ are the post-PhD continuation.
- **The full arc (#2–#10)** is the decade-scale programme — the thing that turns a thesis into a
  research identity and, eventually, a venture (Chapter 13).

## 11.3 A benchmark — *beyond* VCBench (not the first)

> ⚠️ **Correction (prior-art scan):** a shared VC benchmark **already exists** — **VCBench**
> (arXiv:2509.14448; vcbench.com), "the first benchmark for predicting founder success". The earlier
> claim that "no shared VC benchmark exists" was wrong. Do **not** propose a first benchmark.

VCBench occupies the **founder-success-prediction** slot. What it does *not* cover — and what a new
benchmark could add, explicitly building on it — is evaluation of:
- **Representation quality** — does a shared representation support many tasks without re-engineering?
- **Calibration / uncertainty** — are distributional outputs (P10/P50/P90) well-calibrated?
- **Decision quality** — process vs. outcome (Chapter 10, §10.2), the novel and hardest metric.
- **Value of information** — does the system identify the right next datum to acquire (§11.1, P2)?

So a benchmark contribution remains possible, but only as *"beyond VCBench: a decision-quality /
uncertainty / representation benchmark"*, citing and reusing VCBench where relevant. Rename to avoid
collision. This is a high-leverage but *secondary* contribution — a natural collaboration hook with a
data-capable group (SDSC, HSG; see `Group_Funding_DD.md`), not a headline paper on its own.

## 11.4 The Simulator — a virtual VC fund

Real decision histories are one-shot and private; you cannot re-run them. The **Simulator**
(`Research_Infrastructure.md §2`) is a synthetic environment — startups, founders, investors,
markets, macro — in which agents make sequential investment decisions and receive outcomes over
time. It enables what observational data cannot: controlled comparison of **human vs. AI vs. hybrid**
decision-making, counterfactuals ("what if the fund had passed?"), and training data for
decision-quality research where real labels are scarce. It connects to world models (Chapter 12) and
to the human-AI questions of Chapters 9–10.

## 11.5 Dependencies

```
Paper #0 (done)
   → Paper #1 (representation + point-in-time dataset)  ── needs: ontology (Ch.5), public data (Ch.7)
        → Paper #2 (value of information)               ── needs: #1 + Simulator + BOED/EIG/EDDI methods
        → Paper #3 (decision quality)                   ── needs: #1 (bitemporal/PiT) + Simulator
             → Paper #4 (human-AI committee)            ── needs: Decision Graph + subjects/partner (risk)
Simulator ── built during Y1–Y2; de-risks #2/#3 (ground truth without private data)
Benchmark (beyond VCBench) ── secondary; grows on top of #1; not a headline
Integrating framework ── needs most of the above
```

Note the enabling asset is **Paper #1's point-in-time dataset**: everything downstream reuses it.
The Simulator removes the private-data dependency for #2/#3 (see `Research_Agenda.md §2` on feasibility).

PrivateBench is drawn early because it makes every subsequent paper comparable; the Simulator is
mid-arc because it unlocks the agentic and human-AI work.

## 11.6 Venues (indicative)

- **Information Systems:** WI (where #1 was accepted), ICIS, ECIS — natural home for representation
  and decision-support work.
- **Machine learning:** NeurIPS/ICML workshops for GNN/multimodal/benchmark contributions.
- **Finance / entrepreneurial finance:** for the valuation and causal-signal papers, to reach the
  domain audience (the journals cited in `98_References.md §H`).
Publishing across communities is a feature: it is what makes the work legible to AI, IS, and finance
groups alike (relevant to the multi-disciplinary target list in `Professors.md`).

---

## Open questions carried forward
- Which paper is the right *second* after #2 — #3 (graph) or #5 (uncertainty)? (see `STATUS_MEMO.md`)
- Can PrivateBench v0 be built on public data alone and still be credible?
- What is the minimal Simulator that produces useful decision-quality labels?

## To do for this chapter
- [ ] Define PrivateBench v0 tasks/metrics precisely (with `Research_Infrastructure.md`).
- [ ] Map each paper to a concrete target venue + rough timeline.
- [ ] Add Figure F11: paper × asset dependency graph (see `99_Figures.md`).
