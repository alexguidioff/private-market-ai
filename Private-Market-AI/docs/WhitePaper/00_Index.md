# White Paper — Master Index
## *Decision Intelligence for Private Capital Markets: Foundations, Representation, and Systems*

**Author:** Alessandro Guidi · **Target length:** 50–100 pages · **Status:** ✍️ full draft v0.1
(all 13 chapters drafted in prose; figures, some citations, and two worked examples pending)
**Level:** 🧭 **[NORTH STAR — private]** — the lab manifesto. NOT for early outreach.

> ⚠️ **Sequencing note (read `Vision.md §0.1`).** This is a NORTH STAR document. Fill it
> *progressively*, ideally **after** the first professor calls, so the vision consolidates
> before it is cast in 100 pages. It is the document you'd eventually use for a serious grant
> (BRIDGE/Innosuisse) or a deeply-interested professor — not a cold first contact.

---

## Purpose
A single, coherent technical volume — written like an ETH/Stanford lab manifesto — that fuses
the scattered NORTH STAR documents into one narrative with abstract, figures, diagrams, and a
bibliography. ~70% of the raw content already exists across `docs/`; this is assembly +
expansion + academic rigor.

## How to work on it
- One file per chapter in this folder (`01_...md` → `13_...md`).
- Each chapter file lists: **status**, **source docs to fuse**, a **section skeleton**, and
  **what's missing**.
- Write prose into the skeletons; keep `docs/*` as the living "source of truth" and sync back.
- Add references in `98_References.md`; track figures in `99_Figures.md`.

---

## Table of Contents

| # | Chapter | Primary source(s) | Status |
|---|---|---|---|
| 1 | Vision & Philosophy | `Vision.md`, `Theory.md` | ✍️ draft v0.1 |
| 2 | State of the Art | `Vision.md §2` | ✍️ draft v0.1 |
| 3 | Grand Challenge & Research Questions | `Vision.md §0.0`, `Theory.md` | ✍️ draft v0.1 |
| 4 | The Private Market Data Model | `Private_Market_Data_Model.md` | ✍️ draft v0.1 |
| 5 | Private Market Ontology | `Ontology.md` | ✍️ draft v0.1 |
| 6 | Knowledge Graph & Decision Graph | `Private_Market_Data_Model.md §4` | ✍️ draft v0.1 |
| 7 | Data Sources & Data Engineering | `datasets/`, `Vision.md §7` | ✍️ draft v0.1 |
| 8 | Representation Learning & Foundation Models | `Roadmap.md §3` | ✍️ draft v0.1 |
| 9 | Agentic Investment Systems | *new* | ✍️ draft v0.1 |
| 10 | Decision Intelligence & Uncertainty | `Theory.md` | ✍️ draft v0.1 |
| 11 | Research Roadmap 2026–2035 | `Roadmap.md §4` | ✍️ draft v0.1 |
| 12 | Technology Roadmap & Architecture | `Roadmap.md §3–3b` | ✍️ draft v0.1 |
| 13 | Commercialization & Funding Strategy | `Startup_Ideas.md`, `Funding.md` | ✍️ draft v0.1 |
| 98 | References | — | 🔴 to populate |
| 99 | Figures & Diagrams | — | 🔴 to populate |

---

## Front matter — ✅ drafted in `00a_Front_Matter.md`
- [x] Title page
- [x] Abstract (1 page)
- [x] Executive summary
- [x] Reading guide (who should read which chapters)

## Global TODO (post full-draft)
- [x] All 13 chapters drafted in prose (v0.1).
- [x] Chapter 9 (Agentic Investment Systems) written from scratch.
- [x] Chapter 8 expanded beyond the thin source.
- [x] **Figures F1–F13** — all drafted as Mermaid in `figures/figures.md` (tracker: `99_Figures.md`).
      Key ones (F1, F4, F6, F10, F12) referenced inline in their chapters; embed the rest as a polish pass.
- [x] **Worked example** (Ch. 4 §4.6) drafted as synthetic "NimbusAI" across all six layers.
      TODO: swap for a real, public-source-populated company (also seeds PrivateBench).
- [ ] **Citations:** deepen §E (AI-in-VC) and §G (decision science/causality) in `98_References.md`;
      verify all 🟡 entries (agentic-DD) before any external sharing.
- [x] Ontology serialization decided (JSON-schema-first) → v0.2 in `../Ontology_v0.2.md`.
      TODO: validate, add cardinality constraints, RDF/OWL export.
- [x] Front matter (title page, abstract, executive summary, reading guide) — `00a_Front_Matter.md`.
- [ ] Consistency pass: cross-references, terminology, and the disclosure tags across chapters.
