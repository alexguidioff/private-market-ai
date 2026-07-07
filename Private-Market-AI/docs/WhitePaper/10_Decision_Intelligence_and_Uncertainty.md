# Chapter 10 — Decision Intelligence & Uncertainty

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Theory.md`, `Startup_Ideas.md §0`
**Level:** 🧭 NORTH STAR — the theoretical heart of the programme.

---

## Abstract

This is the chapter the rest of the document serves. Representation (Chapters 4–8) and agentic
systems (Chapter 9) exist to support *decisions*, and decisions under extreme uncertainty are the
Grand Challenge (Chapter 3). Here the programme states its theory: precise constructs for what a
decision is, why a good decision differs from a good outcome, what uncertainty and signals are, and
why causality matters more than correlation. From these follows the programme's signature output —
not a point estimate but a **decision object** with a distribution, confidence, reasons, missing
information, and the value of acquiring it — and its signature stance: AI that augments human
decision-making rather than replacing it.

---

## 10.1 Why a theory, not just models

Most labs build algorithms; this one aims to build a theory that survives the churn of methods
(Chapter 1). A field matures when it has shared *constructs*, not just tools — medicine has disease
models, economics has utility and equilibrium. Investing under uncertainty has spreadsheets and
folklore. Defining the constructs precisely enough to be measured and taught is the difference
between *applying AI to finance* and *contributing to a science of decision-making*.

## 10.2 What is a decision (and what is a good one)

A **decision** is a commitment of resources under uncertainty, chosen among alternatives, justified
by information, producing an outcome. It is richer than a prediction: it has alternatives, a
rationale, reversibility, and a cost of being wrong — which is exactly what the Decision Graph
(Chapter 6) records.

The crucial distinction: **a good decision is not the same as a good outcome.** In high-variance
domains like venture capital, sound reasoning can yield bad outcomes and luck can rescue poor
reasoning. A science of investment decisions must therefore be able to evaluate **process quality**
— was the reasoning sound given what was knowable at the time? — and not only realised returns.
This is why the bitemporal knowledge graph (Chapter 5) and the Decision Graph (Chapter 6) matter:
together they reconstruct *what was knowable when*, making process quality assessable.

## 10.3 Two kinds of uncertainty

The programme is, deliberately, obsessed with uncertainty, and distinguishes:
- **Aleatoric** — irreducible randomness; the world is noisy and the future is genuinely open.
- **Epistemic** — reducible by more information; we simply do not know yet.

Much of the value of due diligence is the *conversion of epistemic uncertainty into knowledge* —
and, critically, knowing when that conversion is worth its cost. This reframes diligence from
"gather everything" to "acquire the information with the highest value" (§10.6).

## 10.4 What is a signal, and how do signals combine

A **signal** is information that shifts belief about a latent quality (team, market, product).
Signals have strength, cost, timeliness, correlation with other signals, and **gameability**.
The hard modelling question — largely unaddressed in the prediction literature of Chapter 2 — is how
they *combine*. Naïve addition is wrong: signals are correlated, redundant, and sometimes
contradictory. The founding paper's finding is instructive here: adding financial signals to
non-financial ones produced *no* improvement ("information saturation") `[guidi2026wi]` — a concrete
instance of signals carrying overlapping rather than additive information. A theory of signal
combination connects to information theory and Bayesian updating.

## 10.5 Prediction → causality

The founding paper is predictive: *which signals predict valuation?* The deeper question is causal:
*which signals **cause** good outcomes?* The distinction is practical, not academic:
- Predictive proxies degrade under distribution shift (why the paper insisted on an out-of-time
  holdout) and are gamed once known (§10.4).
- Causal understanding supports **intervention** ("if this company hired senior sales, would
  outcomes improve?") and **policy** ("what should a fund do?").
This opens the programme to causal inference and counterfactual reasoning, and connects to work
already combining prediction with causal discovery in startup valuation `[garkavenko2023]`.

## 10.6 Uncertainty as a first-class output

The programme's signature output is never a number. It is a **decision object**:

```
output = {
  distribution:          P10 / P50 / P90         (not a point)
  confidence:            how sure, and why
  reasons:               which signals drove it   (interpretability, Ch.8)
  missing_information:   what we don't know
  value_of_information:  what it's worth to find out
}
```

This is both better science and a better product (`Startup_Ideas.md §0`): even the paper's strong
non-financial model (R² ≈ 0.56 out-of-sample) leaves real residual uncertainty, and an honest
system reports the range and the reasons rather than a single confident figure.

### 10.6.1 Value of information — the programme's most distinctive contribution
Of all the ideas here, **value of information (VoI)** is the one the prior-art scan flagged as
genuinely open. The distinction matters:
- *Uncertainty intervals alone* are no longer novel — conformal prediction already produces
  calibrated valuation intervals, including for automated valuation models. Adding intervals to
  startup valuation would be incremental.
- *Value of information* asks a different, under-explored question: **given the current decision and
  its uncertainty, which missing datum — at what cost — would most improve the decision?** It turns
  a passive disclaimer ("we're unsure") into an active recommendation ("go find the churn data
  before the enterprise-pipeline data").

Crucially, the *methods* already exist and are battle-tested elsewhere — Bayesian optimal
experimental design, expected information gain, and active feature acquisition (e.g. EDDI-style
"cost reduction at equal decision quality" in healthcare). **The contribution is porting them to VC
due diligence**, where the scan found only practitioner checklists and no formal treatment. This is
what directs the diligence agents of Chapter 9, and is the research behind the Due Diligence Copilot
(`Startup_Ideas.md`). It is **Paper P1 (flagship)** in the revised sequence (`Research_Agenda.md`).

## 10.7 Human-AI decision-making

The future the programme argues for is not "AI that invests" but **AI that participates** in the
decision (Chapters 1, 9). Research questions:
- How does AI participation change the *decision* (not merely the information available)?
- When do humans trust the AI, and when do they override it — rightly or wrongly?
- How to design AI contributions that improve process quality without inducing anchoring or
  automation bias?
The Decision Graph (Chapter 6) records who decided and on what basis, making these questions
empirical rather than speculative.

## 10.8 The epistemological question (kept open)

> **Can an AI make investment decisions — or only support them?**

This is not rhetorical. It determines product boundaries, liability, governance, and how much
authority a system should be given. The programme takes a working stance — *support, with the human
accountable* — while treating the question as genuinely open and revisitable as capabilities grow.

## 10.9 How the theory integrates the programme

Decision Intelligence is the integrating layer named in the roadmap (Chapter 12): representation
(Ch. 4–8) supplies *what is known*; agentic systems (Ch. 9) supply *action*; this chapter supplies
the *theory of the decision* that gives both a purpose. The loop — represent → reason → decide →
observe → learn — is closed by evaluating decisions (process quality, §10.2) and feeding the result
back, which is what PrivateBench and the Simulator (Chapter 11) are built to enable.

---

## Open questions carried forward
- A formal, learnable definition of "decision quality" where only outcomes are observed.
- A tractable representation of *value of information* in a live deal.
- Whether process quality can be improved measurably by AI participation (Chapter 9).

> **Figure F10** (`figures/figures.md#f10`): the decision object — distribution, confidence, reasons,
> missing information, and value of information directing the next diligence step.

> **Citations now available** (`98_References.md §G`): decision under uncertainty
> `[savage1954]`, `[tversky1974]`, `[kahneman1979prospect]`; causality `[pearl2009causality]`;
> value of information `[voi-howard]` (exact ref TBC).

## To do for this chapter
- [x] Decision-science / causality citations added (Pearl, Savage, Tversky-Kahneman).
- [ ] Finalise value-of-information (Howard 1966) + a calibration reference.
- [x] Figure F10 drafted (`figures/figures.md`).
- [ ] Formalise "decision quality" as a candidate PrivateBench metric (Chapter 11).
