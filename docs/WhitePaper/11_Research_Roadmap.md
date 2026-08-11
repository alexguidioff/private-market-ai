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
   *given what was knowable*? Anchored to the *Management Science* (2025, Dong, Saar-Tsechansky & Geva) expert-decision-quality
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

- **A 4-year PhD** would realistically deliver **Papers #1–#3** (value of information → decision
  quality → human-AI committee), a coherent, examinable thesis. #4–#5 are the post-PhD continuation.
- **The full arc** is the decade-scale programme — the thing that turns a thesis into a
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
- **Value of information** — does the system identify the right next datum to acquire (§11.1, P1)?

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

### 11.4.1 Why the Simulator is the systemic risk (not the data)

The Simulator underpins Papers #1, #2 and #5. This concentration is a feature (one asset de-risks
three papers) but also the programme's single largest technical risk: **if the Simulator is not
credible as an evaluation environment, half the arc weakens at once.** The availability of
point-in-time data is a problem of *effort*; the credibility of the Simulator is a problem of
*validity*. It is therefore treated as the first deliverable to be validated, before #2/#5 are built
on top of it.

### 11.4.2 Two things are validated — keep them separate

A reviewer will immediately separate these; so must we.

1. **Decisions *inside* the Simulator** — "given this world, did the policy decide well?" This is
   free: because we control the data-generating process, the optimal decision is computable by
   construction. No external anchor needed.
2. **The Simulator *itself*** — "is this synthetic world realistic enough to be believed?" This is
   the hard problem and the one that needs *external* theory and evidence. §11.4.3 addresses it.

### 11.4.3 Validation by triangulation (no single criterion)

No single test establishes external validity; a synthetic environment "passes" only when several
independent criteria agree. We adopt the standard agent-based-modelling validation hierarchy and add
an outcome check, deliberately triangulated:

| Criterion | What it establishes | Strength | Failure mode if used alone |
|---|---|---|---|
| **Face validity** — domain experts (HSG advisors, interviewed VCs) inspect behaviour | behavioural plausibility | weak | subjective |
| **Stylized-facts matching** — reproduces known VC regularities *not imposed by hand* (power-law of returns; stage-wise failure rates; syndication→survival effect; hot/cold funding cycles) | structural realism | **strong** | can match means while missing the tails |
| **Point-in-time calibration** — base rates (round sizes, failure hazards) fit to open PiT data, checked out-of-sample | parameter realism | medium | overfit to the calibration sample |
| **Outcome correlation** — policies the Simulator rewards correlate with better *real* outcomes, **aggregated across many cohorts/vintages** | predictive realism | medium | **outcome bias + macro shocks** (see below) |
| **Robustness / ablation** — results stable as world parameters vary | non-fragility | strong | expensive |

