# Prior-Art Scan — is the research agenda already taken?

**Date:** 2026-07 · **Level:** 🧭 NORTH STAR · A honest check before investing years in papers #2–#8.

> Bottom line: **the individual building blocks mostly exist already; the *integration* and the
> *decision-intelligence framing* do not.** The gap is real but narrower than "nobody has done this."
> Differentiation must shift from "we build X" (X exists) to "we unify X+Y+Z as a represented,
> uncertainty-aware decision layer, and we standardise it."

---

## Paper #3 — Knowledge Graph / GNN over the VC ecosystem
**Verdict: 🔴 heavily explored. This is NOT novel on its own.**
- Bai & Zhao (?), *GNN-Based VC Investment Success Prediction*, arXiv:2105.11537 — claims SOTA, "surpasses human investors".
- *Scalable Heterogeneous GNNs for High-potential Early-stage Startups*, KDD 2021 (ACM 3447548.3467383).
- *VC-HGCN* (Springer 2024) — two investment networks combined.
- *Enhancing Startup Success Predictions in VC* (GraphRAG), arXiv:2408.09420.
- *Analyze Like a Venture Capitalist: Information-Gain & Knowledge-Enhanced Graph Reasoning*
  (ACL Findings 2026 / arXiv:2512.23489) — LLM + graph reasoning, interpretable theses.
- Nature Sci Rep 2026: *multi-layer AI decision support with knowledge graphs + federated learning*.
- Princeton thesis (2024): co-investment network centrality + SHAP on PitchBook — **strikingly close
  to Guidi et al.**: XGBoost/RF/LogReg, ~45% accuracy, closeness centrality + investor age as drivers.
- **Implication:** a plain "KG + GNN predicts startup success" paper would be *incremental*. Need a
  twist: representation *standard*, temporal/multimodal, uncertainty-aware, or decision-focused.

## Paper #2 — Unified Data Model / Ontology for private markets
**Verdict: 🟡 partially open — the most defensible.**
- Financial-industry ontologies + enterprise knowledge graphs exist (FIBO-style work, EQT Ventures
  essays, arXiv enterprise-KG papers 2602.00029, 2602.01276, 2503.07993).
- BUT: no shared, open, *private-markets-specific* ontology (startup/round/founder/signal/event) with
  a temporal, multimodal, reasoning-ready design and a standardisation ambition (UMLS-style).
- **Implication:** #2 remains the strongest wedge — but must be positioned explicitly as a *standard*
  and against FIBO/enterprise-KG prior art, not as "the first ontology for companies."

## Paper #5/#6 — Uncertainty & Causality in startup outcomes
**Verdict: 🟡 open-ish, but pieces exist.**
- Causal/effectual decision logics in entrepreneurship (Springer 2019, RG 2018) — social-science, not ML.
- *What factors are causal to startup survival?* (RG 2018) — qualitative/quant, not modern causal ML.
- Selection-vs-treatment econometrics on VC financing (disentangling causal effect of VC).
- **Gap:** modern causal-inference ML + distributional/calibrated uncertainty as a *first-class output*
  for valuation is not well covered. This is genuinely more open than the graph work.

## Paper #7 — Agentic Due Diligence
**Verdict: 🔴 crowded and moving fast (2025–2026).**
- DIALECTIC (EACL 2026), VC-DD orchestration (2605.13110), drug-asset DD (2508.16571),
  SSFF (2405.19456), roleplay collective simulation (2512.22608).
- **Implication:** pure "multi-agent DD system" is now a race. Differentiate via *grounding* in the
  represented world (KG + Decision Graph) and *evaluation* (a benchmark), not the agents themselves.

## Paper #8 — Human-AI investment decisions
**Verdict: 🟢 most open for someone with your profile.**
- Rich behavioral literature: algorithm aversion/appreciation (SSRN 4952791; robo-investment
  aversion 2020; delegated investing 2023), trust in human-AI finance (Springer 2026 review),
  AI agents discounting human advice (arXiv:2504.13871).
- BUT: almost all is *retail/experimental*; **VC investment-committee** human-AI dynamics with a real
  decision-process representation (the Decision Graph) are essentially unstudied.
- **Implication:** strong, under-explored niche — and it plays to your business+ML background.

---

## What this means for the agenda (revised positioning)

