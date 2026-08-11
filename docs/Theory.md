# Investment Intelligence Theory
## The scientific core of Decision Intelligence for Private Capital Markets

**Author:** Alessandro Guidi — v0.1
**Level:** 🧭 **[NORTH STAR — private]** — this is the *why* of the lab. Do not pitch it early.

> **Grand Challenge:** How do investors make decisions under extreme uncertainty — and how can
> AI represent, augment, and improve that process?

> **Working definition (the flag).**
> *Decision Intelligence is the study of how artificial systems can represent, acquire, reason over,
> and communicate information that improves human decision quality under uncertainty.*
> This definition — not any specific model — is what the programme plants a flag on, the way
> "representation learning" or "self-supervised learning" name a field rather than a technique.

Most labs build algorithms. This document sketches a **theory** — one that stays valid even as
the underlying models change (LLMs today, something else tomorrow). Venture capital is the first
domain; the theory is meant to generalize to M&A, corporate development, drug-discovery
investing, sovereign wealth, infrastructure, and climate investing.

---

## 0. The meta-framework (the spine every paper sits on)

Every paper in the agenda is an instance of a single loop:

```
Representation → Information → Reasoning → Decision → Outcome → Learning
        ↑______________________________________________________|
```

- **Representation** — how the world (company, ecosystem) is modelled (the point-in-time
  *information state*, §2.6a).
- **Information** — which signals to *acquire*, at what cost → **P1, Value of Information**.
- **Reasoning** — how evidence combines into a judgment (reasoning objects; agents).
- **Decision** — the committed choice, with alternatives and rationale (Decision Graph).
- **Outcome** — what materialised.
- **Learning** — updating the representation/policy; and evaluating the *decision*, not just the
  outcome → **P2, Decision Quality**. Humans and AI share this loop → **P3, Human-AI committees**.

The trilogy (P1→P2→P3) walks this loop: *acquire information → evaluate the decision → decide
together*. This is the theory that keeps the papers from being disconnected.

---

## 1. Why a theory (not just models)

A field matures when it has shared *constructs*, not just tools. Medicine has disease models;
economics has utility and equilibrium. Investing under uncertainty has spreadsheets and
folklore. The ambition here is to define the constructs precisely enough to be measured,
modeled, and taught — the difference between *applying AI to finance* and *defining a discipline*.

---

## 2. Core constructs (to be formalized)

### 2.1 What is a decision?
A decision is a commitment of resources under uncertainty, chosen from alternatives, justified
by information, producing an outcome. This is richer than a prediction: it has **alternatives**,
**rationale**, **reversibility**, and **cost of being wrong**.

### 2.2 What is a good decision?
Crucially: **a good decision ≠ a good outcome.** In high-variance domains (VC), good decisions
can have bad outcomes and vice versa. The theory must evaluate *process quality* (was the
reasoning sound given what was knowable?), not just realized returns.

