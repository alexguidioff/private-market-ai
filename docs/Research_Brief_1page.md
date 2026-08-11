# Research Brief — Value of Information for Investment Decisions under Uncertainty

**Alessandro Guidi** · alexguidioff@gmail.com · alessandroguidi.site · linkedin.com/in/alessandroguidi1 · github.com/alexguidioff
**Level:** 📣 **[OUTREACH — public]** — the ONE document you send to a professor. One page. Nothing beyond P1 (+ a hint of P2).

> ⚠️ Fill [brackets] per professor. Attach the WI2026 one-pager. Do **not** send the white paper,
> the research agenda, or the company plan. (See `Outreach_Brief.md` for the disclosure rule.)

---

## The question
Investors decide under extreme uncertainty on fragmentary information. The standard AI framing —
*predict* which startup will succeed — is crowded and, ultimately, of limited use: **nobody buys a
prediction; investors buy information.** My interest is the prior, under-studied question:

> **Given a decision under uncertainty, which missing piece of information — at what cost — most
> improves the decision?**

This is *value of information* / active information acquisition, brought to private-market
investment decisions.

## What I have already done (the foundation)
My paper *Can Non-Financial Signals Price Private Companies?* (accepted, **WI2026 Student Track**;
with S. Rashid & H. Zhong, ESCP) shows, on 3,403 PitchBook deals with a strict out-of-time holdout,
that ML on **non-financial signals alone** prices private companies competitively with the best
financial baselines — and that **investor-syndicate structure**, not firm financials, is the
dominant driver. It also exposes the limit of a purely predictive approach, which is what motivates
the shift below.

## The proposed line of work
**P1 (flagship) — Value of Information for VC diligence.** Formalise each decision by its
*information state* (what is knowable at time *t*, reconstructed point-in-time), and ask which
acquisition most reduces decision uncertainty per unit cost:
`Decision(state) → acquire info (cost c) → state' → Decision(state')`.
The methods exist (Bayesian experimental design / expected information gain / active feature
acquisition; sequential decision-making under uncertainty); the **application to VC diligence is
open**. Feasibility does not depend on private data: a point-in-time reconstruction from public
sources plus a virtual-fund simulator provide ground truth.

*(If it grows: P2 — how to evaluate whether a decision was good* given what was knowable*, not by
its eventual outcome. But P1 is the focus.)*

## What I'm looking for
Methodological feedback, and whether this could become a **collaboration / research project / PhD**
in your group — I already have an accepted publication in the area and want to build a coherent
line of research, not a single paper.

## Why your group
[1–2 sentences, specific: e.g. *"Your work on [active learning / Bayesian experimental design /
optimization under uncertainty / decision-making under uncertainty — cite one paper] is exactly the
toolbox this question needs; I'd value your view on framing value of information as a sequential
decision problem in this domain."*]

---
*One-page summary of the WI2026 paper attached. Code and manuscript available on request.*

---
## Per-professor angle notes (do not send — internal)
- **Niao He (ETH ODI):** frame as *sequential decision-making / optimization under uncertainty*;
  cite an ODI RL/optimization-under-uncertainty paper. Funded (SNSF) + hiring → strong target.
- **A. Krause (ETH LAS):** frame as *active information acquisition for decision making*; cite his
  "Near-Optimal Bayesian Active Learning for Decision Making" / adaptive submodularity. Aspirational.
- **Ademi / Tykvová (HSG):** domain co-advisor angle — lead with the VC decision problem and the
  WI2026 result; position VoI as "what diligence to do, and why".
- **SDSC:** not this brief — apply to the open Research-Engineer role instead (`Outreach_Emails.md`).