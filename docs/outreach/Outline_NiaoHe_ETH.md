# PhD Project Outline — for Prof. Niao He (ETH Zurich, ODI)

**Alessandro Guidi** · alexguidioff@gmail.com · alessandroguidi.site · linkedin.com/in/alessandroguidi1 · github.com/alexguidioff

> 📣 **[OUTREACH]** — the 1-page outline attached to the email. Scope: P0 (done) + P1 (flagship),
> with only a one-line hint of P2. Methods-first tilt (Niao He is a methodologist, not a finance PI).
> ⚠️ Before sending: confirm her exact title/email on odi.inf.ethz.ch, and re-check the two cited
> papers. Everything below about her group is from her official ODI page (fetched 2026-07).

---

## Working title
**Value of Information for Investment Decisions under Uncertainty: A Sequential Decision-Making Approach**

## Target institution
ETH Zurich, Department of Computer Science (D-INFK) — Optimization & Decision Intelligence (ODI)
Group, Institute for Machine Learning (Prof. Niao He). *Domain co-advisor envisaged at HSG
(private-markets / entrepreneurial finance).*

---

## 1. Research context & focus
Investors in private markets decide under extreme uncertainty on fragmentary, non-standardised
information. The dominant AI framing — *predict* which company will succeed — is increasingly
crowded and, on its own, of limited practical value: an investor does not buy a prediction, they
buy **information** that improves a decision. This project studies the prior, under-explored
question: given a decision under uncertainty, *which* missing piece of information — at what cost —
most improves the decision?

This builds on my accepted WI2026 Student Track paper (*Can Non-Financial Signals Price Private
Companies?*), which shows on 3,403 PitchBook deals, under a strict out-of-time holdout, that ML on
**non-financial signals alone** prices private companies competitively with financial baselines,
and that **investor-syndicate structure** — not firm financials — is the dominant driver. That
result exposes the ceiling of a purely predictive approach and motivates the shift from *prediction*
to *value of information*. The natural home for this shift is **decision-making under uncertainty**:
the acquisition of information is itself a sequential decision to be optimised, not a prediction to
be improved.

## 2. Research questions
**Main question:** In investment decisions under uncertainty, which information acquisition — at
what cost — most improves decision quality?

- How can each decision be represented by its **observable public information state**: what was
  publicly knowable at time *t*, reconstructed point-in-time before the outcome is realised?
- How do we quantify the **marginal value** of acquiring an additional piece of information
  (a signal, a due-diligence step) relative to its cost?
- Can the acquisition process be framed as a **sequential decision / optimisation-under-uncertainty
  problem** with regret or optimality guarantees on *which* step to take next under a cost budget?

## 3. Theoretical framework
The project sits at the intersection of **decision theory under uncertainty** and **information
economics**, operationalised with modern optimisation and ML. The core object is the *value of
information*: the expected improvement in decision quality from moving `Decision(state) → acquire
info (cost c) → state' → Decision(state')`. The natural formal home is the ODI group's own language —
the trade-off between **the value of more information and its cost**. This is precisely the object
of the group's work on the *bias–variance–cost trade-off of stochastic optimisation* (NeurIPS 2021):
acquiring more/better information reduces error but is costly, and the question is how much to
acquire and when to stop. My project transports that trade-off from the estimation setting into a
*decision* setting — where the "sample" is a diligence step and the "error" is decision regret.
Two further group results give the sequential machinery: constrained-MDP formulations with regret
guarantees (*Truly No-Regret Learning in Constrained MDPs*, ICML 2024) formalise "acquire the
highest-value information subject to a cost/time budget," and stochastic-optimisation-under-
uncertainty for revenue management (*Operations Research* 2024) is a template for turning a real
allocation decision into a tractable objective. The methods exist; their **application to
private-market investment decisions is open**.

## 4. Methodology
Feasibility does **not** depend on proprietary data. A **point-in-time reconstruction** of public
sources defines the observable public information state and excludes look-ahead; its real-world
outcome is initially a weak, explicitly scoped SEC proxy, strengthened on a manually adjudicated
public-evidence subset. **Synthetic ground truth** comes only from a virtual-fund simulator, where it
supports counterfactual method validation. On top of this I formalise value-of-information estimators
and an acquisition policy that selects the next diligence step by expected marginal value per unit
cost, benchmarked against the WI2026 pipeline as a predictive baseline. Proprietary sources (e.g.
PitchBook, Orbis) are not a dependency but may later enter as optional acquirable information steps
whose marginal value is estimated — so "is this paid signal worth its cost?" remains a research
question rather than a precondition.

- **Year 1:** formalisation of the information-state / VoI objective; point-in-time dataset +
  simulator; first acquisition-policy experiments.
- **Year 2:** P1 completion and submission (*and, if it grows, P2 — how to evaluate whether a
  decision was good given what was knowable, not by its eventual outcome*).
- **Year 3–4:** extensions (robustness, portfolio-level acquisition), writing, publications.

## 5. Expected contribution
The project contributes (i) a **formalisation of value of information for private-market decisions**
as a sequential optimisation-under-uncertainty problem, (ii) a **reproducible point-in-time +
simulator methodology** that makes the question testable without proprietary data, and (iii)
empirical evidence on which information is worth acquiring in VC diligence. The contribution is
domain-general: the same formulation applies beyond venture capital (private equity, credit, M&A),
which is what makes it a research line rather than a single application.

## 6. Fit with host institution
The ODI group's stated focus — *"algorithmic and theoretical foundations for solving data-driven
decision-making problems, large-scale optimization, optimization under uncertainty, reinforcement
learning"* — is precisely the toolbox this question needs. Framing value of information as a
sequential/constrained decision problem is a direct extension of the group's optimisation-under-
uncertainty and constrained-MDP work into a new, high-stakes application domain. The methodological
core would live in your group; a private-markets co-advisor at HSG (Prof. Tykvová / Prof. Ademi)
would anchor the domain, giving the "ML rigor + domain credibility" pairing. *(I note the group's
SNSF Starting Grant and current openings — I would be glad to discuss whether this fits a funded
position.)*

## 7. Selected references
- Howard, R. A. (1966). *Information Value Theory.* IEEE Trans. Systems Science and Cybernetics.
- Savage, L. J. (1954). *The Foundations of Statistics.*
- Hu, Y., Chen, X., **He, N.** (2021). *On the Bias-Variance-Cost Tradeoff of Stochastic
  Optimization.* NeurIPS 2021. *(closest thematic anchor — information has a cost)*
- Müller, A., Alatur, P., Cevher, V., Ramponi, G., **He, N.** (2024). *Truly No-Regret Learning in
  Constrained MDPs.* ICML 2024. *(acquisition under a cost/time budget)*
- Chen, X., **He, N.**, Hu, Y., Ye, Z. (2024). *Efficient Algorithms for a Class of Stochastic
  Hidden Convex Optimization and its Applications in Network Revenue Management.* Operations Research.
- Guidi, A., Rashid, S., Zhong, H. (2026). *Can Non-Financial Signals Price Private Companies?*
  WI2026 Student Track (accepted).

---
*One-page WI2026 summary attached. Code and manuscript available on request.*

> **Pre-send checklist:** [ ] confirm the two He papers' author list/venue on odi.inf.ethz.ch
> [ ] confirm her exact title/email [ ] keep to 2 pages [ ] attach WI2026 one-pager + CV.