### 2.3 What is uncertainty?
Distinguish:
- **Aleatoric** — irreducible randomness (the world is noisy).
- **Epistemic** — reducible by more information (we simply don't know yet).
The value of due diligence is largely about *converting epistemic uncertainty into knowledge* —
and knowing when that conversion is worth its cost.

### 2.4 What is a signal?
A signal is information that shifts belief about a latent quality (team, market, product).
Signals have **strength**, **cost**, **timeliness**, **correlation** with other signals, and
**gameability**. A theory of signals asks how they *combine* — not just which correlate with success.

### 2.5 How do signals combine?
The central modeling question. Naive addition is wrong (signals are correlated, redundant,
sometimes contradictory). This connects to information theory, Bayesian updating, and causal
structure.

### 2.6 The Information State and formal P1 problem
A decision uses an **observable/public information state** `I_t`: information defensibly available by
decision time `t`, not all data that later exists and not the investor's unobserved private knowledge.
Let `theta` be the latent state, `D` the action set, `A` the available information-acquisition actions,
`X_a` the observation returned by action `a`, `U(d, theta)` utility and `C(a)` total acquisition cost.

```text
BaseValue(I_t) = max_d E[U(d, theta) | I_t]
NDV(a | I_t)  = E[max_d E[U(d, theta) | I_t, X_a] | I_t] - C(a)
NetVoI(a|I_t) = NDV(a | I_t) - BaseValue(I_t)
a*             = argmax over {none union A} of NDV(a | I_t)
```

`C(a)` includes direct spend, analyst time, delay and strategic/opportunity cost. `none` has zero cost.
The policy abstains from acquisition when all NetVoI values are non-positive. P1 fixes one unit of
analysis—one company at one decision time—and evaluates the final action by Net Decision Value, not
by uncertainty reduction alone. See `protocols/P1_VoI_Protocol.md`.

### 2.7 Separate objects in the decision loop
- **InformationState:** point-in-time observations with provenance and availability time.
- **BeliefState:** calibrated beliefs about latent states/outcomes; this is not yet a decision.
- **AcquisitionAction:** obtainable information, observation model, cost, delay and process effect.
- **UtilityModel:** buyer/fund preferences, payoff, risk and constraints.
- **DecisionRecord:** alternatives, chosen action, expected utility, rationale and responsible actor.
- **OutcomeRecord:** later events, censoring and realized payoff, linked without rewriting prior state.

This separation prevents P10/P50/P90 predictions from being mislabeled as decisions and supports a
clean transition from P1 information acquisition to P2 process-quality evaluation.

---

## 3. Prediction → Causality

Today's work (the thesis) is predictive: *which signals predict valuation?*
The deeper question is causal: *which signals **cause** good outcomes?*

- Predictive models break under distribution shift and are gameable (founders optimize the
  proxy, not the substance).
- Causal models support **intervention** ("if this startup hired senior sales, would outcomes
  improve?") and **policy** ("what should a fund do?").
- Opens the door to causal inference, decision science, and counterfactual reasoning.

---

## 4. Uncertainty as first-class output

The lab is *obsessed with uncertainty*. The unit of output is never a number; it is a
**decision object**:

```
Valuation
  ├── P10 / P50 / P90        (distribution, not point)
  ├── confidence             (how sure, and why)
  ├── reasons                (which signals drove it)
  ├── missing information    (what we don't know)
  └── value of information   (what it's worth to find out)
```

This is both better science and a better product (see `Startup_Ideas.md`).

---

## 5. Human-AI decision-making

The future is not "AI that invests". It is **AI that participates** in the investment committee.
Research questions:
- How does AI participation change the *decision* (not just the information)?
- When do humans trust the AI? When do they (rightly or wrongly) override it?
- How to design AI contributions that improve process quality without anchoring or automation bias?

---

## 6. The epistemological question

Deliberately kept open, because it will matter:

> **Can an AI make investment decisions — or only support them?**

This is not rhetorical fluff. It determines product boundaries, liability, governance, and how
much authority a system should be given. A serious lab should have a position and revisit it.

---

## 7. How the theory maps to the trilogy (+ continuations)

| Construct | Becomes | Paper |
|---|---|---|
| Information state + value of information | Value of Information for VC diligence | **P1 (flagship)** |
| Decision quality (process vs. outcome) | Decision Quality for VC | **P2** |
| Human-AI decision-making | Human-AI investment committees | **P3** |
| Signal gameability | Gaming-robustness (strategic classification) | P4 (continuation) |
| Value of information at fund scale | Portfolio-level VoI | P5 (continuation) |
| Representation / knowledge graph | *foundation absorbed inside P1* | — |

---

## 8. Open theoretical questions
- A formal definition of "decision quality" usable as an ML training/eval target?
- How to represent *value of information* tractably in a live deal?
- Can process-quality be learned from data where only outcomes are observed?
- What is the right unit of analysis — the deal, the decision, or the fund?

---

## 9. Parked future options (deliberately NOT in the agenda yet)
Recorded so they are not lost, but **not adopted** — adding them now would break the focus the
trilogy depends on ("an excellent first paper, not five mediocre ideas").
- **Investment Memory / episodic memory.** A fund accumulates memory; each startup seen reshapes how
  the next is judged. An AI system arguably needs episodic memory, not just retrieval. Possible
  future paper (P6+), or a mechanism inside the platform — revisit after the trilogy.
- **Lab name "Computational Investment Science" / "Computational Decision Science".** A more durable
  banner than "AI for Private Markets" for a 10-year career. Attractive, but the mission was just
  fixed on Decision Intelligence; renaming now would be exactly the oscillation to avoid. Keep as a
  *future naming option*, not a change.
- **Portfolio VoI as Operations Research.** P5 may grow into a resource-allocation-under-uncertainty
  line in its own right — likely the first substantial post-PhD direction.
