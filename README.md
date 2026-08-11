# Private-Market-AI

Personal research repository for building the scientific foundations of
**Decision Intelligence for Private Capital Markets**
(Venture Capital, Growth Equity, Private Equity, Family Offices, Corporate VC).

> **Mission**
> We build the scientific foundations of Decision Intelligence for Private Capital Markets.
>
> *(Sub-theme: understand, represent, and augment human decision-making under uncertainty.)*

> **Guiding research question**
> How should AI *represent* private companies and *support* investment decisions under uncertainty?

---

## ⚠️ Disclosure discipline (read this first)

This repository has **two levels**. Keep them separate. This is a strategy, not an accident.

- **NORTH STAR (private)** — the full 10–15 year vision, theory, infrastructure, roadmap.
  This is *your* mental operating system. It exists so your research does not become a
  disconnected series of papers. **You almost never show it in full.**
- **OUTREACH (public)** — what a professor actually sees: the accepted foundational study + one
  clear research question + a concrete P1 idea on **cost-aware Value of Information**. That's it.

> The bigger the vision, the *less* you talk about it early. What convinces a professor is not a
> 10-year plan — it's an excellent first step and the ability to nail the second.
> (Think LeCun publishing one brick at a time, not announcing "foundation models" in 1990.)

Every document is tagged **[NORTH STAR]** or **[OUTREACH]** at the top.

---

## Why this repository exists

The central lab of a long-term research program that starts from an accepted master-thesis
paper and grows into a coherent research agenda, publications, and — eventually — a spin-off.

Positioning has evolved through the project:
`startup valuation` → `AI for private markets` → **`Decision Intelligence for Private Capital Markets`**.
Valuation is the **first use case / wedge**, not the product. Private markets are the
**non-negotiable domain**, not one case study among many — they are what makes the work
credible and hard to copy.

---

## Repository structure

```
Private-Market-AI/
│
├── README.md                          ← you are here
│
├── docs/
│   ├── Vision.md                      [NORTH STAR] founding / strategic document
│   ├── Theory.md                      [NORTH STAR] Investment Intelligence Theory
│   ├── Research_Infrastructure.md     [NORTH STAR] PrivateBench, Simulator, Digital Twin, Decision Graph
│   ├── Roadmap.md                     [NORTH STAR] research + technology + architecture roadmap
│   ├── Private_Market_Data_Model.md   [NORTH STAR] Paper #0: data model + decision graph
│   ├── Ontology.md                    [NORTH STAR] entities, relationships, events
│   ├── Startup_Ideas.md               [NORTH STAR] product evolution & commercialization
│   ├── Funding.md                     [NORTH STAR] grants & funding strategy
│   ├── Entry_Paths.md                 [NORTH STAR] 6 ways into the Swiss ecosystem (PhD is only one)
│   ├── Professors.md                  [NORTH STAR] target groups & outreach database
│   ├── Group_Funding_DD.md            [NORTH STAR] funding due diligence — the career CRM
│   ├── Research_Log.md                [NORTH STAR] operational notebook ("second brain")
│   ├── Entry_Paths.md                 [NORTH STAR] 6 ways into the Swiss ecosystem (PhD is only one)
│   ├── Group_Funding_DD.md            [NORTH STAR] funding due diligence — the career CRM
│   ├── STATUS_MEMO.md                 [NORTH STAR] what exists / what's missing / next
│   ├── WhitePaper/                    [NORTH STAR] the 50–100pp lab manifesto (scaffold, fill later)
│   ├── Academic_Profile.md            [OUTREACH]  CV / Scholar / ORCID / website checklist
│   ├── Outreach_Brief.md              [OUTREACH]  the ONLY things you show: 5-pager + elevator pitch
│   ├── WI2026_OnePager.md             [OUTREACH]  the paper in one page (attach to emails)
│   ├── Research_Statement.md          [OUTREACH]  1-page research statement
│   └── Outreach_Emails.md             [OUTREACH]  personalized email drafts (SDSC, Ademi, Borth)
│
├── papers/     (+ notes/)             index of papers + reading notes
├── datasets/                          data source inventory (no proprietary data)
├── code/                              pipeline documentation (no proprietary data)
└── experiments/                       experiment log
```

---

## How to use it

- **For professors (now):** use only `Outreach_Brief.md` + the WI2026 one-pager. Talk about the
  accepted foundational study and P1: cost-aware Value of Information for VC diligence.
- **For P0 execution:** `programme.yaml` is the canonical sequence; use
  `docs/P0_EXECUTION_PLAN.md`, `docs/protocols/P1_VoI_Protocol.md`, and
  `docs/EVIDENCE_REGISTER.md` as the operating set.
- **For yourself:** everything tagged NORTH STAR is the compass — it decides which papers to
  write, which skills to build, which data to collect.
- **Research_Log.md** is updated continuously — after every meeting, paper, experiment, idea.
- Never commit proprietary data (PitchBook, etc.). Keep only descriptions and shareable artifacts.

---

## Status

- ✅ Master thesis completed — *Machine Learning for Startup Valuation*
- ✅ Paper accepted — *Can Non-Financial Signals Price Private Companies?* (WI2026 Student Track)
- ✅ Long-term research vision + theory defined (north star)
- ⏳ Building academic profile and Wave-1 research-group outreach

**Author:** Alessandro Guidi · **Version:** v0.2
