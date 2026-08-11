# Chapter 1 — Vision & Philosophy

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Vision.md` (§0.0, §3, §3.1.1), `Theory.md`
**Level:** 🧭 NORTH STAR

---

## Abstract

Public capital markets are served by a mature information infrastructure — Bloomberg, Refinitiv,
FactSet — built on a shared, machine-readable representation of instruments, prices, and events.
Private capital markets have no equivalent. Decisions worth trillions of dollars are made on
scarce, heterogeneous, and deeply uncertain information, using tools (spreadsheets, ad-hoc
databases, tacit judgment) that do not represent the domain in a way machines can reason over.
This chapter sets out the mission of the programme — *to build the scientific foundations of
Decision Intelligence for Private Capital Markets* — and the research philosophy that
distinguishes it from the many efforts now applying AI to venture capital. The central claim is
that the durable problem is not *predicting* investment outcomes but *representing* the domain and
*augmenting* the human decisions made within it, under uncertainty.

---

## 1.1 The opening thesis

An investment in a private company is not a number; it is a commitment made under extreme
uncertainty, on the basis of fragmentary evidence, about a system that is changing while the
decision is being made. Yet the tools available to investors treat this either as a data-retrieval
problem (databases that store facts) or as a prediction problem (models that output a valuation or
a score). Both miss the substance of the work. A venture capital fund does not make one decision
per investment; it makes hundreds — what to look at, whom to trust, what to believe, what to
verify, what to offer, when to follow on, when to exit — each under a different mix of irreducible
and reducible uncertainty.

The premise of this programme is that these decisions rest on a missing layer: an explicit,
machine-reasoning-ready **representation** of private companies and their ecosystem. Without it,
every downstream capability — ranking, valuation, due diligence, portfolio monitoring, investment
committee support — is built on sand. With it, they become special cases of a single, coherent
system.

## 1.2 Mission and sub-theme

> **Mission.** We build the scientific foundations of **Decision Intelligence for Private Capital
> Markets**.
>
> **Sub-theme.** Understand, represent, and augment human decision-making under uncertainty.

The mission is deliberately two-sided. "Decision Intelligence" names the ambition — a discipline,
not a feature. "Private Capital Markets" names the domain that keeps the work honest: real data,
real operators, real decisions with consequences. Ambition without a domain drifts into
abstraction; a domain without ambition produces yet another point tool. The programme lives at
their intersection.

## 1.3 The Grand Challenge

Beneath the mission sits a question that outlives any particular technology — including today's
large language models:

> **How do investors make decisions under extreme uncertainty, and how can AI represent, augment,
> and improve that process?**

Framed this way, venture capital is the **initial domain, not the whole subject**. The same
science extends naturally to mergers and acquisitions, corporate development, drug-discovery
investing, sovereign wealth funds, infrastructure, and climate investing — settings that share
the same deep structure: high stakes, thin data, long feedback loops, and consequential human
judgment. This is what makes the question lab-scale rather than product-scale, and what allows a
single research agenda to remain relevant for a decade or more.

## 1.4 Research philosophy: five commitments

Most laboratories build *algorithms*. This one aims to build a *theory* and the infrastructure to
test it, so that the work survives the churn of methods. Five commitments distinguish the
approach.

1. **Theory over algorithms.** The programme develops an *Investment Intelligence Theory*
   (Chapter 10): precise constructs for what a decision is, what a good decision is, what a signal
   is, and how signals combine. A theory of the domain remains valid when the model of the month
   is replaced.

2. **Uncertainty over point estimates.** The unit of output is never "valuation = 18M." It is a
   decision object: a distribution (P10 / P50 / P90), a confidence, the reasons behind it, the
   information that is missing, and the value of acquiring that information. Honesty about what is
   not known is treated as a feature, not a weakness — a direct lesson from the founding paper,
   whose best model leaves roughly half the variance unexplained.

3. **Causality over correlation.** The aim is to understand which signals *cause* good outcomes,
   not merely which *predict* them. Predictive proxies degrade under distribution shift and are
   gamed once known; causal understanding supports intervention and policy.

4. **Human-AI collaboration over automation.** The goal is not an AI that invests, but an AI that
   *participates* in the investment process — screening, diligence, and committee reasoning —
   while human judgment remains central. The research questions are as much about trust,
   overrides, and process quality as about model accuracy.

5. **Benchmarks and simulation over anecdotes.** The field lacks shared evaluation. The programme
   proposes a benchmark (PrivateBench) and a virtual-fund simulator (Chapter 11) so that claims
   can be measured and compared rather than asserted.

## 1.5 Why private markets are the non-negotiable wedge

It would be tempting to describe this as a "decision-science lab" and let the domain float. That
would be a mistake. Credibility, data access, and the ability to tell good work from bad all come
from being concrete. Private markets provide a real dataset (the founding paper uses 3,403
PitchBook deals), real operators whose language and workflow can be learned, and a real, accepted
publication as a starting point. The wedge is not a limitation on the ambition; it is what makes
the ambition fundable and testable.

## 1.6 Positioning: defining a discipline, not applying a tool

The reframing that organises the whole programme can be stated as a shift in four moves:

| From | To |
|---|---|
| A startup-valuation product | Decision Intelligence for Private Capital Markets |
| A model | A theory *and* an infrastructure |
| One prediction | Hundreds of decisions per investment |
| Prediction | Decision-making under uncertainty |

The consequence is an ordering principle that recurs throughout this document: **representation
precedes reasoning, and reasoning precedes decision**. Valuation, the subject of the first paper,
is not the destination but the first use case — the point of entry into a much larger and more
durable problem.

---

## Open questions carried into later chapters
- What is a minimal, adoptable definition of "decision quality" usable as an evaluation target?
  (Chapter 10)
- Which decisions in the VC/PE workflow have the best effort/impact ratio for AI? (Chapters 9, 13)
- How far does the private-markets framing generalise before the theory needs revision? (Chapter 3)

> **Figure F1** (`figures/figures.md#f1`): valuation → representation → reasoning → decision
> intelligence, with the learning feedback loop.

## To do for this chapter
- [x] Figure F1 drafted (`figures/figures.md`).
- [ ] Insert verified anchor citations (now available in `98_References.md`):
      §1.4 commitment 1 (interpretability) → `[lundberg2017shap]`, `[breiman2001rf]`;
      §1.1/§1.6 (representation precedent) → `[bodenreider2004umls]`, `[hogan2021kg]`;
      §1.3 (active field / AI-in-VC) → `[ssff2024]`, `[startup2023crunchbase]` (verify authors first).
- [ ] Decision-science / causality citations for §1.4 commitments 3 — still ⬜ in references (§G).
- [ ] Tighten §1.4 to ~1 paragraph per commitment for the final cut.
