# PhD Project Outline — for Prof. Andreas Krause (ETH Zurich, LAS)

**Alessandro Guidi** · alexguidioff@gmail.com · alessandroguidi.site · linkedin.com/in/alessandroguidi1 · github.com/alexguidioff

> 📣 **[OUTREACH]** — 2-page outline for the LAS application. Scope: P0 (done) + P1 (flagship),
> one-line hint of P2. **Nothing about P3/P4/P5 or the company.**
>
> **Framing rule (differs from the ODI outline):** LAS *built* the VoI apparatus (adaptive
> submodularity, submodular surrogates for VoI, Bayesian active learning for decision making).
> Do **not** pitch "I want to work on value of information" as if it were news to them. Pitch a
> **new, high-stakes application domain their theory has never been tested on**, plus an honest
> negative result that makes the domain non-trivial.
>
> ⚠️ **Pre-send:** verify every cited LAS paper on las.inf.ethz.ch/publications (all listed below
> were read off that page, 2026-07). Verify Hübotter's papers before citing him.

---

## Working title
**Decision-Oriented Information Acquisition for Private-Market Investment Decisions:
When Does Acquiring the Next Signal Pay for Itself?**

## Target institution
ETH Zurich, D-INFK — Learning & Adaptive Systems Group (Prof. Andreas Krause), Institute for
Machine Learning. *Domain co-advisor envisaged at HSG (private markets / entrepreneurial finance).*

---

## 1. Research context

An investor deciding under uncertainty does not buy a prediction. They buy **information** that
changes a decision. Yet the dominant AI framing in private markets is predictive: forecast which
company succeeds. That framing is crowded and, taken alone, answers the wrong question — it
improves an estimate without telling anyone what to go and find out next.

The prior question is decision-oriented: **given the current information state and a cost budget,
which information block — if any — should be acquired before continuing or stopping diligence?**

