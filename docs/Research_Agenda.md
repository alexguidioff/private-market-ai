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
3. **Decision quality for VC** (process vs. outcome) — anchor to Mgmt Science 2025 expert-DQ framework (Dong, Saar-Tsechansky & Geva). *(P2)*
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
| **PiT reconstruction from public data** (SEC filings, dated issuer/investor evidence, OpenAlex and audited web archives) | ✅ core already built; enrichment is laborious | reproducible public information state and observed outcome proxies |
| **Model-reviewed public pilot** | ✅ 20 cases, owner-accepted for method development | Layer-A plumbing and label-sensitivity audit; not human gold |
| **Human-adjudicated public benchmark** | ⚠️ optional/not completed | required before publication-grade strong-round claims |
| **Simulator** (virtual VC fund — you control the data-generating process) | ✅ implemented as a conditional synthetic harness | synthetic ground truth for recovery/counterfactual tests |
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
- **Frozen P0 question:** for one company at one fixed decision time, which information block—if
  any—should be acquired before `continue_diligence` vs `stop`, given cost and delay?
- **Implemented cohort:** US technology-related primary issuers with non-amendment Form D anchors
  in 2016–2020. This is not yet a verified software/startup/seed/VC-backed population.
- **Decision and weak outcome:** decision time is 12 months after public filing availability; the
  observed label is a later non-amendment Form D notice within 18 months. It is not a priced
  institutional follow-on, Series A or success label. A 20-case model-reviewed public pilot is
  accepted for method development and sensitivity analysis; publication-grade stronger claims would
  still require independent human adjudication under `../datasets/P1_OPEN_SOURCE_LABEL_PLAN.md`.
- **~~Primary claim (v0.3, falsified 2026-07-29)~~:** a learned cost-aware policy produces higher **Net
  Decision Value** than every preregistered non-VoI baseline on a locked temporal test cohort.
  **Result: 0 of 15 declared utility-by-cost cells (EXP-001C).** The falsification clause below fired.
- **Primary claim (v0.5, sharpened by EXP-009) — the condition is about direction, not incidence.**
  *Selective value of information requires the **direction** of a decision change to be predictable, not
  merely its **incidence**. Incidence can be predicted at AUC 0.95 while direction stays at r ≈ 0, and a
  policy targeting incidence then scales harmful changes at the same rate as helpful ones.*
  This is the strongest sentence to come out of EXP-005 → EXP-009 and it belongs in the working paper.
  **Why it is harder to dismiss than v0.4.** EXP-005 was open to the objection "your gain model was bad".
  EXP-009 removes that: the intermediate quantity is predicted at AUC **0.770 / 0.679 / 0.950** across the
  three utilities — against EXP-005's per-case gain correlations of +0.015 / −0.070 / +0.000 — and the
  policy still wins **0 of 15** cells, best advantage +0.0025 against a declared margin of 0.005.
  The mechanism is explicit: the score is `P(change) × E[gain|change]` with the second term a population
  constant, and among changes 64% help / 36% hurt under `balanced` with that mix flat in P(change). The
  policy buys action, not correctness. It also has almost no dynamic range — 94.6% acquisition at cost 0,
  0.1% at cost 0.1 — collapsing onto the all-or-nothing threshold EXP-005 identified as correct.
  ✅ **Pre-run predictions logged in the script docstring and all three correct**: E[gain|change] positive
  under `balanced`, negative under `false_positive_averse`, and "roughly 42% helped" in the latter —
  observed **42.0%**, derived arithmetically from EXP-005 rather than guessed. `experiments/EXP-009/REPORT.md`.
