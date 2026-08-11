# PhD Project Outline — Template

**Author:** Alessandro Guidi · alexguidioff@gmail.com · alessandroguidi.site · linkedin.com/in/alessandroguidi1 · github.com/alexguidioff

> **Come si usa questo file.** Questa è la struttura (rubata all'outline di Maria Scetta per UZH,
> che è un ottimo modello: 2 pagine, asciutto, accademico) da replicare **una volta per professore**.
> Il 70% del testo è **generico** (uguale per tutti) e sta qui sotto già scritto. Il 30% è
> **professor-specific** ed è marcato con `[[...]]`: quello lo scrivi seguendo le istruzioni che
> trovi in `Professors.md`, sotto ciascun professore.
>
> ⚠️ **Regola di disclosure:** questo outline è OUTREACH. Contiene solo P0 (fatto) + P1 (flagship)
> e al massimo un accenno a P2. **Mai** P3/P4/P5, mai la north star, mai il piano azienda.
> ⚠️ **Lunghezza target:** 2 pagine. Se sfori, tagli dal generico, non dallo specifico.
> ⚠️ **Verifica** nome, titolo, gruppo, email e ogni paper citato sulla pagina ufficiale prima di inviare.

---

## Working title
`[[TITLE]]` — di default: **Value of Information for Investment Decisions under Uncertainty**.
Adatta il taglio al professore (es. per un metodologo → *"…: a Sequential Decision-Making Approach"*;
per un domain prof di finance → *"…in Venture Capital Diligence"*).

## Target institution
`[[INSTITUTION]]` — Università, dipartimento/gruppo, e **nome + titolo del professore** (verificato).
Esempio formato: *ETH Zurich, D-INFK — Optimization & Decision Intelligence group (Prof. Niao He)*.

---

## 1. Research context & focus
*(GENERICO — riusabile quasi identico per tutti)*

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
result also exposes the ceiling of a purely predictive approach, which motivates the shift from
*prediction* to *value of information*.

`[[CONTEXT_HOOK]]` — 1–2 frasi che agganciano il focus del gruppo del professore (vedi Professors.md).

## 2. Research questions
*(GENERICO il primo blocco, poi 1 sotto-domanda professor-specific)*

**Main question:** In investment decisions under uncertainty, which information acquisition — at
what cost — most improves decision quality?

- How can each decision be represented by its **observable public information state**: what was
  publicly knowable at time *t*, reconstructed point-in-time before the outcome is realised?
- How do we quantify the **marginal value** of acquiring an additional piece of information
  (a signal, a due-diligence step) relative to its cost?
- `[[RQ_SPECIFIC]]` — una domanda tarata sull'expertise del professore (es. per un metodologo:
  *"…as a sequential/active acquisition problem with regret guarantees?"*; per domain finance:
  *"…and which diligence steps do professional investors under- vs over-invest in?"*).

## 3. Theoretical framework
*(GENERICO + gancio teorico specifico)*

The project sits at the intersection of **decision theory under uncertainty** and **information
economics**, operationalised with modern ML. The core object is the *value of information*: the
expected improvement in decision quality from moving `Decision(state) → acquire info (cost c) →
state' → Decision(state')`. It draws on Bayesian experimental design / expected information gain,
active feature acquisition, and sequential decision-making under uncertainty. The methods exist;
their **application to private-market investment decisions is open**.

`[[THEORY_BRIDGE]]` — 2–3 frasi che collegano ESPLICITAMENTE il framework del professore (il suo
filone: active learning / Bayesian experimental design / optimization under uncertainty / RL /
interpretable ML / entrepreneurial finance) al costrutto di value of information. Cita 1 suo paper.

## 4. Methodology
*(GENERICO + eventuale metodo/dato specifico)*

Feasibility does **not** depend on proprietary data. The **observable public information state**
comes from a point-in-time reconstruction of public sources, so information unavailable at time *t*
is excluded. The real-data outcome is initially a weak, explicitly scoped SEC proxy; a manually
adjudicated public-evidence subset provides stronger empirical labels. **Synthetic ground truth**
comes only from the virtual-fund simulator and is used for counterfactual method validation. On top
of this I formalise value-of-information estimators and evaluate which acquisitions most reduce
decision uncertainty per unit cost, benchmarked against the WI2026 pipeline as a predictive baseline.

Year 1: formalisation, point-in-time dataset + simulator, P1 experiments. Year 2: P1 completion and
submission `[[+ P2_HINT]]`. Year 3–4: extension, writing, publications. `[[METHOD_SPECIFIC]]` —
metodo o risorsa specifica del gruppo (es. dataset/industry partner del prof di finance; toolbox di
ottimizzazione/RL del metodologo; setup di interpretability del prof di ML).

## 5. Expected contribution
*(GENERICO)*

The project contributes (i) a **formalisation of value of information for private-market decisions**,
(ii) a **reproducible point-in-time + simulator methodology** that makes the question testable
without proprietary data, and (iii) empirical evidence on which information is worth acquiring in
VC diligence. Scientifically, the contribution is domain-general: the same three questions apply
beyond venture capital (private equity, credit, M&A), which is what makes it a research line rather
than a single application. `[[CONTRIBUTION_SPECIFIC]]` — un contributo aggiuntivo che parla la lingua
del gruppo (metodologico / finanziario / sistemi informativi).

## 6. Fit with host institution
*(TUTTO professor-specific)*

`[[FIT]]` — perché QUESTO gruppo, in 3–5 frasi: il filone del professore, un paper recente, come il
progetto estende i suoi strumenti in un dominio nuovo, e (se vero e verificato) grant attivi /
posizioni RA aperte / accesso a dati o partner industriali. Questa è la sezione che il professore
legge per prima: dev'essere concreta e verificata.

## 7. Selected references
*(GENERICO il nucleo + 1–2 paper del professore)*

Core (verifica edizione/anno prima di inviare):
- Howard, R. A. (1966). *Information Value Theory.* IEEE Trans. SSC.
- Savage, L. J. (1954). *The Foundations of Statistics.*
- Lindley, D. V. (1956). *On a measure of the information provided by an experiment.* Ann. Math. Stat.
- Pearl, J. (2009). *Causality* (2nd ed.). Cambridge UP.
- Guidi, Rashid, Zhong (2026). *Can Non-Financial Signals Price Private Companies?* WI2026 Student Track.
- `[[REF_SPECIFIC_1]]`, `[[REF_SPECIFIC_2]]` — 1–2 paper del professore, citati correttamente.

---
*One-page WI2026 summary attached. Code and manuscript available on request.*
