# Chapter 7 — Data Sources & Data Engineering

**Status:** ✍️ draft v0.1 (prose) · **Fuses:** `datasets/README.md`, `Vision.md §7`,
`Private_Market_Data_Model.md §5`
**Level:** 🧭 NORTH STAR

---

## Abstract

A representation is only as good as the data that populates it. This chapter inventories the
private-market data landscape, argues that the durable advantage is **integration** rather than any
single feed, and addresses the practical concerns that determine whether the model can be built
responsibly: data quality, identity resolution, ingestion architecture, and — critically — the
legal and ethical limits of using sources such as PitchBook and LinkedIn. It also specifies a
**public-only starter stack** so that the research can be reproducible and shareable without
touching proprietary data.

---

## 7.1 The source landscape

No single provider covers the ecosystem; each is strong on one facet.

| Category | Source | Type | Access |
|---|---|---|---|
| Deals | PitchBook | Proprietary | License |
| Deals | Dealroom | Proprietary / Freemium | Account |
| Deals | Crunchbase | API | API key |
| Financials | Orbis | Proprietary | License |
| Founders / people | LinkedIn | Public / limited API | Restricted (ToS) |
| Code | GitHub | API | Token |
| Patents | Google Patents | Public | Open |
| Research | OpenAlex | API | Open |
| News / events | GDELT | API | Open |
| Web | Common Crawl | Public | Open |
| Hiring | LinkedIn Jobs | Limited API | Restricted |
| Funding filings | SEC (Form D, etc.) | Public | Open |
| Macro | World Bank, OECD, GEM | API / dataset | Open / academic |
| VC ecosystem | OpenVC | Public | Open |

The founding paper used **PitchBook (3,403 deals) + GEM** `[guidi2026wi]`; the programme's
ambition is to fuse many more of these into one temporal, multimodal graph.

## 7.2 Integration is the moat

Chapter 2's key observation was that incumbents are databases; §7.1 shows why. PitchBook has deep
structured deal data but not code; GitHub has code but not cap tables; LinkedIn has people but is
access-restricted; GDELT has events but not financials. **The defensible advantage is not owning a
dataset but integrating them** into a single represented world (Chapters 4–6). Integration is also
the hardest part — which is exactly why it is a moat.

> **Caveat — the moat is the integration *method*, not any single (proprietary) feed.** This must be
> reconciled with the programme's feasibility claim that *research does not depend on proprietary
> data*. The two are consistent across *layers*: the public point-in-time stack (§7.6) is the
> reproducible floor for method and proxy-scoped claims, so feasibility genuinely does not depend on
> licensed feeds. Strong priced/institutional or decision-quality claims require adjudicated evidence,
> expert labels or separate validation. Proprietary sources (PitchBook/Orbis) sit on top as an
> *optional premium layer* and, in the research itself, as **one of the acquirable information steps
> whose marginal value is measured** ("is the paid feed worth its cost?" is an instance of the
> value-of-information question, not a hidden dependency). Because the moat is the integration method,
> it survives on public sources
> and merely *improves* with licensed ones. See `Threats_to_Validity.md` #8.

## 7.3 Data quality as a modelled property

Quality is not a preprocessing step to be hidden; it is part of the representation (Chapter 4,
§4.4). Four dimensions are modelled explicitly and attached to every fact, event, and signal:
- **Coverage** — geography, stage, time window (e.g. the founding paper's post-2022 holdout).
- **Freshness** — update cadence; GEM is annual, GitHub is real-time.
- **Provenance** — which source asserted this, and when.
- **Confidence** — how much to trust it, propagated into distributional outputs (Chapter 10).

## 7.4 Identity resolution

The single hardest engineering problem: the same company or founder appears in PitchBook,
Crunchbase, GitHub, and LinkedIn under different names, spellings, and identifiers. Without robust
**entity resolution**, the knowledge graph fragments into duplicates and the relationship layer
(Chapter 5, §5.3) — including the syndicate structure that drives the paper's result — becomes
unreliable. Approaches: deterministic keys where they exist (domains, registration numbers),
probabilistic matching, and learned embeddings for fuzzy cases; all with human-in-the-loop review
for high-stakes merges.

## 7.5 Ingestion architecture

The pipeline must be both batch and streaming:
- **Batch** for bulk sources (filings, patents, macro).
- **Streaming / event-driven** for the dynamic layer (GitHub activity, news, hiring) that keeps
  Digital Twins current (Chapter 6, §6.2).
Connectors normalise each source into the ontology (Chapter 5); events are appended with
timestamps to preserve the bitemporal history.

## 7.6 A public-only starter stack (for reproducible research)

The reproducible core is `SEC Form D + manually adjudicated issuer/investor public evidence`, with
OpenAlex as the first candidate acquisition block and GDELT/Common Crawl as discovery layers. This
is sufficient to test point-in-time plumbing and proxy-scoped baselines without proprietary data;
it is **not** sufficient by itself to claim priced institutional rounds, VC success, or real-world
decision-quality ground truth. OpenVC and OpenCorporates are conditional discovery/matching sources,
not core dependencies, until their access and redistribution terms pass a run-specific audit.
GitHub historical features are blocked until a defensible 2016--2020 archive is identified; the
current Events API does not supply that history. Licensed data (PitchBook, Orbis, Crunchbase where
licensed) remain outside every reproducible public artifact.

## 7.7 Legal and ethical limits (must not be an afterthought)

Several sources carry real constraints, and the programme treats them as design boundaries:
- **PitchBook / Orbis:** licensed data — usable for research under licence, **not redistributable**.
  No proprietary data in public repos, benchmarks, or shared models.
- **LinkedIn:** scraping violates its terms; only compliant, limited-API or user-provided data.
- **Personal data:** founders and employees are individuals — provenance, consent, and data-
  protection rules (e.g. GDPR) apply, especially for behavioural signals.
- **Derived/de-identified artifacts** are the safe unit for sharing (Chapter 11).

> ⚠️ This section states principles, not legal advice. Specific source terms must be checked
> before ingestion, and a compliance review is warranted before any public release. (This also
> echoes the concrete `Amazon Confidential` labelling issue noted for the paper PDF in
> `papers/notes/WI2026_paper_summary.md` — provenance and classification travel with data.)

---

## Open questions carried forward
- How to score and surface data quality to downstream models and users?
- What is the minimum viable identity-resolution approach for a public-only prototype?
- Which licensed sources are worth the cost once a public baseline exists?

## To do for this chapter
- [ ] Specify the public-only starter stack schemas and connectors (ties to `code/`, `datasets/`).
- [ ] Draft a data-quality scoring method (§7.3).
- [ ] Add Figure F7: ingestion architecture (batch + streaming) — see `99_Figures.md`.
- [ ] Compile a per-source terms/limits table for the compliance review (§7.7).