- **Superseded claim (v0.4, after EXP-005) — retained for the record.** *Selective, per-case value of
  information can only beat all-or-nothing acquisition when per-case gain is both heterogeneous and more
  predictable than the outcome itself; in private-market diligence the first holds and the second does
  not.* Correct but less precise: it did not name incidence-versus-direction, which is the distinction
  that closes the obvious repair route. The contribution is the condition, the instrument that separates
  it from the alternatives, and the demonstration that the failure is model-side rather than regime-side:
  - **Instrument (reusable):** an oracle policy acquiring where the *realised* gain exceeds cost gives the
    least upper bound on any selective policy. Oracle advantage above margin + learned advantage at zero
    = model-side; oracle advantage below margin = the regime genuinely does not pay. This decomposition
    is what EXP-001C lacked and is transferable to any VoI application.
  - **Evidence:** oracle beats the strongest baseline by **+0.065 to +0.087** (6–9x the declared 0.010
    margin) while corr(predicted, realised) is **+0.015 / −0.070 / +0.000**. 13 of 15 cells model-side.
  - **Structural argument:** per-case gain is nonzero only where the base and acquired models act
    differently *and* the outcome adjudicates. Predicting it = predicting the base model's residual =
    beating the base model at its own task. With base AUC 0.59–0.65, the gain model inherits that ceiling
    and loses further to variance.
  - **Constructive residue:** the population mean *is* estimable, and it changes sign with the utility
    (+0.028 balanced, −0.008 false-positive-averse). So the acquire/do-not-acquire decision belongs to
    the utility function at cohort level, which is the P5 formulation.
  - **This is not substituting a prediction metric for a decision metric** — the prohibition in the
    falsification clause. NDV remains the metric; the claim moved from "my policy wins" to "here is when
    no policy of this family can, and here is how to tell".
- **Core construct — the Information State.** `I_t` is the observable/public information defensibly
  available at `t`, not all data that exists and not unobserved private fund knowledge.
- **Built on:** a point-in-time, FIBO-aligned representation as infrastructure inside P1—not a
  standalone ontology contribution.
- **Evaluation:** public PiT real-data branch with an explicitly scoped weak outcome proxy and a
  model-reviewed pilot for sensitivity analysis, plus a multi-world synthetic branch. Synthetic
  ground truth validates recovery/counterfactual plumbing; it does not establish market realism or
  real-world performance. Independent human adjudication is reserved for publication-grade strong
  empirical claims.
- **Protocol:** `protocols/P1_VoI_Protocol.md`; data contract: `../datasets/P1_DATA_CONTRACT.md`.
- **Falsification:** if the learned policy does not beat the strongest baseline on test NDV and
  preregistered sensitivity checks, pivot the flagship claim rather than substituting a prediction metric.
  **⚠️ Fired 2026-07-29.** EXP-001C: 0/15. Pivot executed above (v0.4), diagnosis in
  `experiments/EXP-005/REPORT.md`. Recording that the clause fired and was honoured, rather than quietly
  rewriting the claim, is the point of having written it down in advance.
- **Falsification for v0.4:** the claim now rests on the oracle gap being real. It dies if the oracle
  advantage does not survive (i) a second, qualitatively different information block, or (ii) elicited
  rather than assumed utilities. If a richer state representation ever pushes corr(predicted, realised)
  above the 0.05 floor *and* converts it into an NDV win, the condition is wrong and must be retracted —
  the structural argument makes that unlikely, not impossible.
- **Cite & differentiate:** EVPI/EVSI, EDDI/BOED; FIBO & Crunchbase-RDF for representation.
- **Venue:** ML (NeurIPS/ICML workshop) or Management Science / IS.

### P2 — **Decision Quality for VC (process vs. outcome)**
- **Question:** can we measure whether a VC decision was *good given what was knowable*, separately
  from whether it turned out well?
- **Method:** Decision Graph + bitemporal PiT (from P1) to reconstruct information sets; anchor to the
  expert-decision-quality ML framework of **Dong, Saar-Tsechansky & Geva, *Management Science*
  71(7):5696–5721, 2025** (DOI 10.1287/mnsc.2021.03357; preprint arXiv:2110.11425). ⚠️ **Year corrected
  2026-07-29: it is 2025, not 2024** — earlier notes in this file and the outreach material were wrong.
  Validate on the Simulator.
- **Why feasible:** builds directly on P1's dataset + simulator; a concept exists to anchor to. Their
  setting is the one that actually obtains — abundant records of past decisions, scarce instances with
  ground truth — which is P2's core problem and also P1's weak-proxy situation, so the anchor is closer
  than "a concept to point at".
