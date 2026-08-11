# Chapter 2 — State of the Art

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Vision.md §2`, `Startup_Ideas.md §6`,
`papers/notes/WI2026_paper_summary.md`
**Level:** 🧭 NORTH STAR

---

## Abstract

This chapter surveys the landscape the programme builds on and against. It covers four strands:
(i) traditional startup and private-company valuation; (ii) machine-learning approaches to
valuation and success prediction; (iii) commercial data platforms and the recent wave of AI point
solutions for venture capital; and (iv) representation technologies — knowledge graphs and
ontologies — that are mature in other domains but largely absent from private markets. The
chapter closes on the gap that motivates the whole programme: the incumbents are *databases* and
*point predictors*, not a shared, machine-reasoning-ready *representation* of the domain.

*Citations below use keys from `98_References.md`. Entries marked ✅ are verified; those marked
🟡 are found but need author/venue confirmation before the final cut.*

---

## 2.1 Traditional valuation and its limits

Classical valuation rests on discounted cash flow (DCF) and comparables. Both transfer poorly to
startups. DCF requires long-horizon cash-flow forecasts that are incompatible with pre-revenue,
loss-making, non-linear businesses `[damodaran2009]`; comparable-company multiples — revenue
multiples for early stage, EBITDA multiples for later stage `[pratt2008]` — are fragile because
genuinely comparable peers rarely exist and because the method is highly sensitive to market
sentiment `[miloud2012]`. The consequence is systematic mispricing during exuberant markets
`[metrick2010]`, and a documented gap between headline valuations and their true economic value
once contractual terms are accounted for `[gornall2020]`. Ordinary least squares remains a common,
interpretable baseline whose transparency institutional stakeholders often demand `[molnar2022]`;
standard valuation practice is codified in `[koller2015]`. This body of work establishes both the
importance of the problem and the inadequacy of the classical toolkit under the conditions that
characterise venture investing.

## 2.2 Machine learning for valuation and success prediction

A growing literature applies ML to private-company valuation and outcomes. Work has predicted
entrepreneurial-firm valuation with ML `[zhang2023]`, applied deep learning to startup valuation
`[dhochak2024]`, and combined prediction with causal discovery to identify valuation drivers
`[garkavenko2023]`. Related strands predict *outcomes* rather than price — e.g. the likelihood of
reaching a successful Series A from Crunchbase and LinkedIn data `[te2023]` — and develop
interpretable frameworks for explaining company valuation `[blanquet2025]`. Beyond startups,
relative valuation with ML has been studied for public equities `[geertsema2023]`, and there are
textbook treatments of ML in finance generally `[dixon2020]`. Methodologically, the field relies
on tree ensembles `[breiman2001rf]`, `[chen2016xgboost]` and on post-hoc interpretability, in
particular SHAP and its tree-specific form `[lundberg2017shap]`, `[lundberg2020trees]`.

The founding paper of this programme `[guidi2026wi]` sits in this strand but sharpens the question.
Using 3,403 PitchBook deals and GEM macro data under a strict out-of-time holdout across the 2022
correction, it shows that ML trained *only on non-financial signals* prices private companies
competitively with the best financial baselines and generalises more robustly across regimes,
while adding financial and macro data yields negligible improvement — and that investor-syndicate
capacity, not firm financials, is the dominant pricing driver. This is consistent with the
long-standing finding that venture networks and investor quality carry a "certification effect"
`[hochberg2007]`.

**What is missing in this literature.** These are, almost without exception, *prediction* studies:
they estimate a number (valuation) or a probability (success), report error metrics, and — at
best — attach post-hoc explanations. None addresses the prior question of *how the underlying
entity should be represented* so that many such tasks can be supported coherently. Each paper
re-engineers features from whatever data it has; there is no shared substrate.

## 2.3 Commercial platforms and the AI point-solution wave

Industry has moved faster than academia on tooling. Data platforms — PitchBook, Crunchbase,
Dealroom, CB Insights, Orbis, Capital IQ — provide broad coverage and are increasingly layering AI
features (LLM-generated insights, predictive scores, retrieval). In parallel, a wave of startups
automates *single stages* of the investment process, notably AI-assisted due diligence
(e.g. ToltIQ, Xapien and similar). A recent research literature mirrors this, proposing LLM- and
multi-agent frameworks for startup evaluation and venture due diligence 🟡 `[ssff2024]`,
🟡 `[startup2023crunchbase]`, 🟡 `[dialectic2026]`, 🟡 `[vcdd2026]` (verify before final citation).

The pattern is telling: **everyone is building pieces; no one is building the complete system.**
Platforms optimise storage and retrieval; point solutions optimise one workflow step. Both take the
underlying representation of a company as given — usually a flat record of fields — rather than as
the object of design.

## 2.4 Representation technologies: mature elsewhere, absent here

Outside finance, the representation problem has been taken seriously. Knowledge graphs provide a
mature framework for representing entities, relationships, and events over large, heterogeneous,
dynamic data `[hogan2021kg]`. In medicine, shared vocabularies and ontologies — the UMLS
integrates millions of concept names and relations across dozens of source vocabularies
`[bodenreider2004umls]` — give machines a common, reasoning-ready model of the domain. Deep
representation learning `[vaswani2017attention]` and work on learning over populations of models
`[schurholt2022hyperrep]` show how rich, reusable representations can be learned rather than
hand-engineered.

Private markets have **no equivalent**. There is no shared ontology of what a startup, a round, an
investor, a founder, or a growth signal *is*; no temporal, multimodal knowledge graph of the
ecosystem; no agreed representation on which downstream models can be built and compared.

## 2.5 The gap that motivates this programme

Synthesising the four strands:

| Strand | What it provides | What it lacks |
|---|---|---|
| Traditional valuation | interpretable baselines, domain logic | breaks down for startups; sentiment-sensitive |
| ML valuation / success | predictive power, some interpretability | prediction-only; no shared representation |
| Platforms & AI point tools | coverage, workflow automation | databases/point solutions; representation taken as given |
| KG / ontology (other fields) | reasoning-ready representation | not applied to private markets |

The gap is not another predictor and not another database. It is the **missing representation
layer**: an explicit, temporal, multimodal, reasoning-ready model of private companies and their
ecosystem, on which valuation, ranking, due diligence, monitoring, and committee support become
special cases rather than bespoke pipelines. Defining that layer — and the theory of decision it
serves — is the subject of the chapters that follow.

---

## Open questions carried forward
- How much of the classical valuation logic (§2.1) should be *encoded* in the representation vs. *learned*?
- Can a shared benchmark (PrivateBench, Ch. 11) make the fragmented ML literature (§2.2) comparable?
- What is the private-markets analogue of UMLS/SNOMED, and who would adopt it? (Ch. 5)

## To do for this chapter
- [ ] Confirm authors/venue for 🟡 entries in §2.3 (agentic DD) before final cut.
- [ ] Add 2–3 more recent (2024–2026) AI-in-VC references from `98_References.md §E` once verified.
- [ ] Add Figure F2: provider/approach comparison (coverage × reasoning-ready).
- [ ] Consider a short §2.6 on data providers' terms/limits (ties to Ch. 7 legality).
