# Reading Roadmap — Value of Information, Decision Intelligence e Private Markets

**Autore:** Alessandro Guidi  
**Aggiornato:** 22 luglio 2026  
**Obiettivo:** prepararsi a sviluppare una ricerca PhD su AI-supported information acquisition per decisioni strategiche nei private markets, colmando il gap tra entrepreneurial finance, decision theory, active information acquisition e organizzazione.

## Come usare questa roadmap

Non serve leggere tutto integralmente. L'obiettivo iniziale è saper:

1. formulare una decisione tramite azioni, stati incerti, probabilità e utilità;
2. distinguere information gain, prediction accuracy e decision value;
3. rappresentare l'acquisizione costosa e sequenziale di informazioni;
4. progettare una valutazione falsificabile senza look-ahead bias;
5. collegare il meccanismo algoritmico a organizational attention e human–AI collaboration;
6. spiegare perché i private markets sono un setting empirico interessante, non soltanto un'applicazione commerciale.

Le etichette usate sotto sono:

- **CORE:** indispensabile prima di discutere seriamente il progetto con un metodologo;
- **IMPORTANT:** necessario per costruire una tesi interdisciplinare credibile;
- **REFERENCE:** da consultare quando il design diventa più preciso;
- **STRETCH:** materiale matematicamente più impegnativo, da affrontare con supervisione.

---

## 1. Sequenza minima: le prime nove letture

Se il tempo è limitato, seguire quest'ordine.

### 1. Clemen & Reilly — *Making Hard Decisions with DecisionTools* — CORE

Introduzione accessibile alla decision analysis: decision trees, probabilità soggettive, utility, sensitivity analysis e value of information. È il punto di partenza più adatto a un profilo MiM perché costruisce il linguaggio concettuale senza partire da teoremi avanzati.