- **Cite & differentiate:** Dong, Saar-Tsechansky & Geva 2025 assess the quality of decisions *already
  taken*; P1 asks whether to buy information *before* taking one, and P2's contribution is the VC
  setting plus the point-in-time reconstruction of what was knowable. Leakage-aware time-based VC
  ranking (MDPI) and the *Information* 2026 leakage-controlled startup-prediction paper *predict*; we
  assess *decision quality*.
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
- **Measurement dependency (EXP-002).** A budgeted policy only ever examines the top slice of a
  pipeline, so its performance is governed by tail behaviour, not by average discrimination. EXP-002
  shows the two can diverge materially on the same data: SEC issuer history yields ROC-AUC 0.61 while
  concentrating 1.45x enrichment in its top 5%, transporting across a CIK-disjoint boundary. P5 must
  therefore be evaluated with tail-lift and precision@k, not AUC; optimising an average metric for a
  budgeted decision optimises the wrong quantity. Tooling: `code/tail_lift.py`.
- **⬆️ Promoted by EXP-005, and P1's failure is P5's argument.** P1 tried to allocate information
  per case and failed because per-case gain is unpredictable. P5 does **not need that quantity** — a
  budget allocated across a pipeline needs the population-level trade-off, which EXP-005 shows is
  estimable (mean gain +0.028 under `balanced`, sd 0.41, sign flipping with the utility). So the
  sequence P1 → P5 is no longer "scale it up": it is *the per-case formulation is provably the wrong
  granularity, and here is the right one*. That is a stronger motivation than the original framing.
  ⚠️ **The caution is UNRESOLVED, not confirmed. EXP-007 said confirmed; EXP-008 corrected it the
  same day.** EXP-008 added a random ordering as a control, and a random top-5% slice diverges from the
  cohort by **−0.0936** — larger than the −0.0230 of the real ordering. Real orderings diverge in 4 of
  36 cells, the control in 1 of 9: the same rate. With n=92 and per-case sd 0.41 the standard error on a
  top-5% mean is ~0.043, so an arbitrary subsample routinely differs from the cohort by more than the
  cohort mean itself.
  **The correct statement is a precision one, not a bias one: inside the slice a budget works, the
  trade-off is not estimable at this cohort size.** Neither transfer nor its failure is established.
  That is the binding constraint on P5 and no method design fixes a standard error — it needs a
  materially larger cohort, a lower-variance outcome, or a formulation that does not require a
  slice-restricted mean. `experiments/EXP-008/REPORT.md` supersedes EXP-007's interpretation; EXP-007's
  measurements stand and its report carries the correction at the top rather than being rewritten.
  The EXP-007 numbers below are reproducible; read them as descriptive, not as evidence of divergence:
  - `balanced`: cohort mean **+0.0284** collapses to **+0.0054** in the top 5% and **+0.0055** in the top
    10%, difference **−0.0230 [−0.0434, −0.0019]** and **−0.0229 [−0.0434, −0.0044]** — intervals exclude
    zero, so this one is established, not directional. Fivefold overstatement.
  - `false_positive_averse`: cohort mean **−0.0081** (the block destroys value before cost) becomes
    **+0.0587** in the top 10%. Sign flip, and the decision flips at every cost up to 0.05 — but every
    difference interval contains zero, so it is a point-estimate flip only. With n=92 and sd 0.41 the
    standard error is ~0.042, five times the quantity being tested. That imprecision is part of the finding.
  - `opportunity_averse`: every slice from 5% to 50% has mean gain **exactly 0.0000**. The cohort's
    +0.0030 is generated entirely *outside* the slice a budget reaches.
  - The all-or-nothing decision changes in **20 of 75** cost×utility×slice cells.
  **This fixes P5's formulation rather than killing it:** the budgeted problem must estimate the
  trade-off *inside* the slice, on 5–10% of the sample. `experiments/EXP-007/REPORT.md`.
  **~~Constructive residue: the slice mean rises monotonically, so gain concentrates where the base model
  is least confident.~~ Withdrawn by EXP-008.** The monotone trend tests at Spearman −0.479 with
  **p = 0.174** — not established. The decile profile shows something different and weaker: under
  `balanced`, gain concentrates in the *lower-middle* of the probability range (deciles 3–4, mean +0.0710
  and +0.0984, p range 0.196–0.254), with the share of decision changes peaking at 56.3% in decile 5.
  Middle four deciles +0.0430 against extremes +0.0123 clears the declared 0.010 margin, so the shape
  favours the uncertainty reading over the descending one — but only **one of ten** decile intervals
  excludes zero with no multiplicity correction, and the shape **does not replicate** under the other two
  utilities (`false_positive_averse` p = 0.715, `opportunity_averse` p = 0.814, with deciles 4–10 exactly
  zero). Whatever structure exists belongs to one payoff matrix.
  ⚠️ **Design error in EXP-008, recorded:** the "base uncertainty" ranking returned numbers identical to
  the probability ranking, because the base model never predicts above **0.474** — every case sits below
  0.5, so `-|p-0.5|` is a monotone function of `p`. Check (b) therefore ran with two independent
  alternatives (offering size, investor count) plus the control, not four. Separately worth noting: with
  a 29.2% base rate and a maximum predicted probability of 0.474, the base model never asserts an
  outcome is more likely than not.

