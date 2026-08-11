# Documento di design — valutazione di sostenibilità di Private Market AI

## 1. Scopo e vincoli

Questo design definisce un metodo riproducibile, non un sistema software, per rispondere in italiano a cinque domande: (1) la tesi di ricerca è valida e realizzabile? (2) quali sono le prospettive PhD per tier e percorso? (3) esiste un mercato per un wedge ristretto? (4) quando avrebbe senso uno spin-off post-PhD? (5) quali risultati economici personali sono plausibili rispetto alle alternative?

L'analisi usa come fatti soltanto la richiesta originale e i file del repository. Le affermazioni esterne correnti non verificate, inclusi salari, numerosità di mercato, prezzi e disponibilità di posizioni, non diventano fatti né soglie decisionali. Tutti gli importi futuri sono scenari analitici, non promesse; il documento non costituisce consulenza finanziaria, fiscale o legale.

**Data di valutazione:** la data di esecuzione dell'assessment, registrata in formato ISO `YYYY-MM-DD`.  
**Unità monetaria predefinita:** CHF nominali alla Data di valutazione; ogni tabella deve dichiarare eventuali eccezioni.  
**Principio di conservazione:** `requirements.md` e `.config.kiro` restano invariati.

## 2. Architettura del metodo

La pipeline è deterministica e auditabile:

1. **Repository Snapshot**: elenco immutabile dei file letti, data, hash opzionale e locator.
2. **Claim Extractor manuale**: scompone il testo in Material Claim atomici.
3. **Evidence Register**: assegna una sola classe e collega fonti, conflitti e decisioni.
4. **Cinque moduli di valutazione**: ricerca, admissions, mercato, spin-off, earnings.
5. **Rule Engine tabellare**: applica soglie e precedenza `stop > pause > pivot > bridge > continue`.
6. **Validation Ledger**: ricalcola formule, cardinalità, classificazioni e tracciabilità.
7. **Italian Answer Renderer**: produce cinque risposte concise, condizionali e prive di garanzie.

Il flusso dati è `fonti → claim → evidenza → score/stage/scenari → regole → verdetti → risposta finale`. Nessun verdetto può citare direttamente prosa non registrata nell'Evidence Register.

## 3. Evidence Register

### 3.1 Schema obbligatorio

Ogni riga contiene: `Claim_ID`, `Claim_Text`, `Evidence_Classification` (esattamente una tra Documented_Fact, Assumption, Judgment, Unverified_Claim), `Source_Locator`, `Verification_Status`, `Confidence_Level`, `Strongest_Support`, `Strongest_Contradiction`, `Missing_Evidence`, `Negative_Evidence`, `Decision_Affected`, `Depends_On_Claim_IDs`, `As_Of_Date`.
### 3.2 Classificazione e controlli

- **Documented_Fact**: locator `file#heading` (o pagina/linea), stato `verified-in-repository`; non prova che una fonte esterna citata dal repository sia oggi corretta.
- **Assumption**: valore necessario al modello, con lower/base/upper, razionale e owner della verifica.
- **Judgment**: deve referenziare almeno un Documented_Fact e ogni Assumption utilizzata.
- **Unverified_Claim**: informazione esterna o time-sensitive senza verifica ufficiale nel repository; può alimentare sensibilità, mai una Decision Rule deterministica.

Conflitti restano in righe separate; un Judgment di riconciliazione cita entrambi, assegna confidenza e dichiara se cambia l'output. Per ciascuna Core Thesis si prepara un mini-dossier con miglior supporto, miglior contraddizione, evidenza mancante e evidenza negativa.

## 4. Modulo ricerca: scorecard e maturity model

### 4.1 Scorecard

Otto dimensioni hanno peso iniziale uguale (12,5%): novità, contributo metodologico, fattibilità esecutiva, fattibilità dati, dipendenza da partner, potenziale di pubblicazione, trasferibilità commerciale, costo opportunità. Ogni dimensione riceve un intero 1–5 con la definizione vincolante dei requisiti e almeno un Claim_ID favorevole e uno limitante/mancante. Il totale è:

`Research_Total = Σ(score_i × 0,125)`.