- [Scheda Harvard](https://repository.chds.hsph.harvard.edu/repository/2612/)
- [Scheda editore Cengage](https://nz.cengage.com/c/making-hard-decisions-with-decisiontools-3e-clemen-reilly/9780538797573)
- **Focus:** capitoli su uncertainty, utility, decision trees, sensitivity analysis e value of information.
- **Output personale:** modellare un caso `continue diligence / stop` con due acquisizioni informative, costi e payoff.

### 2. Kochenderfer, Wheeler & Wray — *Algorithms for Decision Making* — CORE

Testo moderno sulle decisioni sotto incertezza, con planning, MDP, POMDP e reinforcement learning. Non occorre leggerlo da copertina a copertina: serve per tradurre il progetto da intuizione manageriale a problema sequenziale formalizzato.

- [MIT Press](https://mitpress.mit.edu/9780262047012/algorithms-for-decision-making)
- [Repository e materiali ufficiali](https://github.com/algorithmsbooks/decisionmaking)
- **Focus:** probabilistic reasoning, sequential problems, MDP, POMDP e policy evaluation.
- **Output personale:** scrivere stato, azioni, osservazioni, transizioni, reward e stopping condition di P1.
### 3. Chaloner & Verdinelli — “Bayesian Experimental Design: A Review” — CORE

Review classica che presenta experimental design come decision problem: scegliere un esperimento massimizzando l'utilità attesa. È il ponte concettuale tra VoI classica e acquisizione attiva.

- [University of Minnesota repository](https://conservancy.umn.edu/items/5fb0f449-81b0-4783-b6a5-5c827aaad8bd)
- [Descrizione CMU](https://www.stat.cmu.edu/tr/tr599/tr599.html)
- **Focus:** expected utility of an experiment, prior/posterior, design criterion.
- **Non serve inizialmente:** padroneggiare ogni derivazione per modelli non lineari.

### 4. Rainforth et al. — “Modern Bayesian Experimental Design” — CORE

Survey moderna sugli approcci computazionali al Bayesian experimental design e sulle difficoltà pratiche di stimare expected information gain.

- [Testo HTML su arXiv](https://arxiv.org/html/2302.14545v2/)
- **Focus:** formulazione generale, EIG, nested estimation, amortized e policy-based design.
- **Domanda critica:** il progetto vuole ridurre incertezza su un parametro oppure migliorare una decisione? Non sono necessariamente la stessa cosa.

### 5. Javdani et al. — “Near Optimal Bayesian Active Learning for Decision Making” — CORE

È una delle letture più direttamente collegate alla tesi: l'obiettivo non è identificare perfettamente l'ipotesi vera, ma acquisire abbastanza informazione per scegliere la decisione corretta.

- [Pagina CMU](https://www.ri.cmu.edu/publications/near-optimal-bayesian-active-learning-for-decision-making-2/)
- [PDF arXiv](http://arxiv.org/pdf/1402.5886v1.pdf)
- **Focus:** decision regions, adaptive test selection e differenza tra uncertainty reduction e decision-oriented acquisition.
- **Output personale:** definire quali stati diversi conducono alla stessa decisione `continue/stop`.

### 6. Golovin & Krause — “Adaptive Submodularity” — IMPORTANT/STRETCH

Fondamento teorico per capire quando una policy greedy di acquisizione può essere vicina all'ottimo. È centrale per comprendere il tipo di contributo metodologico associato al gruppo di Andreas Krause.

- [Paper arXiv](https://arxiv.org/abs/1003.3967)
- **Focus iniziale:** intuizione dei diminishing returns adattivi, adaptive greedy e condizioni delle garanzie.
- **Non fare:** affermare che il problema VC è adaptive-submodular prima di averlo dimostrato.

### 7. Ma et al. — “EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE” — CORE

Esempio concreto di acquisizione dinamica di feature mancanti tramite expected information gain. Mostra come un sistema possa scegliere quale variabile osservare dopo, invece di usare sempre tutte le feature.

- [HTML arXiv](https://ar5iv.labs.arxiv.org/html/1809.11142)
- [OpenReview](https://openreview.net/forum?id=HJl0jiRqtX)
- **Focus:** partial VAE, arbitrary conditioning, acquisition function, confronto costo–qualità.
- **Critica da annotare:** EDDI massimizza informazione sui target; P1 dovrebbe massimizzare valore decisionale netto.

### 8. Gompers, Gornall, Kaplan & Strebulaev — “How Do Venture Capitalists Make Decisions?” — CORE

Base empirica per descrivere il processo VC: sourcing, selezione, valuation, deal structure, organizzazione interna e post-investment work. Serve a evitare di progettare una decisione astratta che non corrisponde alla pratica.

- [HBS](https://www.hbs.edu/faculty/Pages/item.aspx?num=51659)
- [Stanford GSB](http://www.gsb.stanford.edu/faculty-research/publications/how-do-venture-capitalists-make-decisions)
- [Versione SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2801385)
- **Output personale:** mappare ogni fase VC alle informazioni disponibili, ai costi, alle decisioni e agli attori coinvolti.

### 9. Fu & Taylor — “Due Diligence and the Allocation of Venture Capital” — CORE

È il vicino accademico più diretto alla research question P1. Il paper studia la due diligence VC come **costly learning** e analizza come la quantità di diligence si associ all'allocazione del capitale e alla variabilità della performance. I risultati riportati collegano una minore diligence a deal e mercati più caldi, investitori più occupati e maggiore distanza; una minore diligence è inoltre associata a performance più variabile.

- [Versione SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5014747)
- **Focus:** costruzione della misura di diligence, teoria di costly learning, unità di analisi, identificazione empirica, endogeneità e interpretazione degli outcome.
- **Distinzione da P1:** Fu–Taylor studiano principalmente **quanta** diligence viene svolta e come si collega ad allocazione e performance; P1 chiede **quale informazione** acquisire successivamente, condizionatamente all'information state corrente, al costo, al ritardo e all'impatto atteso sulla decisione.
- **Claim da evitare:** non sostenere più che nessuno abbia modellato la diligence VC come apprendimento costoso. La novelty potenziale riguarda la selezione sequenziale e decision-aware delle informazioni e lo stopping, non l'idea generale che la diligence riduca l'incertezza.
- **Output personale:** produrre una tabella `Fu–Taylor construct → P1 equivalent → overlap → incremental contribution → required evidence` e identificare almeno tre minacce all'identificazione che P1 deve affrontare.

---

## 2. Fondamenti quantitativi da colmare

### 2.1 Probabilità bayesiana e modelli scientifici

#### Richard McElreath — *Statistical Rethinking* e corso 2026 — CORE

È consigliato perché sviluppa intuizione bayesiana, generative models, causal assumptions, confounding e modelli gerarchici. Per la tesi è più utile imparare a esplicitare il data-generating process che applicare algoritmi ML senza una teoria causale.

- [Materiali ufficiali del corso 2026](https://github.com/rmcelreath/stat_rethinking_2026)
- **Focus:** probabilità, generative models, DAG, confounding, posterior prediction, multilevel models.
- **Applicazione:** disegnare un DAG che separi qualità latente, informazione osservata, scelta di diligence, selezione del deal e outcome.

#### Kevin Murphy — *Probabilistic Machine Learning* — REFERENCE

Testo più tecnico per probabilistic modelling e approximate inference. Da usare selettivamente quando serviranno modelli per dati mancanti e belief updating.

- Cercare sul [sito ufficiale ProbML](https://probml.github.io/pml-book/).
- **Focus:** Bayesian inference, latent-variable models, variational inference, sequential latent-state models.

### 2.2 Decision theory e utility

#### Howard & Abbas — *Foundations of Decision Analysis* — IMPORTANT

Approfondisce preference, utility, value of information e costruzione coerente dei modelli decisionali.

- Cercare tramite biblioteche universitarie o l'[editore Pearson](https://www.pearson.com/).
- **Focus:** value of perfect/sample information, risk attitude, utility elicitation e sensitivity.

#### Berger — *Statistical Decision Theory and Bayesian Analysis* — STRETCH

Testo classico e matematico. Non è una priorità iniziale, ma diventa utile se il paper deve produrre risultati teorici o una formalizzazione decision-theoretic rigorosa.

### 2.3 Sequential decisions

Dopo i capitoli MDP/POMDP di Kochenderfer, studiare:

- belief states;
- finite-horizon stopping;
- exploration versus exploitation;
- off-policy evaluation;
- contextual bandits;
- regret;
- partial observability.

Non partire dal deep reinforcement learning: per il primo paper, un modello semplice, interpretabile e falsificabile è probabilmente più utile.

---

## 3. Value of Information e acquisizione attiva

### 3.1 Distinzioni che devi saper spiegare

- **Information gain:** quanto un'osservazione riduce l'incertezza.
- **Value of information:** quanto l'osservazione migliora l'utilità della decisione.
- **Active learning:** quali esempi etichettare per migliorare un modello.
- **Active feature acquisition:** quali feature comprare/osservare per una specifica istanza.
- **Bayesian experimental design:** quale esperimento scegliere massimizzando una utility attesa.
- **Bayesian optimization:** quale punto valutare per trovare un optimum di una funzione costosa.
- **POMDP:** come scegliere azioni quando lo stato è solo parzialmente osservabile.

Per Private-Market-AI, il nucleo è più vicino a **decision-aware active feature acquisition / sequential VoI** che ad active learning standard.

### 3.2 Letture successive

#### “A Survey on Active Feature Acquisition Strategies” — IMPORTANT

Survey recente che unifica l'AFA tramite una formulazione POMDP e confronta famiglie di strategie.

- [Abstract arXiv](https://arxiv.org/abs/2502.11067v2)
- **Focus:** tassonomia, cost model, stopping, missingness, evaluation e distribution shift.

#### Saar-Tsechansky, Melville & Provost — “Active Feature-Value Acquisition” — IMPORTANT

Lavoro fondamentale in *Management Science* che tratta l'acquisizione incrementale e cost-effective delle feature.

- [INFORMS](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.1080.0952)
- **Perché importante:** collega direttamente machine learning, information value e management research.

#### Chen et al. — “Efficient Online Learning for Optimizing Value of Information” — IMPORTANT/STRETCH

Studia la selezione sequenziale di test costosi per arrivare a una decisione.

- [HTML arXiv](https://ar5iv.labs.arxiv.org/html/1703.05452)
- **Focus:** unknown test distributions, online learning, decision loss e test cost.

#### “Submodular Surrogates for Value of Information” — STRETCH

- [AAAI](https://aaai.org/papers/694-submodular-surrogates-for-value-of-information/)
- **Focus:** difficoltà computazionale della VoI non-myopic, surrogate objective e garanzie.

#### Chen et al. — “Near-optimal Bayesian Active Learning with Correlated and Noisy Tests” — STRETCH

- [PMLR](http://proceedings.mlr.press/v54/chen17b.html)
- **Focus:** test correlati e rumorosi, condizione particolarmente realistica nella due diligence.

---

## 4. Private markets ed empirical finance

### 4.1 Tykvová — letture prioritarie

#### “Venture Capital and Private Equity Financing: An Overview of Recent Literature and an Agenda for Future Research” — CORE

- [Springer](https://link.springer.com/10.1007/s11573-017-0874-4)
- [Versione SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3106933)
- **Obiettivo:** capire la mappa del campo, le domande legittime per entrepreneurial finance e come Tykvová struttura una research gap.
- **Nota:** la review copre letteratura fino alla sua data; va integrata con lavori recenti.

#### Brinster & Tykvová — connected VCs e strategic alliances — IMPORTANT

Il lavoro è direttamente collegato al risultato WI2026 sulle network/syndicate features. Cercare il paper tramite il titolo **“Connected VCs and Strategic Alliances: Evidence from Biotech Companies”** e il *Journal of Corporate Finance*.

- [Profilo editoriale con riferimenti alle pubblicazioni](https://www.journals.elsevier.com/global-finance-journal/editorial-board/tereza-tykvova-dr)
- **Domanda:** le network features rappresentano informazione, capacità dell'investitore, selezione o causalmente valore aggiunto?

#### Tykvová — legal framework e VC investment success — REFERENCE

- [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3078072)
- **Utilità:** eterogeneità istituzionale, cross-country design e cautela sui concetti di “success”.

### 4.2 Contesto VC indispensabile

#### Fu & Taylor — diligence as costly learning — CORE

Leggere integralmente **“Due Diligence and the Allocation of Venture Capital”** prima di formulare claim di novelty su VoI e diligence. È la base empirica più vicina per separare tre domande:

1. quanta diligence viene effettuata;
2. quali condizioni determinano intensità e costo della diligence;
3. quale specifica informazione conviene acquisire dopo e quando fermarsi.

P1 deve contribuire soprattutto alla terza domanda, collegandola esplicitamente alle prime due.

- [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5014747)

Oltre a Gompers et al. e Fu–Taylor, leggere selettivamente lavori su:

- screening versus selection;
- syndication;
- staged financing;
- due diligence;
- investment committee governance;
- selection bias e survivorship;
- post-investment treatment;
- fund incentives e limited attention.

Per ogni paper, compilare una tabella con: unità di analisi, decision time, informazione osservabile, trattamento/scelta, outcome, identificazione, leakage risk e dati richiesti.

---

## 5. Organizational attention, strategy e human–AI

Questa sezione è necessaria se vuoi coinvolgere SMI/von Krogh/Weiser o trasformare il progetto da algoritmo applicato a contributo organizzativo.

### 5.1 Ocasio — Attention-Based View — CORE per SMI

#### “Towards an Attention-Based View of the Firm”

La tesi centrale è che il comportamento organizzativo dipende da come strutture e canali distribuiscono l'attenzione dei decision-maker.

- [Wiley](https://onlinelibrary.wiley.com/doi/10.1002/(sici)1097-0266(199707)18:1+%3C187::aid-smj936%3E3.0.co;2-k)
- **Applicazione:** una recommendation VoI non aggiunge soltanto informazione; reindirizza attenzione, tempo e autorità.

#### Ocasio & Joseph — “The Attention-Based View of Great Strategies”

- [INFORMS](https://pubsonline.informs.org/doi/10.1287/stsc.2017.0042)
- **Applicazione:** collegare information acquisition alla formazione e implementazione dell'agenda strategica.

#### “Research Frontiers on the Attention-Based View of the Firm” — IMPORTANT

- [SAGE](https://journals.sagepub.com/doi/full/10.1177/1476127020985095)
- **Obiettivo:** capire le evoluzioni moderne della teoria e non fermarsi al paper del 1997.

### 5.2 AI e organizzazioni

#### Raisch & Krakowski — “Artificial Intelligence and Management: The Automation–Augmentation Paradox” — CORE

- [Academy of Management Review](https://journals.aom.org/doi/abs/10.5465/amr.2018.0072)
- [Versione open su Zenodo](https://zenodo.org/records/8338404)
- **Applicazione:** evitare il framing semplicistico “AI sostituisce oppure supporta”. Automazione e augmentation possono essere interdipendenti nel tempo e tra attività.

#### Krakowski, Luger & Raisch — “Artificial Intelligence and the Changing Sources of Competitive Advantage” — IMPORTANT

- [Versione CBS](https://research-api.cbs.dk/ws/portalfiles/portal/93816687/sebastian_krakowski_et_al_artificial_intelligence_publishersversion.pdf)
- **Applicazione:** collegare AI capability, complementarità organizzative e vantaggio competitivo.

#### “Organizational Decision-Making Structures in the Age of Artificial Intelligence” — IMPORTANT

Studiare la distinzione tra delegazione, sequenze human-to-AI/AI-to-human e aggregazione human–AI. Usare il titolo per reperire una copia istituzionale o tramite biblioteca.

#### “Human-Centered Artificial Intelligence: A Field Experiment” — REFERENCE

- [Management Science / INFORMS](https://pubsonline.informs.org/doi/10.1287/mnsc.2022.03849)
- **Focus:** come progettare e misurare una reale collaborazione human–AI, invece di assumere automaticamente un miglioramento.

### 5.3 Human reliance e decision quality

Cercare review e studi sperimentali su:

- algorithm aversion/appreciation;
- calibrated reliance;
- automation bias;
- selective adherence;
- second opinions;
- explanation effects;
- override ed escalation;
- process quality separata dall'outcome.

Per P1 non è ancora necessario trasformare tutto in un human-subject experiment. Queste letture servono a definire correttamente P3 e a non promettere claim organizzativi non misurati.

---

## 6. Autori e gruppi metodologici da seguire

### Andreas Krause — ETH Learning & Adaptive Systems

- [LAS Group](https://las.inf.ethz.ch/)
- Seguire lavori su active information acquisition, adaptive submodularity, Bayesian active learning e reliable decision-making.
- **Per il progetto:** è il riferimento concettuale più vicino alla scelta adattiva di test orientata alla decisione.

### Niao He — ETH Optimization & Decision Intelligence

- [ODI Group](https://odi.inf.ethz.ch/)
- Seguire optimization under uncertainty, reinforcement learning, probabilistic inference e data-driven decision-making.
- **Per il progetto:** utile se P1 diventa un problema metodologico generalizzabile e non soltanto un'applicazione VC.

### Wolfram Wiesemann — Imperial Analytics & Operations

- [Profilo Imperial](https://profiles.imperial.ac.uk/ww/about)
- Seguire robust optimization e organizational decision-making under uncertainty.
- **Per il progetto:** ponte naturale tra rigore OR e framing business.

### Tereza Tykvová — HSG Private Markets

- Seguire entrepreneurial finance, VC/PE, syndication, governance, exits e institutional heterogeneity.
- **Per il progetto:** supervisione di dominio, construct validity e publishability nel campo private markets.

---

## 7. Blog, corsi e risorse accessibili

I blog sono utili per intuizione, ma non sostituiscono i paper nelle citazioni.

### Distill / visual explanations

Usare spiegazioni visuali per probabilistic modelling, information theory e reinforcement learning quando disponibili; verificare sempre i concetti sui testi accademici.

### Stanford Human-Centered AI

- [Stanford HAI](https://hai.stanford.edu/)
- Utile per overview su human–AI decision systems e governance, soprattutto prima di passare ai paper.

### NBER Digest e Harvard/HBS summaries

- [NBER](https://www.nber.org/)
- [HBS Working Knowledge](https://www.library.hbs.edu/working-knowledge)
- Utili per una prima lettura della letteratura VC; leggere poi il paper originale.

### Statistical Rethinking lectures

- [Repository 2026](https://github.com/rmcelreath/stat_rethinking_2026)
- Migliore risorsa gratuita per costruire intuizione bayesiana e causale con rigore progressivo.

### Full Stack Deep Learning — REFERENCE

- [Full Stack Deep Learning](https://fullstackdeeplearning.com/)
- Utile più avanti per trasformare il prototipo in un sistema riproducibile; non è una priorità per la teoria VoI.

---

## 8. Piano di studio di 12 settimane

### Settimane 1–2 — Decision analysis

- Clemen & Reilly: uncertainty, utility, decision trees, sensitivity, VoI.
- Costruire un foglio o notebook con un esempio di diligence.
- Calcolare EVPI ed EVSI in un caso semplice.

**Deliverable:** due pagine con azioni, stati, payoff, probabilità, costo delle informazioni e decision rule.

### Settimane 3–4 — Bayesian foundations

- Statistical Rethinking: modelli generativi, Bayes, confounding e posterior predictive checks.
- Chaloner & Verdinelli: introduzione e framework decision-theoretic.

**Deliverable:** DAG del processo VC e modello probabilistico minimo dell'information state.

### Settimane 5–6 — Sequential decisions

- Kochenderfer: MDP/POMDP, belief state e policy.
- Formalizzare P1 come finite-horizon stopping problem.

**Deliverable:** specifica con `state`, `belief`, `action`, `observation`, `cost`, `transition`, `terminal utility`.

### Settimane 7–8 — Active acquisition

- Javdani et al.
- EDDI.
- Survey AFA.
- Leggere solo introduzione, formulation, experiments e limitations di adaptive submodularity.

**Deliverable:** tabella di almeno cinque baseline: acquire-all, acquire-none, cheapest-first, uncertainty-based, decision-aware VoI.

### Settimane 9–10 — Private-market construct validity

- Gompers et al.
- Fu & Taylor, con attenzione a costly learning, misura della diligence ed endogeneità.
- Review di Tykvová.
- Brinster & Tykvová.
- Audit del tuo dataset: cosa rappresenta davvero Form D e cosa non rappresenta.

**Deliverable:** matrice `construct → observable proxy → limitation → sensitivity check`, più una pagina che distingue `how much diligence` (Fu–Taylor) da `which information next` (P1).

### Settimane 11–12 — Organization e human–AI

- Ocasio 1997.
- Raisch & Krakowski.
- Un field experiment human–AI.
- Riscrivere la research question su due livelli: contributo metodologico e meccanismo organizzativo.

**Deliverable:** research memo di 3–4 pagine adatto a Tykvová + metodologo + SMI.

---

## 9. Template per prendere appunti sui paper

Per ogni lettura creare una nota con questo schema:

```markdown
# Autore, anno — Titolo

## Problema
Quale decisione o fenomeno studia?

## Unità di analisi e setting
Chi decide, quando e con quali informazioni?

## Formalizzazione
Stati, azioni, osservazioni, utility/loss, costi, orizzonte.

## Metodo
Modello, identificazione, algoritmo e assunzioni.

## Dati ed evaluation
Split, baseline, metriche, leakage, sensitivity e falsification.

## Contributo
Cosa sappiamo dopo che prima non sapevamo?

## Limiti
Quali assunzioni impediscono di trasferire direttamente il risultato?

## Collegamento a Private-Market-AI
Cosa posso riusare? Cosa devo modificare? Quale nuovo test emerge?

## Una domanda per l'autore
Una domanda specifica, non “cosa ne pensa della mia idea?”.
```

---

## 10. Cosa devi saper presentare a un metodologo

Prima di contattare Krause, He, Wiesemann o un altro metodologo, preparare risposte precise a:

1. Qual è la decisione terminale?
2. Qual è la utility della decisione e come viene identificata?
3. Quali informazioni possono essere acquisite?
4. Qual è il costo e il ritardo di ciascuna acquisizione?
5. Cosa viene osservato dopo l'acquisizione?
6. Quali dipendenze esistono tra i test?
7. Quando la policy deve fermarsi?
8. Qual è il baseline più forte?
9. Perché information gain non è sufficiente?
10. Come valuti la policy senza leakage?
11. Quale parte è un contributo metodologico generalizzabile?
12. Quale parte è un contributo empirico sui private markets?

Se queste risposte non sono ancora solide, la priorità non è trovare una superstar: è migliorare la formulazione.

---

## 11. Ordine degli acquisti

Se vuoi comprare soltanto due libri:

1. **Clemen & Reilly, *Making Hard Decisions*** — per costruire le fondamenta di decision analysis.
2. **Kochenderfer, Wheeler & Wray, *Algorithms for Decision Making*** — per la formalizzazione algoritmica e sequenziale.

Aggiungere *Statistical Rethinking* se vuoi un terzo testo e seguire parallelamente le lezioni gratuite. I paper accademici indicati sopra sono in larga parte disponibili tramite arXiv, repository istituzionali o accesso universitario.

---

## 12. Priorità finale

### Da leggere subito

1. Clemen & Reilly — sezioni VoI.
2. Gompers et al. — VC decision process.
3. Fu & Taylor — due diligence come costly learning e allocazione VC.
4. Javdani et al. — decision-oriented active learning.
5. EDDI.
6. Tykvová — review VC/PE.
7. Ocasio — attention-based view.
8. Raisch & Krakowski — automation–augmentation paradox.

### Da studiare nel trimestre

9. Kochenderfer — MDP/POMDP.
10. Chaloner & Verdinelli.
11. Modern Bayesian Experimental Design.
12. Survey Active Feature Acquisition.
13. Adaptive Submodularity.
14. Brinster & Tykvová.
15. Human-centered AI field experiment.

### Da tenere come riferimento avanzato

16. Howard & Abbas.
17. Murphy, *Probabilistic Machine Learning*.
18. Berger, *Statistical Decision Theory*.
19. Online VoI, noisy/correlated tests e submodular surrogates.

---

## Nota sulle fonti

I link sono stati verificati tramite ricerca online il 22 luglio 2026, privilegiando pagine ufficiali, editori, repository istituzionali, PMLR, SSRN e arXiv. Alcuni articoli possono richiedere accesso tramite biblioteca. Le descrizioni sono sintesi originali e il contenuto delle fonti online è stato riformulato per conformità alle restrizioni di licenza.