### Methodological thread — **measuring information value under a budget constraint** *(new)*
- **Observation:** the VoI literature (EVPI/EVSI, BOED/EIG, EDDI) evaluates acquisition with
  expected-utility or average predictive criteria. Practitioners under a capacity constraint act only
  on an extreme slice. The metric and the decision are therefore mismatched, and the mismatch is
  measurable rather than rhetorical: EXP-002 documents an average-versus-tail divergence on the P1
  cohort.
- **Why this may be publishable in its own right:** the prior-art scan found no formal treatment of
  *which metric* should govern information-acquisition decisions under capacity constraints in
  private markets. Extremal quantile regression and tail-dependence estimation exist in
  finance/EVT; precision@k and partial AUC exist in ranking. Neither literature addresses
  information *acquisition* under a budget.
- **Status:** empirical observation with a reusable estimator, not yet a paper. Requires (a)
  separating mechanical persistence from economic signal, (b) at least one qualitatively different
  block, (c) elicited utilities to convert lift into decision value.
- **Cite & differentiate:** extremal quantile regression; tail dependence coefficients; partial
  AUC / precision@k in ranking; EVPI/EVSI and EDDI for the acquisition framing.
- **Carrier:** strengthens P1's discussion and is a precondition for P5. Could stand alone as a short
  methods paper if the mechanical component can be separated convincingly.

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

- **Biggest *coordination* risk:** P3 (human-AI committee) depends on human subjects / a partner
  fund → keep as the later / stretch item, not the entry paper.
- **Biggest *systemic* risk — the Simulator, not the data.** The Simulator underpins P1, P2 and P5,
  so its credibility as an evaluation environment is a single point of failure for half the arc. Data
  availability is a problem of *effort*; the Simulator is a problem of *validity*. It is therefore the
  first asset to be validated (before P2/P5 build on it), via **triangulation** rather than any single
  test: (a) stylized-facts matching — reproduce known VC regularities *not imposed by hand* (power-law
  returns, stage-wise failure rates, and the syndication→survival effect that is P0's own finding);
  (b) point-in-time calibration on open data; (c) outcome correlation *aggregated across cohorts* so
  macro shocks average out (outcome is a noisy, confounded signal — never the sole judge, to avoid
  outcome bias, cf. P2); (d) robustness/ablation. Circularity is broken by a **separation of roles**:
  the world's hidden data-generating process is sealed from the tested policy (which sees only the
  point-in-time information state and must *discover* what matters), and validation criteria are
  *external* to the world's designer. The *method* (as opposed to the world) is validated by a
  **multi-world recovery study**: thousands of worlds with random hidden parameters, scoring the
  *per-world correlation* between true and estimated importance (not the average, which is trivially
  passable) as a sanity check, then the cost-aware VoI-ranking agreement as the real test. The
  method is judged on **regret** (decision value − cost of information acquired), not on how much it
  learned; the Simulator carries three hidden truths it must handle unseen — weights (what matters),
  costs (what it takes to know: abstract first, then market-proxied from the PiT data's natural
  public-vs-private cost hierarchy, with sensitivity analysis), and luck (noise / macro shocks). See
  white paper §11.4.1–11.4.8.
- **Structural / construct-validity risks** (distinct from novelty risks) are catalogued with their
  defences in `Threats_to_Validity.md` — notably: the public information state ≠ what the VC knew (P1);
  the non-existent decision-quality ground truth outside the Simulator (P2, defended by triangulated
  labels incl. Ademi-style expert elicitation); the Simulator's stylized-facts risk (with a Plan B
  cascade and a Year-1 exit criterion); and causal claims requiring identification (Simulator + E-value
  sensitivity, not bare observational claims). Key structural insight: **P3/P5 depend on P1, not P2**,
  so the arc is resilient to a weak P2.