| Paper | Prior art | Keep? | Required twist |
|---|---|---|---|
| #2 Data Model/Ontology | partial (FIBO/enterprise KG) | ✅ yes — flagship | position as an *open standard*, temporal+multimodal, uncertainty-native |
| #3 KG/GNN | heavy | ⚠️ only as a component | not a standalone "predict success" paper; fold into #2 or add decision/uncertainty angle |
| #5/#6 Uncertainty/Causal | partial | ✅ promising | modern causal ML + calibrated distributional outputs (value of information) |
| #7 Agentic DD | crowded | ⚠️ cautious | differentiate by grounding + benchmark, not the agents |
| #8 Human-AI IC | light | ✅✅ strongest niche | committee-level, with Decision Graph; fits your profile |
| PrivateBench | none found | ✅✅ high-leverage | no shared VC benchmark exists → define it |

**Two conclusions:**
1. The **"predict startup success with ML/graphs"** space is saturated (incl. a Princeton thesis
   almost identical in method to Guidi et al.). Do not build the agenda around prediction.
2. The **defensible core** is the combination the field lacks: an open *representation standard*
   (#2), *uncertainty/causality* as first-class (#5/#6), *human-AI committee* dynamics (#8), and a
   *shared benchmark* (PrivateBench). That is exactly the "decision intelligence, not prediction"
   framing of the white paper — this scan validates that framing.

---

## Second-pass scan (2026-07) — deeper on the promoted papers

### FIBO — the direct prior art for Paper #2 (know it, cite it, differentiate)
- **FIBO (Financial Industry Business Ontology)**, maintained by the **EDM Council** + OMG
  (spec.edmcouncil.org/fibo; github.com/edmcouncil/fibo). A mature, open OWL/RDF ontology defining
  financial *things* (instruments, entities, contracts, ownership) and their relations.
- Packages cover **Foundation, Loans, Investments/Capital Markets, Business & Commerce** — i.e.
  instruments and legal entities, largely **public/regulated markets**.
- There is even a **FIB-DM** (FIBO transformed into an enterprise data model).
- **Differentiation for Paper #2:** FIBO does *not* model private-market-native concepts —
  startup, round, founder, syndicate, growth signals, behavioral events, deal-stage dynamics — nor
  the temporal/multimodal/uncertainty-native design. Position Paper #2 as **"a private-markets
  ontology, aligned-with-but-extending FIBO"**, not a from-scratch first ontology. (Aligning to
  FIBO is itself a credibility signal.)
- **Enterprise Knowledge Graph (EKG):** an architectural pattern (integrate a firm's heterogeneous
  data into one semantic graph), not a standard — confirms the *technology* is mature, so the
  contribution must be the *domain model*, not the graph tech.

### Paper #3 (Uncertainty-Aware Valuation) — ⚠️ less open than hoped
- **Conformal prediction for Automated Valuation Models already exists** (arXiv:2312.06531,
  locally-weighted CP for property AVMs) — i.e. calibrated valuation intervals is a solved *pattern*
  in real estate.
- Rich, active conformal-prediction-in-finance literature: Temporal CP (2507.05470), Conformal
  Predictive Portfolio Selection (2410.16333), distribution-aware CP (2605.26569), Bayesian CP
  (2508.01418).
- **Implication:** "add conformal intervals to startup valuation" is now *incremental* — the method
  is off-the-shelf. The novelty must be **value-of-information + decision object + private-market
  specifics (sparse, survivorship-biased, regime-shifting data)**, not the intervals themselves.
  Consider merging #3 into Paper #2 (representation with uncertainty native) rather than a standalone.

### Paper #6 (Human-AI Investment Committees) — 🟢 confirmed most open, and timely
- Algorithm aversion/appreciation is a live, growing literature (SSRN 4952791 "Algorithm Aversion,
  Appreciation, and Investor Return Beliefs"; trust in human-AI finance review, Springer 2026;
  AI agents discounting human advice, arXiv:2504.13871) — but **retail/experimental**, not VC IC.
- **Implication:** the committee-level, process-representation angle (Decision Graph) is still open
  and now clearly *timely*. Strongest differentiated niche for your profile.

---

## Third-pass scan (2026-07) — benchmark & value-of-information

### ⚠️ PrivateBench — a benchmark ALREADY EXISTS: **VCBench**
- **VCBench** (arXiv:2509.14448; vcbench.com; HuggingFace) — *"the first benchmark for predicting
  founder success in venture capital"*. Standardized, privacy-preserving, anonymized founder
  profiles; split evaluation with F0.5; notes the ~1.9% base rate. Already spawning follow-ups
  (arXiv:2604.00339 "Structured Feature Engineering and Signal Limits for Founder Success").
