# Chapter 8 — Representation Learning & Foundation Models

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `Roadmap.md §3`, `Vision.md §5`, plus new material
**Level:** 🧭 NORTH STAR

---

## Abstract

Chapters 4–7 defined *what* to represent (the data model, ontology, graphs) and *from what* (the
data sources). This chapter addresses *how the representation is learned*: the progression from
hand-engineered tabular features, through graph and multimodal learning, toward pretrained
foundation models of private-market entities. The argument is that each step reduces the amount of
manual feature engineering and increases what can be shared and reused across tasks — turning the
fragmented, per-study modelling of Chapter 2 into a common learned substrate. Throughout,
interpretability and uncertainty remain requirements, not afterthoughts.

---

## 8.1 Stage 0 — Tabular baselines (the founding paper)

The starting point is the founding paper `[guidi2026wi]`: interpretable models — Random Forest
`[breiman2001rf]`, gradient boosting `[chen2016xgboost]` — over hand-engineered structured
features, with SHAP for interpretability `[lundberg2020trees]`. This stage established two things
the rest of the chapter builds on: that **non-financial, structural signals carry most of the
pricing information**, and that **the investor syndicate (a relational feature) dominates**. Both
point beyond tabular data: the most informative signal is relational, and relational structure is
poorly captured by flat feature tables.

## 8.2 Stage 1 — Graph representation learning (GNNs)

If the syndicate is the dominant signal (§8.1), the natural next step is to learn over the graph
rather than flatten it. **Graph Neural Networks** operate on the knowledge graph (Chapter 6),
propagating information along typed edges — e.g. investor quality along `INVESTED_IN` and
co-investment edges, operationalising the "certification effect" `[hochberg2007]` as a *learned*
graph feature rather than a hand-coded one. This is the technical core of Paper #3. Open problems:
temporal GNNs (the graph changes over time), and heterogeneous graphs (many node/edge types).

## 8.3 Stage 2 — Multimodal representation

Investors read decks, filings, news, and code — not just tables. Multimodal representation learning
fuses these into a single company representation: text and documents via language models (built on
the Transformer architecture `[vaswani2017attention]`), tabular financials, time-series signals
(hiring, GitHub cadence), and code/patent content. The Digital Twin (Chapter 6, §6.2) is the target
object: one coherent, updatable representation per entity that carries all modalities. This is
Paper #4 territory (multimodal startup representation).

## 8.4 Stage 3 — Foundation models for private-market entities

The longer-horizon goal is a **pretrained foundation model** of private-market entities: a model
trained (largely self-supervised) over the whole temporal, multimodal graph, producing reusable
embeddings of companies, founders, and investors that many downstream tasks can consume without
re-engineering features. The analogy is deliberate — as large pretrained models reshaped NLP after
`[vaswani2017attention]`, and as learning over *populations* of models proved fruitful in other
settings `[schurholt2022hyperrep]`, a foundation model *of companies* could become the shared
representation the field lacks. This is speculative and years out; it is stated as a direction, not
a claim.

## 8.5 Cross-cutting requirements: interpretability and uncertainty

Two constraints hold at every stage and distinguish this programme from pure predictive modelling:

- **Interpretability.** As models move from tabular (inherently interpretable) to graph/multimodal
  (opaque), interpretability must be engineered in — SHAP `[lundberg2017shap]`,
  `[lundberg2020trees]`, attention attributions, counterfactuals. Institutional investors demand it
  (Chapter 2; `[molnar2022]`).
- **Uncertainty.** Outputs remain distributional, not point estimates (Chapter 10). A more powerful
  representation that cannot say *how confident it is* is not an improvement for decision support.

## 8.6 Evaluating representations

A recurring difficulty (flagged in Chapters 3 and 11): how do you evaluate a *representation*, as
opposed to a prediction? Two complementary routes:
- **Extrinsic** — does the representation improve performance across several downstream tasks
  (valuation, next-round, survival) without task-specific feature engineering? This is the
  operational definition of "good representation" from Chapter 3, §3.5.
- **Intrinsic** — probing tasks, calibration, stability across market regimes (the out-of-time
  discipline of `[guidi2026wi]`).
PrivateBench (Chapter 11) is the vehicle for both.

## 8.7 Why this ordering

The sequence tabular → graph → multimodal → foundation is not fashion-following; each step is
*motivated by the previous result*. The paper showed relational signals dominate → learn on the
graph. Graphs ignore documents → go multimodal. Multimodal models are re-trained per task → pretrain
a foundation model. The through-line is the reduction of bespoke feature engineering and the growth
of a shared, reusable representation.

---

## Open questions carried forward
- Which GNN family best fits a heterogeneous, temporal private-market graph?
- How to pretrain over a graph that is sparse, biased (survivorship), and partly proprietary?
- Can interpretability keep pace as representations become foundation-scale?

## To do for this chapter
- [ ] Expand §8.2 into a concrete Paper #3 experiment sketch (dataset, GNN type, baseline, metric).
- [ ] Add recent, *verified* GNN / multimodal / foundation-model citations to `98_References.md`
      (currently this chapter leans on the verified core set; deepen before final cut).
- [ ] Add Figure F8: representation-learning stages (tabular → GNN → multimodal → FM).