Il totale non sostituisce i blocker. Un blocker sistemico (per esempio construct validity del Simulator) limita il verdetto a `conditional` finché non è chiuso. Mapping iniziale: `strong` se totale ≥4,0 e nessun blocker maggiore; `conditional` se ≥3,0 oppure esiste un blocker risolvibile; `weak` se 2,0–2,99; `unsupported` se <2,0. Il report indica la variazione di score/evidenza necessaria per il verdetto adiacente.

### 4.2 Giudizio corrente, solo repository

Il repository supporta **conditional**, con confidenza Medium: P1 ha framing definito e prior-art interno favorevole, ma non risultano studio P1 eseguito, accesso buyer/fund verificato o validazione esterna del Simulator. Il lavoro fondativo è riportato come tesi completata e WI2026 Student Track accettato; ciò è un segnale utile ma non equivale a record top-venue. Il prior-art scan è evidenza interna di ricognizione, non verifica bibliografica indipendente.

### 4.3 Evidence Maturity

La rubrica è M0 concetto; M1 design specificato; M2 dati e accesso confermati; M3 analisi/working paper; M4 accettato, pubblicato o replicato. Assegnazione preliminare da validare nel Register:

| Studio | Maturità corrente | Criterio repository | Prossimo criterio non soddisfatto |
|---|---:|---|---|
| Valutazione startup fondativa | M4 (accepted branch) | `papers/README.md` riporta WI2026 Student Track Accepted | pubblicazione/replica indipendente non documentata |
| P1 Value of Information | M1 | domanda, metodo e piano in `Research_Agenda.md` | M2: dati/accesso operativo e protocollo confermati |
| P2 Decision Quality | M1 | design e dipendenze specificati | M2: label/accesso o protocollo operativo confermato |
| P3 Human-AI committee | M1 | domanda e metodo delineati | M2: soggetti/partner e protocollo confermati |
| P4 Gaming robustness | M0 | continuazione descritta | M1: design completo e identificazione |
| P5 Portfolio VoI | M0 | continuazione descritta | M1: design completo e benchmark |

Per P1/P2/P5 il Simulator è dipendenza sistemica: anno 1 richiede soglie preregistrate di stylized-fact matching, calibrazione PiT, robustness/ablation e multi-world recovery. Fallimento → pausa delle generalizzazioni simulator-dependent e cascata Plan B descritta in `Threats_to_Validity.md`. P3 registra accesso a soggetti e decision logs, deadline e fallback vignette/synthetic-first.

Almeno tre condizioni di inferiorità rispetto a un'agenda alternativa: (a) P1 non supera i baseline su Net Decision Value; (b) Simulator non supera recovery/external-validity preregistrate entro anno 1; (c) nessun percorso dati riproducibile raggiunge M2 entro la deadline; (d) un nearest neighbor verificato elimina il contributo differenziale.

## 5. Modulo admissions: matrice tier × route

### 5.1 Matrice a sei celle

Ogni riga valuta nove fattori su scala 1–5: pubblicazioni, referenze accademiche, preparazione quantitativa/CS, profondità metodi, supervisor fit, maturità proposta, funded-seat availability, concorrenza e (separatamente) evidenza di engagement. La WI2026 è descritta con venue, Student Track, review status se documentato, posizione autore e acceptance; campi non documentati restano Unknown.

Intervalli preliminari, onesti e non predittivi, basati unicamente sul repository:

| Tier | Direct PhD | Bridge | Confidenza e ragione |
|---|---|---|---|
| A aspirational methods-led | Very Low [0,10%) | Low [10,25%) | Low: fit tematico, ma engagement/funded seat/metodi profondi non verificati |
| B strong-fit interdisciplinary | Low [10,25%) | Plausible [25,50%) | Medium-Low: diversi fit documentati; seat e sponsorship non verificati |
| C broader applied Swiss | Plausible [25,50%) | More Likely Than Not [50,70%) | Low: maggiore ampiezza ipotizzata, ma lista/seat attuali incompleti |

Questi non sono tassi statistici. Ogni cella deve elencare supporti, blocker e osservazioni datate per passare all'intervallo adiacente. Per ogni Bridge Route si riportano tre intervalli condizionali successivi: zero, uno, almeno due esiti verificati fra paid research work, publication submission, supervisor sponsorship; il passaggio non è automatico e richiede rivalutazione dei nove fattori.

### 5.2 Confronto e regole

Bridge e Direct sono confrontati su research signal, mesi trascorsi, gross Cash Earnings (Unverified/Assumption finché non ufficiali) e option value. Regole admissions:

- `apply now`: proposta M1+, almeno una sponsorship/engagement sostanziale e seat verificato → continue.
- `bridge first`: buon fit ma manca almeno uno tra metodi, sponsorship, seat → bridge.
- `broaden`: meno di 3 target con fit ≥4/5 o nessun seat verificato in un tier alla review → pivot.
- `stop campaign`: due cicli completi senza inviti/applicazioni richieste e con alternativa dominante → stop.
- Regola vincolante: zero interesse sostanziale dopo ≥20 contatti tailored, ≥2 tier, entro 12 settimane → pivot di pitch, target set o route.

## 6. Modulo mercato: narrow-wedge bottom-up test

Il wedge viene valutato prima di qualsiasi Copilot/Operating System: **supporto Value of Information alla diligence live di VC/growth**. Buyer: Partner, Head of Investments o Head of Due Diligence. Workflow: scegliere quale informazione mancante acquisire sotto budget. Stage: VC/growth (da scegliere una sola fascia nel protocollo). Geografia: Svizzera + un perimetro europeo esplicito. Evento: decisione go/no-go o term-sheet su un deal live.

La baseline per buyer registra strumenti, ruoli analista, elapsed time, labor hours e direct expenditure. Tutti i valori correnti assenti dal repository sono Assumption o Unverified_Claim.

### 6.1 Test bottom-up

Input con unità e bound: workflow/anno (`V`), ore/decisione (`H`), costo loaded/ora (`C`), delay/error cost (`D`), buyer addressable (`N`), ACV (`P`).

- `Current_Annual_Cost = V × (H × C + D)`
- `Reachable_Market_low = N_low × P_low`
- `Reachable_Market_high = N_high × P_high`

Il test non usa TAM top-down. `N` richiede lista deduplicata; `P` richiede buyer behavior prima di essere considerato osservato. Stage corrente da repository: **B0 No Buyer Evidence**, perché non è documentato comportamento qualificato; i claim di willingness to pay in `Startup_Ideas.md` sono Assumption. B1–B3 provano problema/soluzione, B4–B6 soltanto willingness to pay.

La Competition Set copre database, tooling interno, consulenti, general AI, AI-DD vendor e non-consumo, confrontati su data, workflow, model performance, integration, trust e price. Ogni categoria dati (`datasets/README.md`: proprietary, freemium/API, public/open, academic, restricted) riceve almeno una barriera: licenza/redistribuzione, coverage/PiT, identity resolution, accesso o ToS. Privacy, riservatezza, financial-services, explainability, governance e liability sono issue analitiche per fund, family office, private bank e wealth manager, non conclusioni legali.

Verdetti separati: problema, budget owner, Buyer Stage, reachable market, differentiation, deployability. Dopo ≥10 interviste, meno di 5 buyer che mettono il workflow nella top-3 → pivot/stop. Dopo tre offerte senza denaro o procurement documentato → stage massimo B3. Conversione paid pilot <1/3 dopo ≥6 proposte → pivot buyer-workflow-price.

## 7. Otto gate spin-off

Ogni gate ha `metric | operator | threshold | deadline | evidence source | current status | pass output | fail output`. Stato corrente prudenziale: non verificato/non passato finché manca evidenza comportamentale o documentale.

| Gate | Soglia minima | Fallimento |
|---|---|---|
| Problem | interviste ≥15 e top-3 count ≥10 entro decisione | pivot |
| Solution | design-partner commitments ≥5, ciascuno con workflow/data/owner/metric | pivot |
| Payment | paid pilots ≥3 AND contracted ARR ≥CHF 50k | pause |
| Retention | renewals/annual contracts ≥2 entro 12 mesi dal primo pilot | stop |
| Data rights | diritti collection/processing/model/commercial per ogni fonte | pause |
| Regulatory feasibility | assessment datato completo, owner e deadline per blocker | pause |
| Technical performance | improvement ≥25% su metrica buyer-approved in ≥2 pilot | pivot |
| Founder commitment | runway firmato 12 mesi e ≥40h/settimana entro 30 giorni | stop |

Full-time formation è `continue` solo se tutti e otto passano. IP universitario aggiunge licensing terms, founder ownership terms e commercialization permission scritti al gate data rights. Pubblicazioni e novità non sostituiscono alcun gate.