- Industry benchmarking also exists for *portfolio performance* (Standard Metrics, standardmetrics.io).
- **Implication — this is the biggest correction of the whole scan:** the "no shared VC benchmark
  exists" claim in `Research_Infrastructure.md §1` and Ch. 11 is **now false**. VCBench occupies the
  founder-success-prediction slot.
- **What is still open for a "PrivateBench":** VCBench is **prediction-only** (founder success
  probability). It does NOT cover: *representation* quality, *calibration/uncertainty* metrics,
  *decision-quality* (process vs. outcome), *value-of-information*, or *multi-task* evaluation over
  a shared representation. So a benchmark is still possible — but it must be explicitly
  **"beyond VCBench: a decision-quality / uncertainty / representation benchmark"**, and must cite
  and build on VCBench, not claim to be first. Rename to avoid collision (not "PrivateBench" vs
  "VCBench" confusion).

### Value of information in VC — 🟢 genuinely open (academically)
- Search returns only **practitioner** material: DD checklists, "top 50 DD questions", data-room
  guides (affinity.co, 4degrees.ai, seraf-investor). No formal, academic *value-of-information /
  optimal-information-acquisition* modelling for the VC decision.
- **Implication:** framing diligence as a **value-of-information problem** ("which data most reduces
  decision uncertainty, given its cost") is a real, open, and distinctive contribution — and it ties
  Paper #2/#3 (uncertainty) to Paper #8 (agentic DD: what should the agent go find out?). This may
  be the single most novel technical idea in the whole agenda.

---

## Fourth-pass scan (2026-07) — decision quality & human-AI augmentation

### Decision quality (process vs outcome) — 🟡 exists generally, 🟢 open for VC + ML
- The **concept** is well established outside ML: behavioral work on "good decision ≠ good outcome"
  (RG 2010 "Good decisions, bad decisions"; Forbes/ESMT 2026 outcome-bias experiments; practitioner
  frameworks pmctraining, dsebastien).
- In **ML**, it is emerging but NOT in finance/VC:
  - **"A Machine Learning Framework for Assessing Experts' Decision Quality"** — *Management Science*
    (INFORMS, 2024, doi 10.1287/mnsc.2021.03357) → **the closest prior art**; read and differentiate.
  - Process- vs outcome-based supervision (LessWrong 2022); AutoML agent decision assessment
    (arXiv:2602.22442); decision-oriented text eval (arXiv:2507.01923); LMs in high-stakes decisions
    (arXiv:2410.15471).
- **Implication:** the *idea* of decision-quality ML is no longer virgin territory, but **applying it
  to VC investment decisions** (with the Decision Graph + bitemporal "what was knowable when") is
  open. Must cite the Management Science 2024 framework as the anchor.

### Human-AI augmentation in VC — 🔴 huge *industry* activity, 🟢 thin *academic* study
- Industry is moving fast: SVV free AI platform for investors, Affinity (82% of firms use AI for
  sourcing), Ensemble.vc "Gopi's Manifesto" (machine-augmented process, humans keep top-level
  decisions), Mandalore/venturesquare essays, AI-DD tools with IC-grade citation tracking.
- Consistent industry framing: **"augment, not replace; humans keep capital-allocation decisions"**
  — which *matches* your thesis (validation) but means the *narrative* is now mainstream, not novel.
- BUT this is **product/industry commentary, not rigorous research.** No controlled academic study of
  how AI participation changes IC *decision quality*, trust calibration, or override behavior.
- **Implication:** the augmentation *vision* is now consensus (don't claim it as your insight); the
  *rigorous measurement* of AI's effect on committee decision quality remains open and is your angle.

---

## Fifth-pass scan (2026-07) — methods that make the "hard" parts feasible

### Point-in-time / look-ahead-bias — 🟢 mature *methods*, not yet applied to VC decisions
- Strong, current tooling & theory: **Look-Ahead-Bench** (PiT LLMs in finance, arXiv:2601.13770);
  formal PiT bias taxonomy & bitemporal backtesting (preprints.org 202606.0436; Medium/StockFit
  practitioner pieces); Bailey & López de Prado formalisation.
- **Implication:** the *technique* for "what was knowable at time t" is well established in **public
  markets / quant**. Nobody has ported it to **private-market investment decisions**. So the
  Decision-Graph / decision-quality work is *methodologically supported* (you're not inventing PiT)
  and *domain-novel* (nobody did it for VC). This is the answer to "how would I, at a university,
  manage the hard data part": PiT reconstruction is standard practice, just laborious.

### Value of Information — 🟢 rich ML machinery exists, VC application is empty
- Deep, active literature: Bayesian Optimal Experimental Design / Expected Information Gain
  (arXiv:2302.14545, 2208.00549), **active feature acquisition** (EDDI, ICML — "cost reduction at
  same decision quality", healthcare), VoI in Bayesian evidence synthesis (PMC7034331).
- **Implication (important):** the *methods* to do VoI are off-the-shelf and battle-tested in
  healthcare/experimental design. **Applying "active feature/information acquisition under cost"
  to VC due diligence is the open, transferable contribution.** EDDI-style framing ("which datum, at
  what cost, most improves decision quality") is almost directly portable to diligence.

## Consolidated whitespace (after four passes)
Ranked by how open × how differentiated for your profile:
1. **Value of Information for VC decisions** — 🟢🟢 academically empty; ties uncertainty→diligence→agents.
2. **Decision-quality measurement for VC** (process vs outcome, via Decision Graph) — 🟢 open in
   finance/VC; anchor to Mgmt Science 2024 expert-decision-quality framework.
3. **Human-AI at the investment committee** — 🟢 rigorous study open (industry vision is mainstream).
4. **FIBO-aligned private-market representation standard** — 🟡 open but must position vs FIBO.
5. A benchmark *beyond VCBench* (decision-quality/uncertainty/representation, not founder-success prediction).

Crowded / avoid as primary contribution: founder-success prediction (VCBench + GNN + LLM papers),
generic agentic DD, conformal valuation intervals, "AI augments VC" as a thesis (now consensus).

---

## Sixth-pass scan (2026-07) — per-paper deep dive (P1–P4)

### Paper 1 — Representation + point-in-time (⚠️ weakest on novelty; reposition)
- **Ontology/schema:** exists — FIBO; Crunchbase Open Data Map schema (Organization/People/
  FundingRound/Product/Competitor); **Crunchbase already turned into RDF/KG** (arXiv:1907.08671,
  "Linked Data API and RDF Data Set about Innovative Companies"; CrunchBase Linked Data wrapper).
- **Temporal graph:** mature tech + general benchmarks (Temporal Graph Benchmark / TGB 2.0,
  arXiv:2307.01026, 2406.09639) — but on social/trade/transport, **not private markets**.
- **Point-in-time for VC decisions:** ✅ genuinely open (PiT mature only in public-markets/quant).
- **Verdict:** a "startup ontology / KG" is NOT novel. Novelty = **point-in-time + reasoning-objects
  + uncertainty, oriented to decisions.** → **Reposition: P1 is the foundation *inside* P2, not a
  standalone ontology paper** (an ontology-only paper risks "engineering, not research").

### Paper 2 — Value of Information for VC (🟢🟢 the strongest, still open)
- VoI is a mature decision-theory concept (EVPI/EVSI; Springer ESD special issue; USC 2026 "buying
  price of information"; healthcare/BOED/EDDI) — but **applied to VC diligence: essentially empty**
  (only practitioner material). Confirmed again this pass.
- **Verdict:** keep as the flagship contribution. Method transfer + empty VC application = ideal PhD paper.

### Paper 3 — Decision Quality for VC (🟡 concept exists broadly, VC+ML application open)
- Behavioral base is solid (outcome bias; "good vs bad decisions" RG 2010). In VC there is adjacent
  work — evaluation uncertainty of VC criteria (SSRN 1886225), meta-analysis of bias in venture
  appraisal (RG 2022, 75 studies), signal management/delay (Management Science 2016) — but **not a
  formal process-vs-outcome *decision-quality* measure for VC decisions**.
- ⚠️ Also note **leakage-aware time-based VC ranking** (MDPI 2076-3417/16/6/3082) — someone is
  already doing PiT-aware VC prediction; read it and differentiate (they predict; you assess DQ).
- **Verdict:** open, but crowded *around* it. Must anchor to Mgmt Science 2024 expert-DQ framework
  and lean on the Decision Graph + Simulator to define DQ, not just predict outcomes.

### Paper 4 — Human-AI committees (🟡 rich HCI base, VC-committee application open)
- Very active HCI/decision literature on **reliance/over-reliance/appropriate reliance**
  (arXiv:2302.02187, 2401.07058 "second opinions", 2503.03529 "stakes", 2304.08804 "overriding wrong
  advice"), incl. **group** settings (Purdue thesis 2025 recidivism groups) and expertise paradox
  (arXiv:2509.16772: experts override correct AI).
- BUT: it is lab/recidivism/house-price/hiring — **not VC investment committees**, and not tied to a
  represented decision record.
- **Verdict:** open as *application + Decision-Graph grounding*, but the generic finding ("humans
  mis-rely on AI advice") is well established — your contribution is the *VC-committee* setting and
  the process-quality measurement, not discovering reliance effects.

---

## Seventh-pass scan (2026-07) — the two candidate late papers (gaming; portfolio VoI)

### Candidate P4 — Gaming-robustness of signals — ⚠️ a whole field exists: **Strategic Classification**
- There is a **large, active ML field called "strategic classification"** (Hardt et al. 1506.06980;
  1710.07887; 2302.12355; 2410.18066 "double-edged sword"; 2505.05594 "anticipating gaming to
  incentivize improvement"; 2605.04202 sequential/multi-stage; 2506.01936 reveal-classifier). It
  studies *exactly* agents manipulating features to game a classifier, incl. cost of manipulation,
  gaming-vs-genuine-improvement, and multi-stage settings.
- **Implication (important correction):** "signals are gameable" is NOT an open question — it is a
  mature field with strong theory. A generic "Goodhart for VC" paper would be reinventing strategic
  classification. **BUT** the field is almost entirely *theoretical / synthetic*; applying it to
  **real private-market signals** (which signals founders actually game, at what cost, and whether
  robust signals coincide with causal ones — link to P0 syndicate + your causal thread) is open and
  **empirical**. So P4 survives only if framed as *"strategic classification, empirically grounded
  in real VC signals + connected to causality"*, citing the strategic-classification canon. Not a
  from-scratch idea.

### Candidate P5 — Portfolio/pipeline VoI (budgeted diligence) — 🟢 open academically
- Practitioner material is everywhere (triage, "score every deal, route top decile", AI deck-tagging
  at Sequoia/a16z) but it is **product/ops, not research**. No academic formalisation of *optimal
  budgeted information acquisition across a deal pipeline* to maximise fund-level decision quality.
- Adjacent methods exist to borrow: Bayesian optimization / bandits / resource allocation
  (e.g. MDPI 2504-2289/10/7/206 BO in Wasserstein spaces vs semi-bandit) — transferable, not VC-specific.
- **Implication:** genuinely open as research; natural extension of single-deal VoI (P1) to the fund.
  Strong applied/grant story. Keep as **P5**.

## Final per-paper positioning (what to claim vs. cite)
| Paper | Novelty status | Claim | Must cite & differentiate |
|---|---|---|---|
| P1 Representation+PiT | weak alone | fold into P2; PiT-for-VC is the only novel bit | FIBO, Crunchbase-RDF, TGB |
| P2 Value of Information | 🟢🟢 strongest | flagship: VoI for VC diligence | EVPI/EVSI, EDDI/BOED |
| P3 Decision Quality | 🟡 open-ish | process-vs-outcome DQ for VC | Mgmt Science 2024; leakage-aware VC ranking (MDPI) |
| P4 Human-AI committee | 🟡 open as application | VC-committee + Decision Graph | reliance lit (2302.02187, 2401.07058, 2503.03529) |

## Revised takeaways (after all three passes)
1. **Paper #2 must explicitly align to / differentiate from FIBO.** Not doing so is the #1
   reviewer objection. Private-market-native + temporal + multimodal + uncertainty is the gap.
2. **Uncertainty alone is no longer a strong standalone paper** (conformal AVMs exist). Fold it into
   representation, and lead with *value of information* + *decision object*, which are less trodden.
3. **A benchmark exists (VCBench)** — do NOT claim to build the first. A benchmark contribution must
   be *beyond VCBench*: decision-quality / calibration / representation / multi-task. Rename.
4. **The clearest genuinely-open spaces are: (a) Value of Information for VC decisions, (b) Human-AI
   Investment Committees, (c) a FIBO-aligned private-market representation standard.** Prioritise these.
5. Overall the "decision intelligence, not prediction" thesis holds and is *reinforced*: everyone
   else is doing prediction/benchmarks of prediction; almost no one is doing value-of-information,
   process/decision quality, or committee-level human-AI. That is the whitespace.

## TODO
- [ ] Read the Princeton thesis + arXiv:2512.23489 closely — nearest neighbors to Paper #1; cite and differentiate.
- [ ] Study FIBO's Investments/Capital-Markets package to define exactly what Paper #2 adds.
- [ ] Read the AVM conformal-prediction paper (2312.06531) to scope what's left for startup valuation.
- [ ] Add all these to `98_References.md` (§D FIBO, §G/§I uncertainty & human-AI) once confirmed.
- [ ] Reframe `Roadmap.md`/Ch.11: standard (FIBO-aligned) + value-of-information + human-AI + benchmark.
