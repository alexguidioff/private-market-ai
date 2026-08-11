# Chapter 3 — Grand Challenge & Research Questions

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Vision.md §0.0, §8`, `Theory.md`,
`papers/notes/WI2026_paper_summary.md`
**Level:** 🧭 NORTH STAR

---

## Abstract

Chapter 1 set the mission; Chapter 2 established the gap. This chapter states the decade-scale
question the programme is organised around, explains why venture capital is the *entry domain*
rather than the whole subject, and derives the concrete research questions that structure the rest
of the document. It also traces the line from the three narrow, answerable questions of the
founding paper to the broad, durable questions of the programme — showing that the agenda is a
principled expansion of a result already in hand, not a leap of faith.

---

## 3.1 The Grand Challenge

> **How do investors make decisions under extreme uncertainty — and how can AI represent,
> augment, and improve that process?**

Three properties make this a lab-scale question rather than a product specification.

- **It is durable.** It does not depend on the model of the moment. Large language models,
  gradient-boosted trees, and knowledge graphs are all *means*; the question is about decisions,
  signals, and uncertainty, which persist as the methods change.
- **It is deep.** "A good decision" is not "a good outcome" (Chapter 10). Uncertainty is not one
  thing but two — reducible and irreducible. Signals interact, are costly, and are gameable. These
  are genuine scientific problems, not engineering details.
- **It is general.** Venture capital is the first instance of a family of settings that share the
  same structure: high stakes, thin data, long feedback loops, and consequential human judgment.

## 3.2 Why venture capital is the entry domain, not the whole subject

The same science extends, with changes of vocabulary rather than substance, to mergers and
acquisitions, corporate development, drug-discovery investing, sovereign wealth, infrastructure,
and climate investing. Each is a decision under extreme uncertainty about a complex, evolving
entity, made on fragmentary and heterogeneous evidence.

Venture capital is chosen first for three reasons: it is where the founding result already exists
`[guidi2026wi]`; it has rich (if partly proprietary) data; and its operators are reachable, so the
work can be validated against practice. The generalisation is a *claim to be tested* in later
years, not an assumption — but framing the domain as an instance rather than the totality is what
keeps the research agenda from ageing into a single-application project.

**The wedge remains non-negotiable (Chapter 1).** Breadth of ambition is disciplined by depth in
one domain. The programme is not "a decision-science lab that happens to look at VC"; it is a
private-markets programme whose results are designed to generalise.

## 3.3 From the paper's questions to the programme's questions

The founding paper asked three narrow, answerable questions and answered them:

- **RQ1 (paper):** Do ML models trained only on non-financial signals match traditional financial
  baselines under market stress? → *Yes; and they generalise more robustly across regimes.*
- **RQ2 (paper):** Which features drive algorithmic pricing? → *Investor-syndicate capacity, via SHAP.*
- **RQ3 (paper):** Does adding financial data help? → *Negligibly ("information saturation").*

Each answer opens a broader question the programme must address:

| Paper question | Answer | Programme question it opens |
|---|---|---|
| RQ1 — non-financial signals suffice | yes, more robustly | **How should those signals be *represented*** so any task can use them? (Ch. 4–6) |
| RQ2 — syndicate is the driver | yes (SHAP) | **What is the causal role of network/structure**, not just its predictive weight? (Ch. 10) |
| RQ3 — financials add little | information saturation | **What information *does* reduce uncertainty**, and what is it worth to acquire? (Ch. 10) |

This is the intellectual hinge of the programme: a concrete, published result about *prediction*
points directly at the deeper problems of *representation*, *causality*, and *uncertainty*.

## 3.4 Primary research questions

The programme is organised around six questions. Each is mapped to the chapters that address it.

1. **Representation.** How should private companies and their ecosystem be represented digitally —
   entities, relationships, events, signals — so that heterogeneous AI systems can reason over
   them? *(Ch. 4–6)*
2. **Signals.** Which signals matter, how stable are they across market regimes, and how do they
   combine (given that they are correlated, costly, and gameable)? *(Ch. 8, 10)*
3. **Uncertainty.** How can outputs express not a point but a distribution with confidence,
   reasons, missing information, and the value of acquiring it? *(Ch. 10)*
4. **Causality.** Which signals *cause* good outcomes rather than merely predicting them, and how
   can that support intervention and policy? *(Ch. 10)*
5. **Human-AI decisions.** Can AI *participate* in investment reasoning — screening, diligence,
   committees — improving process quality without inducing anchoring or automation bias? *(Ch. 9, 10)*
6. **Standardisation.** Can a shared, open ontology of private markets be defined and adopted, as
   UMLS/SNOMED were in medicine? *(Ch. 5)*

> **Whitespace note (5-pass prior-art scan, `papers/notes/Prior_Art_Scan.md`).** A literature check
> confirms which of these are genuinely open. **Q3 (uncertainty / value of information)** and **Q5
> (human-AI at the committee)** are the emptiest and most defensible; **Q1/Q6 (representation /
> standardisation)** are open but must be positioned against **FIBO**. By contrast, *prediction* of
> founder/startup success is crowded (VCBench, GNN & LLM papers) — so the programme treats it as a
> component, not a headline. The research agenda (`Research_Agenda.md`) therefore leads with value of
> information (with representation as its foundation), then decision quality, then human-AI.

## 3.5 Success criteria

To keep the agenda falsifiable rather than aspirational, each question carries a rough test of
"answered":

- **Representation** — a schema on which ≥3 distinct downstream tasks are built without re-engineering features.
- **Signals** — a signal set whose predictive value is stable across at least two market regimes.
- **Uncertainty** — calibrated distributional outputs (e.g. reliable P10–P90 coverage), not just point error.
- **Causality** — a causal effect **identified in the Simulator** (where structure is known by
  construction), plus an **E-value sensitivity analysis** on real data quantifying robustness to
  unobserved confounding; a natural-experiment identification on real data is upside, not a
  requirement. *(Softened from "an intervention effect estimated on real data" — see
  `Threats_to_Validity.md` #9; strong causal claims on observational VC data are not promised without
  an identification strategy, per Risk #5.)*
- **Human-AI** — a measured change in decision *process quality*, not only in model accuracy.
- **Standardisation** — adoption of the ontology by at least one external group or dataset.

---

## Open questions carried forward
- How far can the VC-derived representation travel before it needs revision for M&A / PE / SWFs?
- Is "decision quality" measurable from data where only outcomes are observed? (Ch. 10)
- Which of the six questions is the right *second* paper after representation? (see `STATUS_MEMO.md`)

## To do for this chapter
- [ ] Add Figure F3: research-questions → chapters map (see `99_Figures.md`).
- [ ] Tighten §3.5 success criteria once PrivateBench tasks/metrics are defined (Ch. 11).
- [ ] Decision-science citations for §3.1 (bullet "deep") — still ⬜ in `98_References.md §G`.
