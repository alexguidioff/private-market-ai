# Research Agenda — a Trilogy on Decision Intelligence for Private Markets

**Author:** Alessandro Guidi — v0.3 · **Level:** 🧭 [NORTH STAR — private]
**Inputs:** `papers/notes/Prior_Art_Scan.md` (7-pass prior-art), `Career_Options.md`, white paper.

> **Framing (why "agenda", not "PhD plan"):** the research is the goal; a PhD is one *means* to it.
> The core is a **trilogy** — three questions, three contributions — that stands on a **Foundational
> Study** already done (WI2026). It is built ONLY in whitespace confirmed by the scan, using methods
> that already exist (feasible at a university) applied where no one has applied them (novel).
> Prediction is deliberately NOT the core. This is a *living* agenda — papers get reshaped over time.

> **The trilogy in one line each:**
> 1. *What information should investors collect?* — **Value of Information** (P1, flagship)
> 2. *How should an investment decision be evaluated?* — **Decision Quality** (P2)
> 3. *How should humans and AI decide together?* — **Human-AI committees** (P3)
> These three questions are **domain-general**: they hold for PE, M&A, credit, venture debt — even
> medicine or defense. VC is the entry domain that proves the idea, not the limit of it.

---

## 1. Guiding thesis (what makes it defensible)

Everyone else does **prediction** of private-market outcomes (VCBench, GNNs, LLM founder-success).
This PhD does **decision intelligence**: *value of information*, *decision quality* (process not
outcome), *human-AI* at the committee, and signal *gaming-robustness*. The whitespace, ranked by
the 7-pass scan:

1. **Value of Information for VC diligence** — methods exist (BOED/EIG/EDDI), VC application empty. *(P1)*
2. **Portfolio-level VoI (budgeted diligence)** — no academic formalisation for the pipeline. *(P5)*
3. **Decision quality for VC** (process vs. outcome) — anchor to Mgmt Science 2024 expert-DQ framework. *(P2)*
4. **Human-AI at the investment committee** — industry vision is consensus, rigorous study is open. *(P3)*
5. **Gaming-robustness of signals** — strategic-classification theory exists; empirical VC grounding open. *(P4)*

Representation (FIBO-aligned + point-in-time) is **not a standalone paper** — a startup ontology/KG
already exists (FIBO, Crunchbase-RDF); it is the *foundation inside P1*.

Crowded → avoided as core: founder-success prediction, generic agentic DD, conformal valuation
intervals, "AI augments VC" as a thesis, standalone ontology, "signals are gameable" in the abstract.

---

## 2. Feasibility answer (the question a professor WILL ask)

"How can a PhD student get 'what was knowable when' and measure decision quality?"

| Source of "point-in-time" truth | Feasibility | Role |
|---|---|---|
| **PiT reconstruction from public/licensed data** (timestamps in PitchBook, Crunchbase, GitHub, SEC, news) | ✅ standard practice (quant), laborious | base method for all papers |
| **Simulator** (virtual VC fund — you control the data-generating process) | ✅ you build it | ground truth for decision-quality & VoI without private logs |
| **Real fund decision logs** (anonymised) | ⚠️ only via industry partner | upside/gold standard, NOT a prerequisite |

The methods are off-the-shelf: PiT/look-ahead-bias tooling exists; BOED/EIG/EDDI for VoI exist. The
contribution is **porting them to private-market decisions**, plus the representation + simulator.

---

## 3. The paper sequence (v0.3 — trilogy + continuations)

> The thesis is the **trilogy P1–P3**; **P4/P5** are continuation / post-PhD. A *living* plan —
> reshaped as results and the advisor's group dictate. `papers/notes/Prior_Art_Scan.md` has the
> evidence and the "cite & differentiate" list per paper.

**Foundational Study — (done) Explainable ML for Startup Valuation** — WI2026 (Guidi, Rashid &
Zhong). Not "Paper 0" — the *foundation the trilogy stands on*: non-financial signals price
startups; investor syndicate is the dominant driver; and the limits of a purely predictive approach
motivate the shift to decision intelligence. Proof of competence — no need to return to it.