- **Data risk mitigated, not eliminated:** P1's open-only SEC PiT core, model-reviewed Layer-A pilot
  and Simulator make method development feasible without private logs. Publication-grade VC-specific
  claims would still require independent human evidence or a partner dataset.
- **Novelty risk mitigated:** each paper cites its nearest prior art (FIBO & Crunchbase-RDF; EDDI/BOED;
  Mgmt Science 2025 DQ (Dong, Saar-Tsechansky & Geva); reliance lit; strategic-classification canon) and differentiates explicitly —
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

**Update 2026-07-29 — lead with EXP-005, not with P1's original claim.** For a methods group (LAS, ODI)
the negative result plus its diagnosis is the strongest item in the file, and stronger than a passing
gate would have been. The pitch is three sentences: a preregistered cost-aware acquisition policy lost
0/15 cells; an oracle bound shows a winning policy exists (+0.065 to +0.087), so the failure is the
selector rather than the cost regime; and the reason is structural, because per-case gain is the base
model's residual and predicting it means beating the base model at its own task. It shows preregistration
honoured, a clause fired and obeyed, an instrument built to separate rival explanations, and one of my own
hypotheses withdrawn as a category error. That is the behaviour a supervisor is screening for at the
aptitude colloquium. **Do not present it as a setback** — and equally, do not oversell the oracle: it uses
the outcome, so it bounds what is possible and does not demonstrate an implementable policy.

## 7. TODO
- [ ] Read & cite nearest neighbors: EDDI/BOED, Mgmt Science 2025 (Dong, Saar-Tsechansky & Geva, expert DQ), strategic-
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
- [x] Wave-1 sent 2026-07-29: D-INFK portal (LAS named), LAS group list, ODI form, eligibility pre-check.
      Record in `outreach/SUBMISSION_LOG.md`.
- [x] **EXP-005** — separated (a)/(b)/(c) behind EXP-001C's 0/15. Result: (c) withdrawn as a category
      error; failure is model-side in 13/15 cells; oracle gap proves a winning policy exists. P1 claim
      pivoted to v0.4 above. `experiments/EXP-005/REPORT.md`.
- [x] **EXP-007** — the population-level trade-off restricted to the top-k slice. Result: it does **not**
      transfer. 7 sign flips, 2 magnitude shifts, 6 transfers across 15 slice-utility cells; 20 of 75
      all-or-nothing decisions change. The pre-run prediction (gain concentrates where the base model is
      least confident, so the slice mean shrinks) was correct and is on the record in the script docstring.
      `experiments/EXP-007/REPORT.md`.
- [x] **EXP-008** — tested the monotonicity, and it corrected EXP-007 instead of extending it. Check (a)
      fails: the shape does not replicate across utilities. Check (b) partially void: the uncertainty
      ranking was degenerate (see design error above). Check (c) not addressed. The decisive addition was
      a **random control**, which diverges more than any real ordering — so EXP-007's divergence is inside
      noise. `experiments/EXP-008/REPORT.md`.
      *Method note worth keeping:* the control cost four lines and overturned a same-day conclusion. Add a
      null-ordering control to every slice-restricted estimate in this project by default.
- [x] **EXP-009 Part A — calibrated null, done.** 400 random orderings per utility. **The cleanest
      statement of the sample-size problem this project has produced:** under `balanced` the cohort mean
      gain is +0.0284 and the *median* divergence of an arbitrary top-5% slice is **+0.0284**. At the slice
      size a budget works, the typical meaningless deviation equals the entire quantity being estimated.
      3 of 27 ordering×slice cells clear the null against 1.35 expected — not compelling.
- [x] **EXP-009 Part B — change-targeting closed, informatively.** Objection tested first as declared and
      *survived* (a change is worth something, sign stable within a utility). Premise also held (incidence
      far more predictable than direction). Policy still 0/15. Logged so the route is not silently resumed.
- [ ] **One lead survives, worth one test and not a direction.** Offering size clears the calibrated null
      at two nested slices under `false_positive_averse` (+0.1004 at 5%, +0.0559 at 10%). Unadjusted for
      multiplicity and the only structure in 27 cells. Deal size may carry slice-level structure under a
      false-positive-averse utility. One targeted test, then drop it.