The **syndication→survival effect** is a particularly strong anchor: it is the central empirical
finding of the WI2026 paper (Paper #0). A Simulator that reproduces a result we have *already
established on real data*, without being tuned to do so, earns external credibility cheaply.

The concrete list of stylized facts, operational tests, tolerances, and the **Year-1 exit-criteria
gate** (full-pass / partial-pass / fail decision rule) is specified in
`Research_Infrastructure.md §2.1`. The two WI2026-anchored facts (syndication→survival; information
saturation) are the cheapest and most convincing early checks and are run first.

### 11.4.4 Outcome is one signal, not the judge

The final outcome (exit / failure) is a tempting single yardstick, but it is a **noisy and
confounded** one: a good decision can be punished by an exogenous shock (COVID, the 2022 rate
repricing) that has nothing to do with what was knowable at decision time. Relying on outcome alone
would penalise sound decisions hit by bad luck — precisely the **outcome bias** that Paper #2
(decision quality, anchored to *Management Science* 2025, Dong, Saar-Tsechansky & Geva) exists to avoid. Outcome therefore enters
validation only (a) **aggregated across cohorts** so idiosyncratic macro shocks average out,
(b) **conditioned on the macro regime**, and (c) **alongside** the other criteria — never as the
sole arbiter.

### 11.4.5 Breaking the circularity — separation of roles

The deepest risk is circularity: if the same hand that *builds* the world also "discovers" what
matters in it, nothing has been discovered. The defence is a strict **separation of three roles that
do not share information**, designed in from the start:

1. **The data-generating process (DGP)** defines the hidden rules — which factors drive success, how
   much noise, which macro shocks. These rules stay *hidden* from everything downstream (the sealed
   "answer key").
2. **The tested policy** (our VoI / decision method) sees only what a real investor would see: the
   information state at time *t*. It has **no access to the DGP** and must *discover* what matters by
   observation. If it finds that (say) team quality is worth acquiring, that is a result precisely
   because we never told it so.
3. **The validator** is *external*: it does not ask the Simulator whether it is realistic (that would
   be self-referential) — it asks the *real world*, via published stylized facts and open outcome
   data, which are not under our control when the world is designed.

This is why "many signals, not one" is not mere prudence but the mechanism that breaks circularity:
the validation criteria are independent of, and external to, the world's designer, so the Simulator
must satisfy constraints it did not manufacture — like an exam graded by someone else.

### 11.4.6 Validating the *method* — the multi-world recovery study

§11.4.3–11.4.5 validate the *Simulator*. A separate question is whether the *method* works: does our
VoI / decision procedure actually recover truth, or is it just re-reading assumptions we baked in?
The answer is a **multi-world recovery study**, and it is what makes the circularity defence concrete.

**Protocol.**
1. Generate **thousands of worlds**, each with hidden parameters drawn at random (world A: team 0.4 /
   market 0.3 / traction 0.3; world B: team 0.1 / market 0.7 / traction 0.2; …). We never commit to a
   single "true" weighting — we sweep the space of possible worlds.
2. In each world the method sees only what an investor would see (the point-in-time information state)
   and must *infer* structure and *choose* which information to acquire. It has **no access** to the
   hidden parameters (separation of roles, §11.4.5).
3. Score across worlds.

**What to score — and what NOT to.** Do **not** average the recovered weights: with symmetric random
draws the mean is trivial (≈ uniform) for both true and estimated weights, so a useless method that
always outputs "everything matters equally" would pass. The discriminating metric is the
**per-world correlation between true and estimated importance**: when a world makes team decisive the
method must find team decisive, and when it makes team irrelevant the method must say so. The method
must *track* truth across worlds — a test that is hard to pass by chance.

**Two levels, not one.** Recovering weights is only the *sanity check* (Level 1) — and weight
recovery is a prediction problem, which is deliberately not the thesis. The test that carries the
contribution is **Level 2 — VoI ranking**: in each world, because we know the true parameters, we
also know which information was *objectively most worth acquiring net of its cost*; we check whether
the method chooses it. The distinction matters: a signal can carry high weight yet be a waste to buy
because it is expensive or already known. **Level 3 — robustness**: sweeping across many world types
(different structures, noise levels, macro regimes) exposes a method that only works in one kind of
market — the same "many worlds, not one" medicine applied to the method rather than to outcomes.

| Level | Question | Metric | Role |
|---|---|---|---|
| 1 — Recovery | Does the method grasp the world's structure? | per-world corr(true, estimated importance) | sanity check |
| 2 — VoI ranking | Does it acquire the right information *given cost*? | agreement with the cost-aware optimal acquisition | **the thesis** |
| 3 — Robustness | Does it hold across world types / regimes? | stability of 1–2 under parameter sweeps | non-fragility |

Together, §11.4.3–11.4.5 (is the world believable?) and §11.4.6 (does the method recover truth in it?)
are the full answer to the reviewer's sharpest question: *"how do you know your method works and is
not just re-reading your own assumptions?"*

### 11.4.7 Cost is the point — judging with regret, not information gathered

Without cost the problem is trivial: acquire everything, always. It is the **cost of information**
that creates the trade-off and hence the research question. With cost, "did it decide well?" becomes
two-sided — the method can fail by **over-acquiring** (buying an expensive signal that barely moves
the decision) or **under-acquiring** (skipping a cheap signal that would have flipped it). The right
yardstick is therefore not "how much did it learn" but **regret**:

```
regret = value(optimal decision, full information)
       − value(decision the method actually took)
       − cost(information the method chose to acquire)
```

The ideal method minimises regret: it acquires information only while expected benefit exceeds cost,
then **stops**. This "when to stop acquiring" is exactly the ODI group's bias–variance–*cost* tradeoff
(NeurIPS 2021) transported from estimation to *decision* — the natural methodological bridge to a
methods advisor.

### 11.4.8 Where the costs come from — abstract first, market-proxy second

Costs are hidden parameters of the world, and (like the weights) they are set in two phases:

1. **Phase 1 — abstract, controlled costs.** Not realistic, deliberately: costs are known numbers we
   *sweep* on purpose. Doubling a signal's cost must make the method acquire it less — a sanity check
   that the method actually reasons about cost, not just about information.
2. **Phase 2 — market-proxy costs.** Cost in VC diligence is mostly **time, access and effort**, not
   cash. Crucially, the point-in-time dataset already implies a natural cost hierarchy: information
   that is public and timestamped (a patent filing, GitHub activity, a Form D) costs ≈ 0; information
   requiring private access (revenue metrics under NDA, reference calls) costs more. Proxies are
   anchored to *external* evidence — reported diligence timelines in the literature and VC interviews
   (a concrete role for the HSG domain co-advisor, who has access to practitioners).

| Information | Realistic cost proxy | Proxy source |
|---|---|---|
| Revenue / traction metrics | high (internal access, NDA, time) | VC interviews; documented DD time |
| Team reference call | medium (time, network) | standard diligence practice |
| Market / sector data | low (purchasable reports) | sector-report pricing |
| Public signals (patents, GitHub, news) | ~zero (already in the PiT dataset) | API / scraping cost |

**Cost sensitivity analysis** is mandatory: show conclusions hold across a *range* of plausible
costs, not just the chosen numbers — the same "many worlds, not one" discipline applied to costs, so
"why does this signal cost 3 and not 6?" is pre-empted by "the behaviour is stable across the range".

This means the Simulator carries **three independent hidden truths** the method must cope with without
seeing: the **weights** (what matters — varies across worlds), the **costs** (what it takes to know —
abstract then market-proxied, with sensitivity), and the **luck** (noise / macro shocks — varies
across runs of the same world). The method is judged on regret: not "did it know more" but "did it
spend well to know".

**Worked example (one deal, one world).** World: team-weight 0.5 (dominant), market 0.3, traction 0.2.
Startup "Acme": team 8, market 4, traction 3 (truly a good deal). Acquirable signals: team reference
(cost 5), market report (cost 3), revenue DD (cost 4). Decision payoff: invest in a good deal +10, in
a bad deal −10, pass 0. Net value = decision payoff − acquisition cost.

| Method | Action | Payoff | Cost | Net value |
|---|---|---|---|---|
| A — buy nothing | passes (guesses wrong) | 0 | 0 | **0** |
| B — buy everything | invests (correct) | +10 | 12 | **−2** |
| C — buy only team signal | invests (correct) | +10 | 5 | **+5** |

Best achievable net value is +5 (C). So regret(A) = 5 (under-acquired → missed the deal),
regret(B) = 7 (over-acquired → paid too much to be right), regret(C) = 0 (bought *only* the signal
that mattered in this world). A method that always buys the same signal regardless of world scores
low regret only by luck in some worlds; the method that *tracks the world* scores low regret
everywhere — which is exactly what the multi-world plot (§11.4.6) measures.

## 11.5 Dependencies

```
Paper #0 (done)
   → Paper #1 (value of information)                    ── needs: point-in-time dataset + PiT/FIBO representation (Ch.5, Ch.7) + Simulator + BOED/EIG/EDDI methods
        → Paper #2 (decision quality)                   ── needs: #1 (bitemporal/PiT) + Simulator
             → Paper #3 (human-AI committee)            ── needs: Decision Graph + subjects/partner (risk)
                  → Paper #4 (gaming-robustness)        ── continuation
                  → Paper #5 (portfolio-level VoI)      ── continuation
Simulator ── built during Y1–Y2; de-risks #1/#2 (ground truth without private data)
Benchmark (beyond VCBench) ── secondary; grows on top of #1; not a headline
Integrating framework ── needs most of the above
```

Note the enabling asset is **Paper #1's point-in-time dataset**: everything downstream reuses it.
The Simulator removes the private-data dependency for #1/#2 (see `Research_Agenda.md §2` on feasibility).

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
- Which paper is the right *third* after P1→P2 — P3 (human-AI) or bringing P5 (portfolio VoI) forward? (see `STATUS_MEMO.md`)
- Can PrivateBench v0 be built on public data alone and still be credible? *(validation strategy: §11.4.3 triangulation)*
- What is the minimal Simulator that produces useful decision-quality labels? *(design constraint: §11.4.5 separation of roles — the minimal Simulator is the one whose DGP is rich enough to reproduce the §11.4.3 stylized facts, no more)*

## To do for this chapter
- [ ] Define PrivateBench v0 tasks/metrics precisely (with `Research_Infrastructure.md`).
- [ ] Map each paper to a concrete target venue + rough timeline.
- [ ] Add Figure F11: paper × asset dependency graph (see `99_Figures.md`).