This is not a new question in the abstract. It is precisely the object of your group's work on
[optimizing value of information](http://las.ethz.ch/files/chen15submsrgtvoi.pdf), of
*Near-Optimal Bayesian Active Learning for Decision Making* (Javdani et al., AISTATS 2014), and of
adaptive submodularity as a structural condition under which adaptive greedy acquisition is provably
near-optimal (Golovin & Krause, JAIR 2011). Yuxin Chen's ETH thesis, *Near-optimal Adaptive
Information Acquisition* (2017), is the closest existing statement of the machinery.

**What is open is the domain.** That apparatus has been validated on active learning, troubleshooting,
object detection, sensor placement and viral marketing — settings with cheap, repeatable, largely
independent tests. Private-market investment decisions violate almost every one of those conveniences:
tests are expensive and slow, correlated, partly unobservable, and the outcome arrives years later
under confounding. My claim is not that the theory needs replacing. It is that **this is the setting
in which its assumptions bind hardest, and nobody has checked what happens there.**

## 2. Research questions

**Main question:** In investment decisions under uncertainty, which information acquisition — at what
cost and delay — most improves decision quality, and when should acquisition stop?

- How should the **information state** `I_t` be defined so that it contains only what was defensibly
  observable at time `t`, with no look-ahead?
- Do the structural conditions that license near-optimal adaptive greedy acquisition (adaptive
  submodularity, or a usable surrogate) **hold, approximately hold, or fail** when tests are costly,
  correlated and noisy in the way diligence steps are?
- Under what cost structure does a decision-aware acquisition policy beat cheaper heuristics on
  **net decision value** — and under what cost structure does it provably not?

That third question is where my current evidence points, and I state it as a question rather than a
claim because my own result so far is negative. See §4.

## 3. Foundation and honest evidence boundary

**Completed work (P0).** *Can Non-Financial Signals Price Private Companies?* (Guidi, Rashid & Zhong;
accepted, **WI2026 Student Track**). On 3,403 PitchBook deals under a strict out-of-time holdout
spanning the 2022 regime shift, non-financial signals priced private companies competitively with the
strongest financial baseline, and investor-syndicate capacity was the most influential signal among
those tested. The value of that result here is diagnostic: it maps the ceiling of the predictive
framing and motivates the shift to acquisition.

**Current state of the flagship (P1) — stated plainly.** I have built a point-in-time pipeline on
public SEC data: US technology-related primary issuers with non-amendment Form D anchors; decision
time 12 months after filing availability; company-disjoint temporal splits (development 2021,
validation 2022, locked test 2023 untouched).

- A real SEC-history information block is **predictive**: the frozen baseline reaches ROC-AUC 0.6551
  on 2022 validation, and transports across cohorts.
- The **cost-aware value-of-information policy currently fails** to beat the preregistered non-VoI
  baselines on net decision value. This is an exploratory negative result, not a published finding.
- The outcome label is an explicitly **weak proxy** (a later non-amendment Form D notice within 18
  months) — not a priced round, Series A, or success label. A 20-case model-reviewed pilot reached
  75% raw exact agreement with 45% initially unresolved; I treat it as adequate for protocol
  development and sensitivity analysis only, **not** as human-adjudicated gold data.

I lead with the negative result deliberately. Either the utility model is mis-specified, or the cost
structure of public information makes acquisition genuinely not worth it in this regime, or the
structural conditions for decision-oriented greedy acquisition do not hold here. **Which of those
three it is, is a research question worth a thesis, and it is a methodological question, not a
finance one.**

## 4. Methodology

Feasibility does not depend on proprietary data.

1. **Point-in-time reconstruction** from dated public evidence defines `I_t` and excludes look-ahead.
   Proprietary sources (PitchBook, Orbis) are not a dependency; they may later enter *as acquirable
   blocks whose marginal value is estimated* — so "is this paid signal worth its cost?" stays a
   research question rather than a precondition.
2. **Diagnosing the negative result**: separate mis-specified utility from genuinely unfavourable
   cost structure from failure of the structural conditions. This is the Year-1 core and the part
   that most needs your group's theory.
3. **A synthetic multi-world harness** where the data-generating process is sealed from the tested
   policy, used for recovery and counterfactual checks. It validates plumbing and method recovery;
   it does **not** establish market realism, and I will not present it as evidence of real-world
   performance.
4. **Preregistered baselines** — acquire-all, acquire-none, cheapest-first, uncertainty-based,
   decision-aware VoI — scored on decision value net of information cost and delay, never on
   prediction accuracy alone. The 2023 cohort stays locked.

- **Year 1:** formalise the acquisition objective and stopping rule; diagnose the negative result;
  test whether a usable structural condition or surrogate exists in this setting.
- **Year 2:** P1 completion and submission. *(If it grows: how to judge whether a decision was good
  given what was knowable, separately from how it turned out.)*
- **Year 3–4:** robustness, correlated and partially observable tests, writing.

## 5. Expected contribution

(i) A **stress test of decision-oriented information acquisition** in a domain where its standard
assumptions are violated — costly, delayed, correlated, partly unobservable tests with confounded
long-horizon outcomes; (ii) a **reproducible point-in-time methodology** that makes the question
testable on public data, with the evidence boundary stated rather than blurred; (iii) a characterisation
of **when cost-aware acquisition does and does not pay**, which is domain-general — the same
formulation applies to credit, M&A, and clinical or defence triage. Private markets are the entry
domain, not the limit.

## 6. Fit with LAS

Your group's stated focus is systems that *"actively acquire information, reason and reliably make
decisions in complex and uncertain domains."* My project is that sentence applied to a domain the
group has not worked in, and it arrives with the infrastructure already built and a falsified first
attempt rather than a proposal.

I am aware the group's current output centres on foundation models, flow-based generative
optimisation, test-time training and RL rather than the 2010–2017 VoI line. I read that as an
opportunity rather than a mismatch: the recent work on **active data selection** — deciding which
data is worth acquiring at test time — is the same question under a modern name, and my setting
supplies an application where acquisition cost is real money and real delay rather than compute.

What I bring is not theoretical depth, which is what I am asking to acquire. It is a built
point-in-time data layer, an engineering background (Amazon; product management), a strict evaluation
discipline, and a demonstrated willingness to report my own negative result before someone else finds it.

## 7. Selected references

- Howard, R. A. (1966). *Information Value Theory.* IEEE Trans. Systems Science and Cybernetics.
- Golovin, D. & **Krause, A.** (2011). *Adaptive Submodularity: Theory and Applications in Active
  Learning and Stochastic Optimization.* JAIR 42. *(IJCAI-JAIR Best Paper 2013)*
- Javdani, S., Chen, Y., Karbasi, A., **Krause, A.**, Bagnell, J. A., Srinivasa, S. (2014).
  *Near-Optimal Bayesian Active Learning for Decision Making.* AISTATS. *(closest anchor: acquire
  enough to decide, not to identify)*
- Chen, Y., Javdani, S., Karbasi, A., Bagnell, J. A., Srinivasa, S., **Krause, A.** (2015).
  *Submodular Surrogates for Value of Information.* AAAI.
- Chen, Y., Renders, J. M., Chehreghani, M. H., **Krause, A.** (2017). *Efficient Online Learning for
  Optimizing Value of Information.* UAI.
- Chen, Y. (2017). *Near-optimal Adaptive Information Acquisition: Theory and Applications.*
  PhD thesis, ETH Zurich.
- Ma, C. et al. (2019). *EDDI: Efficient Dynamic Discovery of High-Value Information.* ICML.
  *(maximises information about targets; P1 must maximise net decision value — the gap I work in)*
- Fu, H. & Taylor, L. (2024). *Due Diligence and the Allocation of Venture Capital.* SSRN 5014747.
  *(nearest domain neighbour: how much diligence; P1 asks which information next, and when to stop)*
- Gompers, P., Gornall, W., Kaplan, S., Strebulaev, I. (2020). *How Do Venture Capitalists Make
  Decisions?* JFE.
- Guidi, A., Rashid, S., Zhong, H. (2026). *Can Non-Financial Signals Price Private Companies?*
  WI2026 Student Track (accepted).

---
*One-page WI2026 summary attached. Code, point-in-time pipeline and manuscript available on request.*

> **Pre-send checklist:**
> [ ] verify all six LAS citations on las.inf.ethz.ch/publications
> [ ] verify Hübotter's active-data-selection papers before naming him (§6 currently avoids naming)
> [ ] confirm ROC-AUC 0.6551 and split sizes against `programme.yaml`
> [ ] keep to 2 pages [ ] attach WI2026 one-pager + academic CV