### P1 — **Value of Information for VC Diligence** ⭐ flagship *(absorbs the old "representation" paper)*
- **Question:** given a decision under uncertainty, *which* missing piece of information — at what
  cost — most improves the decision? (active, budgeted information acquisition for one deal)
- **Core construct — the Information State.** Each investment decision is made from an *information
  state*: not the data that exists, but **what the investor knows at that moment**. This makes VoI
  precise: `Decision(State) → acquire information → State' → Decision(State')`, and VoI is the
  expected improvement in decision quality from moving `State → State'` net of acquisition cost.
  Point-in-time reconstruction (§2) is how the information state is built; it is the formal spine of P1.
- **Built on:** a **point-in-time, FIBO-aligned representation** of private companies (the former
  standalone "P1"), now the *foundation inside this paper* — not a paper on its own (an ontology-only
  paper reads as engineering; prior art: FIBO, Crunchbase-RDF, TGB).
- **Method:** port BOED / Expected Information Gain / EDDI-style active feature acquisition to the
  representation; evaluate on the Simulator (ground truth) + PiT public data.
- **Why feasible & novel:** methods exist (healthcare/experimental design); **VC application empty**.
- **Cite & differentiate:** EVPI/EVSI, EDDI/BOED; FIBO & Crunchbase-RDF (for the representation part).
- **Venue:** ML (NeurIPS/ICML workshop) or Management Science / IS.

### P2 — **Decision Quality for VC (process vs. outcome)**
- **Question:** can we measure whether a VC decision was *good given what was knowable*, separately
  from whether it turned out well?
- **Method:** Decision Graph + bitemporal PiT (from P1) to reconstruct information sets; anchor to
  the *Management Science* (2024) expert-decision-quality ML framework; validate on the Simulator.
- **Why feasible:** builds directly on P1's dataset + simulator; a concept exists to anchor to.
- **Cite & differentiate:** Mgmt Science 2024 (expert DQ); leakage-aware time-based VC ranking
  (MDPI) — they *predict*, we assess *decision quality*.
- **Venue:** Management Science / IS / decision-science venue.

### P3 — **Human-AI at the Investment Committee**
- **Question:** how does AI *participation* change committee decision quality, trust, and overrides?
- **Method:** experiments (partner fund or lab subjects) + the Decision Graph.
- **Why:** the reliance/over-reliance findings are established in HCI; the **VC-committee setting +
  process-quality measurement** is the open contribution.
- **Cite & differentiate:** reliance lit (arXiv 2302.02187, 2401.07058 second-opinions, 2503.03529
  stakes) — established generically; novelty is the VC committee + Decision Graph.
- **Venue:** CHI / CSCW / IS / management. *(Higher coordination cost — needs subjects/partner.)*

### P4 — **Gaming-Robustness of VC Signals** *(new; continuation/stretch)*
- **Question:** which private-market signals do founders actually game, at what cost, and do
  gaming-robust signals coincide with *causal* ones (link to P0 syndicate + the causal thread)?
- **Method:** ground **strategic classification** theory in real VC signals; empirical + causal.
- **⚠️ Positioning:** "signals are gameable" is a mature ML field (strategic classification) — do
  **not** reinvent it. Novelty = *empirical grounding in real private-market signals + causality*.
- **Cite & differentiate:** strategic classification canon (Hardt 1506.06980; 2410.18066; 2505.05594;
  2605.04202).
- **Venue:** ML / IS.

### P5 — **Portfolio-Level Value of Information (budgeted diligence)** *(new; continuation)*
- **Question:** with a limited attention/DD budget across a whole deal pipeline, how should a fund
  allocate information-gathering to maximise *fund-level* decision quality? (P1 scaled from one deal
  to the fund)
- **Method:** Bayesian optimization / bandits / resource allocation over the pipeline; Simulator.
- **Why open:** practitioner triage exists everywhere, but **no academic formalisation** of optimal
  budgeted information acquisition across the pipeline.
- **Cite & differentiate:** BO/bandit resource-allocation methods (transferable, not VC-specific).
- **Venue:** ML / Management Science / IS. Strong applied/grant + product story.

**Integrating chapter (thesis intro/conclusion):** "Decision Intelligence for Private Capital
Markets" — ties P0–P5 into one framework.

