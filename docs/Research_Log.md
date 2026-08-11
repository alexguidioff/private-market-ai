# Research Log

Operational notebook for the research program — the "second brain".
Update this file continuously: after every meeting, paper read, experiment, idea, or email.

> **Research question:** How can AI represent, reason about, and support investment decisions
> in private capital markets?

---

## Current Status
- ✅ Master thesis completed.
- ✅ WI2026 paper accepted (Student Track).
- ✅ Long-term vision defined (`Vision.md`) + mission set to *Decision Intelligence for Private Capital Markets*.
- ✅ Theory (`Theory.md`) and research infrastructure (`Research_Infrastructure.md`) drafted [NORTH STAR].
- ✅ Outreach material separated (`Outreach_Brief.md`) [OUTREACH] — the only thing shown to professors.
- ⏳ Building academic profile and Wave-1 outreach.

> **Disclosure discipline:** NORTH STAR docs = private compass; OUTREACH docs = professor-facing.
> Pitch only the accepted foundational study → P1 cost-aware Value of Information. Never the full roadmap.

---

## Immediate TODO

### Academic profile
- [ ] Academic CV (LaTeX, 2 pages, MIT/Stanford style)
- [ ] Research Statement (1 page) — title: *AI for Private Market Decision Systems*
- [ ] WI2026 one-pager (problem, dataset, method, results, contribution)
- [ ] Google Scholar profile
- [ ] ORCID
- [ ] Personal website (bio, CV, papers, GitHub, contacts)
- [ ] Clean public GitHub repo (no proprietary PitchBook data)
- [ ] LinkedIn headline: "Product Manager @ Amazon | AI for Private Markets | WI2026"

### P0 execution (started 2026-07-21)
- [x] Freeze canonical programme sequence and evidence maturity.
- [x] Formalize P1 state, acquisition action, utility, cost, NDV and falsification gate.
- [x] Define provisional narrow cohort and PiT data contract.
- [x] Add executable decision schema and synthetic oracle smoke harness.
- [ ] Pass source-access/cohort/utility gates; then run EXP-001.

### Research
- [ ] Private Market Data Model v0.1 (RFC)
- [ ] Ontology draft
- [ ] Knowledge Graph design
- [ ] Data source inventory (see `datasets/README.md`)
- [ ] Read 30 papers (log below)

### Networking
Swiss group map complete → see `Professors.md` (15 groups + 3 waves).
**Wave 1 (do now):** Ademi (HSG) · Borth (HSG) · Gonon (HSG) · Tykvová (HSG) · Krause/ETH AI Center · SDSC
- [x] **Verified all 6 Wave-1 identities on official sources (2026-07)** → see `Group_Funding_DD.md §4b`.
      Key: SDSC is *actively hiring* Research Engineers (best paid entry); Ademi's institute is
      ITEM-HSG (corrected); Borth's SNSF grant number still UNVERIFIED — don't cite it yet.
- [ ] Verify Borth SNSF grant manually on data.snf.ch; collect exact emails
- [ ] Read ≥2 papers per Wave-1 professor
- [ ] Write one-page research brief (title, abstract, main result, ask, 3 directions)
- [ ] Send Wave-1 emails (Ademi first, then Borth, then Gonon)
- [ ] Do first 3–5 calls (use the 3 call questions in `Professors.md`)
- [ ] Wave 2 after first replies: ETH D-MTEC · EPFL AI Center · EPFL MLO · Gruber (EPFL) · UZH FinTech Lab

### Funding (later)
- [ ] BRIDGE
- [ ] Innosuisse
- [ ] ETH Pioneer Fellowship
- [ ] Venture Kick

---

## 30-Day Campaign

| Week | Focus |
|---|---|
| 1 | Academic CV · Research Statement · One-pager |
| 2 | GitHub · Website · Google Scholar · ORCID |
| 3 | Database of 15 groups · read their papers |
| 4 | First 5 emails · first calls |

---

## Reading Notes (papers)
> Format: `[YYYY-MM-DD] Author (Year) — Title — 2-line takeaway — relevance (A/B/C)`

- [2026-07] Built a verified core bibliography → `WhitePaper/98_References.md` (SHAP, Random
  Forest, XGBoost, Transformer, Hyper-Representations, Knowledge Graphs survey, UMLS) + a list of
  recent AI-in-VC papers (2023–2026) marked "found, verify authors before citing".
- [2026-07] **Extracted the real WI2026 paper** (PDF on Desktop) → `papers/notes/WI2026_paper_summary.md`.
  Corrections applied across docs: (1) **three authors** (Guidi, Rashid, Zhong), not single-author;
  (2) real results — Layer-2 Random Forest R² 0.557 / MAE 0.888, "information saturation", investor
  syndicate as dominant SHAP driver — the old "R²≈0.45 / half variance unexplained" framing was wrong.
  17 real references merged into `98_References.md §H`.
- ⚠️ **Compliance:** paper PDF is labelled "Amazon Confidential" → re-export clean copy before sharing.
- _(add per-paper notes as you actually read them — 2 per Wave-1 professor)_

---

## Meetings Log
> Format: `[YYYY-MM-DD] Person / Group — key points — follow-up actions`

- _(empty)_

---

## Ideas Inbox
> Dump raw ideas here, refine later.

- Ontology for private markets as an open standard (analogous to SNOMED CT / UMLS).
- Evaluation metric based on *decision quality*, not only prediction error.
- Temporal multimodal knowledge graph as the core representation.
- **[parked]** Investment Memory / episodic memory for an investing AI (a fund accumulates memory;
  each startup reshapes how the next is judged). Possible P6+ or a platform mechanism — after the trilogy.
- **[parked]** Rename the lab "Computational Investment Science" / "Computational Decision Science" —
  a more durable banner for a 10-year career. Future option, NOT a change now (keep mission fixed).
- **[parked]** Portfolio VoI (P5) as a full Operations-Research line — likely first post-PhD direction.
> Parking rationale: protect focus — an excellent P1 beats five mediocre ideas. See `Theory.md §9`.

---

## Experiments
> Link to `experiments/` entries.

- _(empty)_

---

## Open Questions
- How should private companies be represented digitally?
- Which signals matter most?
- How can AI explain investment decisions?
- How should multimodal data be integrated?
- Can AI participate in investment-committee reasoning?