- [ ] **DECIDE THIS BEFORE DESIGNING ANOTHER EXPERIMENT ON THIS COHORT.** Four of the last five
      experiments were limited by the same arithmetic, not by method. Pick one:
      (i) materially larger cohort — widen the anchor years or drop the technology restriction;
      (ii) lower-variance outcome — the per-case sd of 0.41 comes from a binary decision on a weak proxy;
      (iii) a formulation that never requires a slice-restricted mean — which is a change to P5's question,
      not to its method. Continuing to design experiments before choosing is how the last four got spent.
- [ ] Estimate the slice-restricted trade-off from information available *at the decision time*.
      EXP-007 and EXP-008 both use realised gain, so they describe where gain *is*, not where it can be
      predicted to be.
- [x] **EXP-010 — the v0.5 condition tested as a mechanism, with a gate that could have killed it.**
      5×3 grid (base ROC-AUC 0.614→0.840), 40 synthetic worlds per cell, 1,500 cases each, two costs.
      **0 of 30 tests refute**, and the learned selective policy is *significantly worse* than the best
      fixed baseline in every cell (−0.0018 to −0.0064, intervals over worlds excluding zero) while an
      oracle prize of +0.0217 to +0.0562 existed everywhere — the real-data structure of EXP-005
      reproduced where we control the generator. `experiments/EXP-010/REPORT.md`, paper §4.9.
      ⚠️ **One declared prediction was refuted and it changed the mechanism we assert.** I predicted the
      predicted-realised gain correlation would *rise* as the base state anticipates the block, giving a
      trade-off frontier (predictable-but-small vs large-but-blind). It **falls**: 0.056, 0.049, 0.038,
      0.024, 0.007 at intermediate base strength. There is no frontier — anticipating the block makes the
      prize small *and* the direction less predictable, because a rare quantity is estimated with more
      noise. Worse for selective acquisition than what I assumed, which is why it is on the record.
      The residual correlation peaks where the signal is *independent* of the base state, consistent with
      it being incidence leaking in rather than direction — EXP-009 reproduced in a controlled generator.
      **Limit that matters:** the sweep's model class is correctly specified throughout, so the one route
      by which the condition could still fail on real data — a misspecified base model leaving a
      structured residual — is precisely what the synthetic design cannot exhibit. Not a substitute for
      the second real block.
- [ ] **P1 is now three items from submittable, and two need you rather than more experiments.**
      (i) Read three papers properly: Alur et al. (arXiv:2306.01646), Dong/Saar-Tsechansky/Geva
      (arXiv:2110.11425), EDDI (arXiv:1809.11142). The other five §1.1 entries can stay abstract-level for
      a working paper; these three cannot. (ii) Choose the venue, which splits the material: §8.6 for an
      ML workshop, §6+§9 for Management Science / IS. Keeping them fused past this point costs, because
      each section that serves one weakens the other. (iii) Optionally register for a free USPTO Open Data
      Portal key — the only one of the four blocked source gates that is credential-limited rather than
      structurally dead.
- [ ] Stop work on the per-case gain model. Logged explicitly so it is not silently resumed: the gap
      starts at r ≈ 0 and better learners do not close it.
- [ ] Second information block, qualitatively different from the first — the single largest threat to
      EXP-005's generality, since the whole diagnosis rests on one block and one cohort.
- [ ] **Bookkeeping repair, logged not tidied away.** Two experiments were both numbered EXP-005
      (`exp005_why_voi_fails.py` and `exp005_entity_resolution.py`) and both wrote the same
      `experiments/EXP-005/results.json`; whichever ran second destroyed the other's artefact, and the
      VoI one survived. Fixed 2026-07-29: entity resolution now writes `experiments/EXP-005-ER/` and has
      been re-run to restore its results; the VoI folder keeps its number because this file and the P1
      working paper cite it by path. **Consequence to check:** any earlier reading of
      `EXP-005/results.json` for entity-resolution numbers was reading the wrong file. EXP-006 also had
      `results.json` with no REPORT.md — written up 2026-07-29 (`experiments/EXP-006/REPORT.md`): string
      matching ceilings at **80.8%** balanced accuracy, the best-of-seven does not beat the best single
      matcher, hard positives collapse to 0–11%, and state/entity-type/industry separate the hard cases
      by +53/+38/+26 points. Add an experiment-numbering check to the protocol so a collision cannot
      recur silently.
