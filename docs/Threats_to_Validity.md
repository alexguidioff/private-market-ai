# Threats to Validity — Structural Risks of the Research Programme

**Author:** Alessandro Guidi — v0.1 · **Level:** 🧭 NORTH STAR — private
**Purpose:** the honest, interview-grade catalogue of *structural* risks — flaws that would sink a
paper regardless of execution quality, because they touch **construct validity** ("are we measuring
what we claim?") or **identification** ("can this claim be supported at all with this data?").
Distinct from the *novelty* risks catalogued in `papers/notes/Prior_Art_Scan.md`.

> **Reading guide.** Most defences share one spine: *state the limit explicitly, and lean on the
> Simulator where real data cannot reach* — keeping **P1 as the robust paper** and treating P2/P4 as
> the exposed ones. Crucially, the trilogy is resilient: **P3 and P5 depend on P1, not on P2**
> (white paper §11.5), so a weak P2 does not collapse the downstream arc.

---

## Summary table

| # | Structural risk | Papers hit | Status | Severity |
|---|---|---|---|---|
| 1 | "Information state" (public) ≠ what the VC actually knew | P1 (real-data branch) | defended | high |
| 2 | Decision-quality ground truth does not exist outside the Simulator | P2 | defended (multi-label) | high |
| 3 | Circularity Simulator ↔ method | P1/P2/P5 | mitigated (§11.4.5–11.4.6) | closed |
| 4 | Simulator may not reproduce stylized facts | P1/P2/P5 | plan B defined | high (execution) |
| 5 | Causal claims without an identification strategy | P4, P1 | scoped + sensitivity | med-high |
| 6 | Whole trilogy hangs on P1 + Simulator | programme | monitored | medium |
| 7 | Decision Graph needs a fund's private history to bootstrap | P3 | scoped (synthetic-first) | med-high |
| 8 | "Integration is the moat" (incl. proprietary) vs "no proprietary dependency" | Ch.7 vs outreach | aligned | medium |
| 9 | Ch.3 §3.5 causal success criterion exceeds what the defences allow | Ch.3, P4 | softened | medium |

---

## Risk #1 — The information state is *observable/public*, not what the investor knew

**The flaw.** The programme rests on the *information state* at time *t* — "what the investor knew".
But point-in-time reconstruction recovers what was **publicly knowable**, a *subset* of the real
information state. A real VC also knew informal things absent from any database (a founder call, a
partner's tip, intuition). If the investor already knew — informally — what the model suggests going
to "acquire", the recommendation is empty. We would be measuring VoI against an impoverished state
that matches no real decision-maker.

**Defence (state it explicitly).** Reframe the object as an **observable/public information state**,
and the research question as *"given the publicly acquirable information, which is worth acquiring?"*
— honest and still valuable. The Simulator has **no such gap**: there the information state is
complete and known, so construct validity is exact; the flaw exists only on the real-data branch and
must be declared, not hidden.

**Extension — the private-information backtest (two tracks).**
- **Track A — in the Simulator, now (inside P1).** We control how much private information the
  investor already holds. Experiment: if the decision-maker already knows (say) 30% of what the model
  would recommend acquiring, does the VoI recommendation **degrade gracefully** or become useless?
  This tests robustness of the thesis to the information gap — free, because the Simulator allows it.
- **Track B — on real data, a later paper (needs a partner fund).** Recovering the private
  information a VC *actually* held requires anonymised fund decision logs. This is **P3 / later**,
  not P1. Do **not** promise the real-data version in P1 (no partner secured yet).

---

## Risk #2 — Decision-quality ground truth does not exist outside the Simulator

**The flaw.** On real data only the *outcome* is observed. Measuring *process quality* separated from
outcome needs a "this was a good decision" label that **no dataset contains**. So P2 risks living
only in the Simulator ("in my synthetic world my method recognises the good decisions I defined as
good") — circular and silent about the real world. The white paper Ch.10 open questions concede this.

**First defence — the dependency is not fatal.** P3 and P5 depend on **P1**, not P2 (§11.5). A weak
P2 does not collapse the arc. Frame this openly: the trilogy hangs on P1 (the robust paper), not on
the exposed one.

**Second defence — triangulated labels (many signals, not one).** Instead of one fragile source,
combine independent decision-quality labels and require agreement:
1. **Simulator ground truth** — strong but synthetic.
2. **Expert elicitation** — have real VCs rate historical decisions shown **only what was knowable at
   the time, with the outcome hidden**. This yields a *real* process-quality label decoupled from
   outcome. It is a **conjoint / vignette study — Ademi's methodological tradition** — so the HSG
   co-advisor directly enables the real-world label source once thought impossible.
3. **Weak track-record proxy** — top-quartile vs bottom-quartile decision-makers over many decisions
   (noisy but independent).
4. **Process-completeness metrics** — did the decision use the information available? (measurable from
   the Decision Graph).

If independent criteria agree, P2 gains construct validity on real data too, moving from
"Simulator-only" to "multi-source validated". Accept nonetheless that **P2 is intrinsically weaker
empirically than P1**; keep it *conditional* on Simulator success, never a forced second paper.

---

## Risk #3 — Circularity between Simulator and method (mitigated)

Already closed by the **separation of roles** (sealed DGP vs tested policy) and the **multi-world
recovery study** (per-world correlation, not averages). See white paper §11.4.5–11.4.6. Listed here
only for completeness — it is the one large structural risk already resolved in the documents.

---

## Risk #4 — The Simulator may not reproduce the stylized facts

**The flaw.** The validation plan (§11.4.3) *assumes* the Simulator will reproduce power-law returns,
stage-wise failure rates, the syndication→survival effect, etc. If those do not emerge without being
forced, the Simulator is unvalidated and P1/P2/P5 wobble. This is an **execution risk**, high impact.

**The distinction that saves it.** The Simulator serves **two goals with different realism needs**:
- **Goal 1 — validate the *method*** (recovery study, regret): needs *known ground truth*, **not
  realism**. An unrealistic-but-known world still proves "the method recovers truth". This goal
  **never fails** for lack of realism.
- **Goal 2 — generalise to the real world**: this needs realism (stylized facts).

So if realism fails, we lose the *generalisation* claims, **not the method**. **Plan B cascade:**
1. **Partial realism** — match a subset of stylized facts; scope claims to those regimes.
2. **Simulator as method-validation harness only** — move empirical VoI claims onto real point-in-time
   data with a noisy observed outcome proxy and a manually adjudicated public-evidence subset; do not
   describe either as decision-quality ground truth.
3. **Narrow-cohort calibration** — restrict to a sector/period where the facts *can* be matched.

**Exit criterion (Year-1 milestone).** Decide *before* building P2/P5 on top which stylized facts the
Simulator must reproduce within tolerance. If it fails, fall to Plan B early — at Year 1, not Year 3.

---

## Risk #5 — Causal claims without an identification strategy

**The flaw.** Ch.10.5 promises "prediction → causality" and P4 (gaming) requires it, but no
identification strategy (instruments, natural experiments, discontinuities) is specified. Causal
claims on observational VC data — riddled with selection and survivorship bias — are attacked in two
lines by any economist (and Tykvová/Ademi are economists).

**Defence — three levels of increasing honesty, use all:**
1. **Causality in the Simulator = free and rigorous.** The causal structure is known by construction;
   strong causal claims live here. Safe.
2. **On real data = no strong causal claims, but sensitivity analysis.** Instead of "X causes Y", say
   "X is associated with Y, and an unobserved confounder of strength ≥ Z would be needed to overturn
   it". The tool is the **E-value** (VanderWeele-style sensitivity analysis): cheap, standard, and it
   disarms "what about selection bias?" — the answer becomes "I quantified exactly how robust it is to
   unobserved confounding".
3. **A real causal claim needs a natural experiment** (exogenous shock, regulatory change,
   discontinuity). Do **not** promise it a priori — search for one; if found, it is a bonus. Never
   base P4 on the *hope* of finding one.

**Golden rule for the interview:** never promise causality on observational VC data without saying
*how* it is identified. "Simulator + E-value + possible natural experiment" is covered and honest.

---

## Risk #6 — The trilogy hangs on P1 + Simulator (programme-level)

**The flaw.** P2, P3 (partly), P5 all reuse P1's point-in-time dataset and the Simulator. If P1 slips
or the Simulator underwhelms, the whole arc slides. A single point of failure at *programme* level.

**Defence.** Ensure **P1 is publishable on its own** even if the Simulator turns out only "adequate":
P1 must depend on the Simulator's *sufficiency*, not its *perfection* (see Risk #4, Goal 1). Keep P1's
core contribution — VoI framing + point-in-time methodology — testable on real data using an explicitly
scoped weak outcome proxy and an adjudicated public benchmark. The Simulator supplies synthetic
recovery/counterfactual evidence; it is corroboration rather than real-world ground truth.

---

## Risk #7 — The Decision Graph needs a fund's private history to bootstrap

**The flaw.** P3 (human-AI committee) depends on the **Decision Graph** (information used,
alternatives, rationale, decision-maker, outcome). But a *real* Decision Graph requires a fund's
private decision history — the white paper (Ch.6 open questions) asks exactly *"how to bootstrap a
Decision Graph without access to a fund's private decision history?"*. So P3 inherits the same real-
data dependency as P2: it lives in the synthetic/seeded world until a partner fund appears. This is a
data dependency on top of the already-known "needs human subjects" risk — worth stating separately.

**Defence — synthetic-first, real-later, same shape as P2.**
1. **Simulator-seeded Decision Graph (now).** The Simulator emits decision records by construction
   (information state, alternatives, chosen action, outcome), so a synthetic Decision Graph exists
   for free and is enough to develop and stress-test the P3 methodology.
2. **Vignette / lab reconstruction (mid).** The same expert-elicitation study used for P2 (decisions
   shown with outcome hidden, Ademi-style) produces *real* decision records with rationale — a
   partial real Decision Graph without a partner fund.
3. **Partner-fund logs (late, upside).** The gold standard, kept as upside, never a prerequisite.

Consequence for sequencing: **P3 stays a late/stretch paper** not only for the human-subjects reason
but because its real Decision Graph is not yet available. P1/P2 must not depend on it.

---

## Risk #8 — "Integration is the moat" vs "no proprietary dependency"

**The flaw.** Ch.7 argues the durable advantage is **integration** of sources (including proprietary
PitchBook/Orbis) and notes the founding paper used PitchBook (3,403 deals). The outreach pitch,
however, is *"feasibility does not depend on proprietary data"*. Left unreconciled, a reviewer can
say: "if the moat is integrating proprietary feeds and the founding result uses PitchBook, then the
results *do* depend on proprietary data." The defence exists (proprietary as a *signal to be valued*,
public base reproducible) but **Ch.7 does not yet carry the caveat** — the two documents appear to
contradict.

**Defence — reconcile the two, do not drop either.** They describe *different layers*:
- **Reproducible base (public):** the point-in-time public stack (Ch.7 §7.6) is the floor; all core
  claims stand on it, so feasibility genuinely does not *depend* on proprietary data.
- **Optional premium layer (proprietary):** integrating PitchBook/Orbis is a *commercial/quality*
  advantage and, in the research, one of the **acquirable information steps whose marginal value is
  measured** (the VoI framing already added to the outlines). "Is the paid feed worth its cost?" is
  an instance of the research question, not a hidden dependency.
- **The moat is the *integration method*, not the ownership of any one feed** — which is exactly why
  it survives on public sources and merely *improves* with licensed ones.

**Action taken:** Ch.7 §7.2 now carries this caveat explicitly (see below), so "integration is the
moat" and "no proprietary dependency" no longer read as contradictory.

---

## Risk #9 — Ch.3 §3.5 causal success criterion exceeds the defences

**The flaw.** §3.5 lists as a "success" test: *"at least one causally-identified signal whose
intervention effect is estimated, not assumed."* But Risk #5 establishes that on observational VC
data we make **no strong causal claims** without a natural experiment (which cannot be promised). So
the stated criterion is more ambitious than the defences allow — an internal inconsistency a careful
reader will catch, and a criterion we might not be able to meet.

**Defence — soften to what is deliverable.** Restate the causal success criterion as: *"a causal
effect identified **in the Simulator** (where structure is known by construction), plus an
**E-value sensitivity analysis** on real data quantifying robustness to unobserved confounding; a
natural-experiment identification on real data is upside, not a requirement."* This keeps the
criterion falsifiable *and* achievable, and matches Risk #5.

**Action taken:** Ch.3 §3.5 causal bullet updated accordingly (see below).

---

## Cross-references
- Simulator design, validation-by-triangulation, separation of roles, recovery study, regret & cost:
  white paper `WhitePaper/11_Research_Roadmap.md` §11.4.1–11.4.8.
- Decision-quality theory & open questions: `WhitePaper/10_Decision_Intelligence_and_Uncertainty.md`.
- Novelty / prior-art risks (distinct from these structural risks): `papers/notes/Prior_Art_Scan.md`.
- Programme risk view & sequencing: `Research_Agenda.md` §4.
