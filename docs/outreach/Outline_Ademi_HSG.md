# PhD Project Outline — for Prof. Dr. Petrit Ademi (HSG, ITEM)

**Alessandro Guidi** · alexguidioff@gmail.com · alessandroguidi.site · linkedin.com/in/alessandroguidi1 · github.com/alexguidioff

> 📣 **[OUTREACH]** — the 1-page outline attached to the email. Scope: P0 (done) + P1 (flagship),
> with only a one-line hint of P2. **Domain-first tilt** — Ademi is an entrepreneurial-finance PI who
> studies how VCs actually decide; lead with the VC decision problem, keep the ML light.
> ✅ Verified from his HSG/Alexandria profile (fetched via user, 2026-07): email
> petrit.ademi@unisg.ch · ORCID 0000-0002-4443-1350 · Prof. Dr., ITEM-HSG.

---

## Working title
**The Value of Information in Venture Capital Diligence: Which Signals Are Worth Acquiring?**

## Target institution
University of St. Gallen, Institute of Technology Management (ITEM-HSG) — Prof. Dr. Petrit Ademi
(Entrepreneurial Finance). *A methodological co-advisor at ETH (decision-making under uncertainty /
optimisation) is envisaged for the modelling side.*

---

## 1. Research context & focus
Venture investors decide under extreme uncertainty on fragmentary, non-standardised information.
Research — including your own conjoint studies of how (corporate) venture capitalists evaluate
opportunities — has mapped *which attributes investors weight* when they screen and decide. The
question I want to open sits one step earlier and is, so far, largely unasked in venture finance:
given a decision, *which missing piece of information — at what cost — most improves it?* Not
"which feature predicts success," but "which diligence step is worth doing."

This builds on my accepted WI2026 Student Track paper (*Can Non-Financial Signals Price Private
Companies?*), which shows on 3,403 PitchBook deals, under a strict out-of-time holdout, that
non-financial signals price private companies competitively with financial baselines — and that
**investor-syndicate structure**, not firm financials, is the dominant driver. That last finding
connects directly to your work on syndication decisions, and it exposes the ceiling of a purely
predictive approach: knowing *what predicts* is not the same as knowing *what to go and learn*.

## 2. Research questions
**Main question:** In venture diligence, which information acquisition — at what cost — most
improves the quality of the investment decision?

- How can each decision be represented by its **observable public information state**: what was
  publicly knowable at time *t*, reconstructed point-in-time before the outcome is realised?
- How do we quantify the **marginal value** of an additional diligence step (a reference call, a
  cohort metric, a syndicate signal) relative to its cost?
- Which diligence steps do investors appear to **under- or over-invest in** relative to their
  information value — and does this differ across deal stages or syndicated vs solo deals?

## 3. Theoretical framework
The project brings the economics of *value of information* (Howard; Savage) into venture diligence.
Where your conjoint experiments identify the *revealed weighting* of attributes in investor
decision-making, value-of-information theory asks the normative counterpart: *what would be worth
knowing next.* Placing the two side by side — how investors actually weight information vs. how much
that information is objectively worth to the decision — is the conceptual core. The technical
machinery (Bayesian experimental design / expected information gain; sequential decision-making
under uncertainty) exists in the ML literature; its **application to venture diligence is open**,
and it needs a domain anchor in entrepreneurial finance to be posed correctly.

## 4. Methodology
Feasibility does **not** depend on proprietary data. A **point-in-time reconstruction** of public
sources defines the observable public information state and excludes look-ahead; its real-world
outcome is initially a weak, explicitly scoped SEC proxy, strengthened on a manually adjudicated
public-evidence subset. **Synthetic ground truth** comes only from a virtual-fund simulator, where it
supports counterfactual method validation. On top of this I estimate the value of each information
type and rank diligence steps by expected value per unit cost, benchmarked against the WI2026
pipeline as a predictive baseline. Proprietary sources (PitchBook, Orbis) are not dependencies; where
an institution lawfully provides them, they may be evaluated as optional acquirable signals. The
design naturally extends to your experimental tradition: a later stage could compare model-implied
information value against investors' revealed weighting in a conjoint-style study.

- **Year 1:** formalise the information-state / VoI framing; point-in-time dataset + simulator.
- **Year 2:** estimate information value across diligence steps; P1 completion and submission
  (*if it grows: P2 — evaluating decision quality by what was knowable, not by the eventual exit*).
- **Year 3–4:** extensions (syndication signals, human-vs-model weighting), writing, publications.

## 5. Expected contribution
The project contributes (i) a **value-of-information framing for venture diligence** — a normative
account of which signals are worth acquiring; (ii) a **reproducible point-in-time + simulator
methodology** that makes the question testable without proprietary data; and (iii) empirical
evidence, connectable to investors' revealed decision weights, on where diligence effort is
mis-allocated. It speaks to entrepreneurial-finance audiences (how investors decide) and generalises
beyond VC (PE, credit, M&A), which is what makes it a research line rather than a single study.

## 6. Fit with host institution
Your research programme — the decision-making of (corporate) venture capitalists, venture screening,
and syndication — is exactly the domain this question needs. *Venture Capital Screening* (Drover &
Ademi, 2024) frames the very act I want to formalise: what investors examine before committing.
Your conjoint experiments on CVC evaluation give a rigorous behavioural counterpart to the normative
value-of-information model, and your work on syndication decisions connects to my paper's central
finding. I would value ITEM-HSG as the domain home for the project, with an ETH methodological
co-advisor for the modelling. I already have an accepted publication in the area and want to build a
coherent line of research, not a single paper.

## 7. Selected references
- Howard, R. A. (1966). *Information Value Theory.* IEEE Trans. Systems Science and Cybernetics.
- Savage, L. J. (1954). *The Foundations of Statistics.*
- Drover, W., **Ademi, P.** (2024). *Venture Capital Screening.* Springer/Palgrave Macmillan
  (book section). *(the act this project formalises)*
- **Ademi, P.**, Schuhmacher, M., Zacharakis, A. (2023). *Evaluating Affordance-Based Opportunities:
  A Conjoint Experiment of Corporate Venture Capital Managers' Decision-Making.* Entrepreneurship
  Theory and Practice, 47(6). *(revealed weighting of information in investor decisions)*
- **Ademi, P.**, Schuhmacher, M., Zacharakis, A. (2023). *When Do Sharks Partner Up? An Experiment
  of Corporate Venture Capital Syndication Decisions.* *(links to the WI2026 syndicate finding)*
- Guidi, A., Rashid, S., Zhong, H. (2026). *Can Non-Financial Signals Price Private Companies?*
  WI2026 Student Track (accepted).

---
*One-page WI2026 summary attached. Code and manuscript available on request.*

> **Pre-send checklist:** [x] citations verified on Alexandria (ET&P 47(6); Screening = Springer/
> Palgrave; Sharks 2023) ✅ [ ] keep to ~1 page [ ] attach WI2026 one-pager + CV [ ] title/email verified ✅.
