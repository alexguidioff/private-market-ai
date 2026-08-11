# Paid contract work on backtest validity — how to actually start

**Drafted 2026-07-29.** Third path, distinct from "found a company" and "get into academia". Requires no
company formation, no fundraising, no charisma. Uses the one skill the research has actually demonstrated.

---

## Why this one is different from the ten dead hypotheses

Ten commercial hypotheses were tested and none survived. But the search method only ever produced
rejections: declared thresholds, falsification conditions, oracle bounds. **A falsification-only search
returns zero by construction**, because it has no confirmatory step. And the confirmatory step for demand
is talking to people who pay, which was ruled out.

This path dissolves that bind. The objection to interviews is correct: *stated* preference about a
hypothetical product is worthless. But a paid engagement is **revealed** preference. Someone either
transfers money or does not. So this is the only candidate on the list that can be validated by a method
already considered acceptable.

## What the service is

An independent audit of whether a model or backtest is measuring skill or measuring hindsight. Concretely:

- **look-ahead and leakage**: does the evaluation use information that did not exist at the decision date
- **circular evaluation**: is the label reachable through the same information path as the prediction
- **metric mismatch**: is an average metric being used to justify a decision taken only on the tail
- **bound the damage**: not "this is wrong" but "correcting it moves the number by X"

Every item is something already done on own work rather than theorised: three circularities caught,
including 1770/1770 positive pairs resolving to a single identifier; a documented average-versus-tail
divergence; a point-in-time pipeline that reconstructs only what was observable at date t.

## Step 1 — build the artefact, because low rizz means the document has to sell

Do **not** start with outreach. Start with one public audit, on public data, that demonstrates the service
on something a reader already cares about.

**Best target: audit a public benchmark for leakage.** VCBench exists and is cited in the field
(`Research_Agenda.md` notes its existence). A short, careful report showing whether a widely used benchmark
leaks the future, with the effect size measured, is simultaneously:

- a research output, publishable as a note and presentable at the ETH pre-NeurIPS poster session
- the public artefact that both the Agentic Systems Lab form and any September email to a chair currently lack
- a sales document that requires no pitching, because it shows the work instead of describing it

⚠️ **Do not audit a named private firm's published backtest as the opening move.** Public benchmarks and
own work only. Attacking a potential client's published numbers is not a first contact.

## Step 2 — the offer, fixed scope and fixed price

Not open-ended consulting. One package: a two to three week validity audit of a single model or backtest,
delivering a written report with findings ranked by measured impact on the headline number. Fixed price.
Fixed scope makes it a purchase decision rather than a hiring decision, which is what gets a first yes.

## Step 3 — who to approach, warmest first

1. **Capgemini, the former employer.** Two years in Technology Consulting for Tier-1 banking clients,
   Sep 2023 to Aug 2025, with roughly €2M in documented cost savings. This is the warmest channel that
   exists: ex-colleagues and managers who already know the work quality, at a firm that *sells* exactly
   this kind of specialist engagement and routinely subcontracts it. No cold outreach, no charisma
   required. **This channel has been sitting unused the entire time.**
2. **Model validation / model risk management functions at Swiss banks.** Independent model validation is
   a regulatorily required function, so the budget exists whether or not anyone is enthusiastic. That is
   the opposite of the discretionary tooling markets that killed the ten hypotheses. Look-ahead bias in
   backtests sits squarely inside their mandate.
3. **Asset managers in Lugano and Zurich.** Right density, but colder, and they are the third call rather
   than the first.

## Practicalities to verify, not to assume

- **Ability to invoice.** Registering as self-employed in Switzerland has real administrative
  requirements, including social-insurance registration and typically evidence of more than one client.
  Verify the current rules before promising an invoice date. Italian EU citizenship and Swiss work
  eligibility help but do not settle it.
- **Conflict with employment.** If the Apertus role or an ETH research-assistant post comes through, side
  contracting may be restricted. Check the terms before signing anything.
- **Tax residency** if invoicing from Italy while living in Zurich. Do not improvise this.

## Sequence

| When | What |
|---|---|
| Weeks 1–2 | Build and publish the benchmark leakage audit. This is also the missing public artefact. |
| Week 3 | Two emails: former Capgemini managers, and one model-validation contact. Artefact attached, fixed-scope offer named. |
| In parallel | ETH applications continue. Apertus Evaluations first. These do not conflict; an RA post plus one small engagement covers September. |

**The honest framing.** This is not a startup and should not be dressed as one. It is paid expert work
that happens to use the research, buys time, and produces the public artefact that unblocks the academic
route as a side effect. If it turns out nobody pays, that is a real negative result obtained by an
acceptable method, and it is worth more than the ten previous ones.
