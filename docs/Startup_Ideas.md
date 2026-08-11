# Startup Ideas & Commercialization

**Author:** Alessandro Guidi — v0.2
**Level:** 🧭 **[NORTH STAR — private]** — commercialization comes *after* research foundations.
**Current boundary:** the implemented MVP is the P1 research/evidence MVP, not a fundraising-ready
product; see `PROJECT_DIRECTION.md` for gates from research to buyer validation and possible spin-off.

> Product comes *after* research foundations. Valuation is a feature, not the product.
> Positioning: **Decision Intelligence for Private Capital Markets** (wedge: AI for VC).

---

## 0. The differentiator: uncertainty, not point estimates

Every competitor outputs a number. The product's wedge is an **honest decision object**:

```
This round: fair-value range P10 €12M · P50 €17M · P90 €24M
Confidence: medium
Why: strong founder signal, weak traction evidence, hot sector
Missing: revenue detail, churn, cohort data
Worth finding out: churn (high value-of-information) → ask for it in DD
```

This reflects the lab's obsession with uncertainty (see `Theory.md`): even a strong model
(the paper's best non-financial ML reaches R² ≈ 0.56 out-of-sample) leaves real residual
uncertainty, and investors trust ranges-with-reasons far more than a single confident number.
It is *better science and better product*.

---

## 1. Product evolution

```
V1  Valuation Assistant  (uncertainty-first)
      "Fair value P10–P90 = 12–24M. This round looks +35% above P50."
      "Here's what we don't know, and what it's worth finding out."
   ↓
V2  Due Diligence Copilot
      Upload deck → AI reads it → estimates traction → analyzes team →
      compares to 2000+ deals → drafts investment memo → generates DD questions.
   ↓
V3  Investment Copilot
      Sourcing + screening + valuation + DD + IC support in one workflow.
   ↓
V4  Private Market Operating System
      The decision-intelligence platform — "Bloomberg for private markets".
```

---

## 2. Where AI creates value (VC workflow)

| Process | Human time | AI today | Opportunity |
|---|---|---|---|
| Sourcing | High | Medium | ⭐⭐⭐⭐⭐ |
| Screening | High | High | ⭐⭐⭐⭐⭐ |
| Partner review | High | Almost none | ⭐⭐⭐⭐⭐ |
| Due diligence | Enormous | Medium | ⭐⭐⭐⭐ |
| Investment committee | Enormous | Almost none | ⭐⭐⭐⭐⭐ |
| Portfolio monitoring | High | Medium | ⭐⭐⭐⭐⭐ |
| Exit | Medium | Low | ⭐⭐⭐ |

Highest effort/impact: **screening**, **partner review**, **investment committee** (nobody is
really doing IC support yet).

---

## 3. Moats to build
1. **Proprietary data** — beyond PitchBook: user feedback, uploaded docs, cap tables, SaaS metrics.
2. **Workflow** — sell a *process*, not a model.
3. **Network effects** — every fund using it improves the model.
4. **Verticalization** — own the "AI for VC" category.

---

## 4. Why Switzerland
Many VCs, family offices, private banks, PE funds, wealth managers; strong willingness to pay
for B2B tools; high-ticket clients (UBS, Julius Baer, Pictet, Lombard Odier entering private
markets).

---

## 5. Customer segments
- VC / Growth funds (internal deal tooling).
- Family offices.
- Private banks / wealth managers (pricing, risk scoring, portfolio monitoring — possibly as API).
- Corporate VC.

---

## 6. Competitive landscape (watch list)
PitchBook · Crunchbase · Dealroom · CB Insights · Carta · AngelList · Harmonic ·
AI-DD startups (ToltIQ, Xapien, ...). Everyone builds pieces; the opportunity is the
**integrated system + representation layer**.

---

## 7. Open questions
- Wedge product: which single decision to win first?
- Build vs. partner for data access?
- Regulatory constraints for private-bank customers?


## 8. Commercial activation rule

The commercial path can be activated if the PhD/research-collaboration route does not materialise,
but an academic rejection is not evidence of product demand. Follow the staged gates in
`PROJECT_DIRECTION.md`:

1. run 10 buyer interviews alongside the 20-issuer gold-label pilot;
2. require repeated evidence of one narrow workflow problem;
3. use static mockups before building production software;
4. start a partially manual concierge prototype only with 1–2 prospective design partners;
5. process 5–10 real cases and measure accepted recommendations, time saved and provenance errors;
6. build a standalone commercial application only after these gates; separate customer documents,
   authentication and proprietary feedback from the reproducible research repository;
7. consider bootstrap, grant/accelerator or pre-seed only after continued use, a paid pilot or a
   credible letter of intent.

Initial wedge: **evidence-gap assistant**, not automated investment advice and not a general
private-market operating system. The product can use P1's information-state, provenance and
decision-record components immediately.

> ⚠️ **"Next-best-diligence" removed from the wedge, 2026-07-29.** The earlier wording said the learned
> VoI policy "enters only after real validation", which was correctly hedged. The hedge is no longer
> enough, because the validation has now been attempted and failed in a specific way that bears on the
> product rather than only on the paper.
>
> Per-case targeting — telling a user *which case* to diligence next — requires the **direction** of a
> decision change to be predictable, and it is not. On real data the correlation between predicted and
> realised per-case gain is +0.015 / −0.070 / +0.000 across three utility assumptions, and an oracle
> that uses the outcome beats every fixed baseline by +0.065 to +0.087, so a winning policy exists and
> no implementable selector finds it. Predicting *whether* a decision changes reaches ROC-AUC 0.950 and
> still converts into nothing, because helpful and harmful changes scale together. A synthetic sweep
> across 30 declared tests found no region where a selective policy wins. See paper §8.6 and
> `experiments/EXP-005`, `EXP-009`, `EXP-010`.
>
> **What survives as sellable, and it is narrower than the original wedge:**
> 1. **Evidence gap and provenance** — "here is what is not known, here is where each fact came from,
>    here is what was knowable at the decision date." This is the point-in-time information-state
>    infrastructure, not a VoI policy, and nothing above touches it.
> 2. **A cohort-level acquire / do-not-acquire recommendation under a declared utility.** The population
>    mean gain *is* estimable and changes sign with the payoff matrix (+0.028 balanced, −0.008
>    false-positive-averse), so the honest product statement is "for a fund with your loss preferences,
>    this source is or is not worth buying" — a procurement recommendation, not a per-deal ranking.
> 3. **P5's budgeted allocation across a pipeline**, which never required per-case gain. But EXP-009
>    showed the slice-restricted estimate is unmeasurable at this cohort size — the median divergence of
>    an arbitrary top-5% slice equals the whole quantity — so this needs a materially larger cohort
>    before it is a product claim rather than a research question.
>
> **Do not ship or pitch a "what to diligence next" ranker on this evidence.** Recording that here so
> the falsified capability is not quietly reintroduced through a product roadmap.