---

## 4. Dependency & risk view

```
P0 (done) → P1 value of information (+ PiT representation inside)  ── the enabling asset
              ├─ P2 decision quality        ── needs P1's bitemporal PiT + Simulator
              ├─ P3 human-AI committee       ── needs Decision Graph + subjects/partner (risk)
              ├─ P4 gaming-robustness         ── needs P1 signals + strategic-classification framing + causality
              └─ P5 portfolio VoI             ── scales P1 from one deal to the pipeline
Simulator ── built during Y1–Y2; de-risks P1/P2/P5 (ground truth without private data)
```

**PhD core = P1–P2 (+P3)** (value-of-information with representation inside → decision quality →
human-AI). **P4/P5** are continuation papers (post-PhD or if time allows); the whole set is
deliberately reshuffleable as results dictate.

- **Biggest risk:** P3 (human-AI committee) depends on human subjects / a partner fund → keep as the
  later / stretch item, not the entry paper.
- **Data risk mitigated:** P1's PiT public dataset + Simulator make P1/P2/P5 feasible without private logs.
- **Novelty risk mitigated:** each paper cites its nearest prior art (FIBO & Crunchbase-RDF; EDDI/BOED;
  Mgmt Science 2024 DQ; reliance lit; strategic-classification canon) and differentiates explicitly —
  the #1 reviewer objection is pre-empted (see the table in `Prior_Art_Scan.md`).

---

## 5. Where this can go (outcomes)

- **Academic:** a coherent thesis in an underserved niche → recognizable as *the* "decision
  intelligence for private markets" researcher; venues across IS, ML, and management.
- **Grants:** P1 (value of information — a tool that tells investors what to diligence) + P5
  (fund-level budgeted diligence) are a strong BRIDGE/Innosuisse story — applied, fundable,
  partner-friendly.
- **Company (later):** P1 (value of information) and P3 (human-AI IC) are the research behind the
  Due Diligence / Investment Copilot products (`Startup_Ideas.md`); P5 is literally how a fund
  prioritises work. Science first, company last.
- **Fallback:** the skills (PiT data engineering, representation learning, Bayesian VoI / active
  acquisition, decision modelling) transfer directly to quant/ML roles (`Career_Options.md §3`).

---

## 6. What to pitch to a professor NOW (disclosure discipline)
Only: **P0 (done) + P1 (value of information, with the point-in-time representation as its
foundation)**, and *maybe* mention P2 (decision quality) as "a direction I'm excited about". Not
P3/P4/P5, not the company. (`Outreach_Brief.md`.)

## 7. TODO
- [ ] Read & cite nearest neighbors: EDDI/BOED, Mgmt Science 2024 (expert DQ), strategic-
      classification canon (Hardt et al.), reliance lit, FIBO Investments pkg, VCBench.
- [x] Reframed `Roadmap.md` §4, white paper Ch.11, and `Vision.md §4` (whitespace-first sequence).
- [x] Corrected the "no VC benchmark exists" claim (VCBench exists) in Ch.11 & `Research_Infrastructure.md`.
- [x] Minor follow-ups: Ch.3 (whitespace note), Ch.5 (§5.1.1 FIBO), Ch.10 (§10.6.1 VoI central).
- [x] Sequence v0.2: P1 absorbs representation; added P4 (gaming-robustness) & P5 (portfolio VoI).
- [x] Propagated the v0.2 sequence into `Roadmap.md` §4, white paper Ch.11, and `Vision.md §4`
      (P1 VoI → P2 DQ → P3 human-AI → P4 gaming → P5 portfolio).
- [x] Drafted the 1-page outreach brief centred on P1 (value of information) → `Research_Brief_1page.md`.
- [x] Advisor re-alignment: **Niao He (ETH ODI)** identified as top methods fit (funded + hiring);
      Krause aspirational; HSG (Ademi/Tykvová) as domain co-advisor. See `Group_Funding_DD.md §4a`.
- [ ] Read 2 papers each: Niao He (ODI), Krause (LAS); fill the "why your group" line per target.
- [ ] Fill [brackets] in `Research_Brief_1page.md` and send Wave-1 (He/ODI, Ademi, SDSC application).
