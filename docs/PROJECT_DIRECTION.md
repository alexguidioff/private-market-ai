# Private-Market-AI — Direzione, stato e prossimi passi

**Aggiornato:** 2026-07-21  
**Ruolo:** documento canonico per spiegare cosa stiamo costruendo, perché e verso quale risultato.  
**Fonti operative:** `../programme.yaml`, `STATUS_MEMO.md`, `Research_Agenda.md`.

## 1. Decisione strategica

L'MVP attuale è prima di tutto un **research/evidence MVP** per P1 — Value of Information for VC
Diligence. Serve a dimostrare, in modo falsificabile e riproducibile, se una policy che decide quale
informazione acquisire produce più valore decisionale del costo sostenuto.

Non è ancora un SaaS, un Due Diligence Copilot completo o un prodotto pronto per raccogliere venture
capital. Può però diventare il nucleo scientifico e tecnico di un futuro prodotto, se la ricerca e la
buyer discovery superano gate separati.

La sequenza scelta è:

```text
research evidence → paper/collaborazione/grant → buyer validation → product MVP → eventuale startup
```

Un PhD è un possibile veicolo per sviluppare questa agenda, non il fine esclusivo. Allo stesso modo,
una startup è un possibile esito della ricerca, non una conclusione già dimostrata.

## 2. Il problema che stiamo cercando di risolvere

Gli strumenti per investitori privati tendono a predire un outcome o produrre uno score. La domanda
qui è diversa:

> Dato ciò che è pubblicamente conoscibile in un preciso momento, quale informazione conviene
> acquisire prima di decidere, considerando costo, tempo, incertezza e utilità della decisione?

Nel vertical slice P1 la decisione è volutamente stretta: per una società e un tempo decisionale
fisso, scegliere se acquisire un ulteriore blocco informativo prima di `continue_diligence` o `stop`.
La metrica primaria è **Net Decision Value (NDV)**, non accuracy.

## 3. Dove vogliamo arrivare

### Risultato scientifico vicino

Dimostrare o falsificare che una policy cost-aware di acquisizione delle informazioni supera baseline
semplici su un test temporale bloccato, con dati point-in-time, costi espliciti e analisi di
sensibilità. Il risultato deve essere pubblicabile anche se la policy non vince: in quel caso si
riporta il fallimento e si restringe la tesi.

### Risultato accademico

Usare P1 come paper di ingresso per una collaborazione con un professore o un gruppo, un ruolo da
Research Engineer/Assistant, un grant o eventualmente un PhD. L'agenda più ampia prosegue verso
Decision Quality e Human-AI Investment Committees.

### Possibile risultato commerciale

Trasformare il principio di VoI in un assistente di diligence che non dica soltanto “investi/non
investire”, ma:

- mostri cosa manca;
- proponga la prossima domanda o verifica;
- stimi quanto quella verifica può cambiare la decisione;
- confronti il valore atteso dell'informazione con costo e ritardo;
- produca un decision record verificabile.

Questa è una product hypothesis, non ancora product-market fit.


## 4. Cosa abbiamo fatto

### Fondazione concettuale

- Posizionato il progetto come **Decision Intelligence**, non semplice outcome prediction.
- Formalizzato Information State, Belief State, Acquisition Action, Utility Model, Decision Record,
  Value of Information e Net Decision Value.
- Separato qualità della predizione, qualità della decisione e outcome realizzato.
- Definito un protocollo P1 falsificabile, baseline, split temporali e leakage controls.

### Validazione sintetica

- Costruito un ambiente multi-world con segnali nascosti, costi e oracle.
- Implementata una policy appresa cost-aware e confrontata con baseline semplici.
- Il risultato è **synthetic-conditional**: alcune configurazioni passano e altre no.
- Questo valida parte del laboratorio e del metodo, non dimostra efficacia nei private markets.

### Dataset reale open-only

- Scaricati e normalizzati 62 trimestri SEC Form D, dal 2008 Q1 al 2023 Q2.
- Costruito un archivio con 594.422 filing e 274.947 issuer.
- Creato un panel technology-related e una coorte model-ready di 12.381 issuer unici.
- Implementate feature point-in-time e split train 2016–2018, validation 2019, test 2020.
- Corretto il parsing delle date SEC e superati i controlli temporali e di leakage disponibili.

### Limite della label reso esplicito

La label corrente significa soltanto “successivo notice Form D entro 18 mesi”. Non significa Series A,
round istituzionale, fundraising riuscito, salute economica o successo della società. Il positive rate
non è un tasso di successo.

### Piano per label più forti

- Definito un protocollo open-only basato su evidenze pubbliche.
- Creato uno schema strutturato per label, fonti, date, confidenza, censura e adjudication.
- Generata una review queue deterministica di 200 issuer unici, bilanciata 100/100 sulla weak label SEC.
- Separati `no_public_evidence`, `unknown` e vero evento positivo.
- Chiarito che public point-in-time data sono osservazioni/proxy; solo il simulatore ha synthetic
  ground truth per costruzione.

## 5. Stato attuale

| Componente | Stato | Cosa dimostra |
|---|---|---|
| Teoria e protocollo P1 | pronto per iterazione | domanda e test sono formalizzati |
| Harness sintetico | condizionale | il metodo può funzionare in alcuni mondi sintetici |
| SEC real-data core | costruito e auditato | P1 è tecnicamente eseguibile su dati reali open-only |
| Label SEC | weak proxy | un successivo filing, non successo VC |
| Gold-label pilot | model-reviewed, owner-accepted | 20 casi: 9 positive, 4 no-public-evidence, 7 unknown; non human gold |
| Publication-grade gold benchmark | opzionale/non completato | necessario solo per claim forti su round VC |
| Real-data baseline | completata, EXP-001B | ROC-AUC test 0,6485; utility dipende dalla matrice |
| Acquisition block SEC issuer history | testato, VoI fail | predictive lift; cost-aware 0/15 gate pass |
| SEC Form C disclosure | auditato, coverage fail | exact CIK/PiT pass; 52/2.369 development issuer, sotto il gate minimo di 100 |
| SBIR/STTR award block | auditato, data gate fail | 622/10.550 candidate match; manca first-publication time difendibile |
| USPTO/PatentsView pre-grant | access-gated | schema pubblico; ODP richiede account/API key personale; nessuna estrazione |
| Future temporal baseline | completata, EXP-001D | 2021→2022 company-disjoint: full ROC-AUC 0,6551; utility assumption-bound |
| Future locked test | chiuso | 914 casi 2023, outcome mascherati e non ispezionati |
| OpenAlex founder research | bloccato | mancano founder identities revisionate |
| Buyer evidence | differita/B0 | in attesa di PhD o partner istituzionali; nessuna utility buyer-realistic |
| Startup product | non costruito | — |

## 6. Cosa dobbiamo fare adesso

### Gate 1 — Pilot gold-label su 20 issuer

**Eseguito come pilot AI-assisted a doppia revisione.** Il campione cieco contiene 10 weak-positive
e 10 weak-negative, distribuiti 4 per anno tra 2016 e 2020. Le revisioni hanno raggiunto 75% di
accordo esatto. Il project owner ha accettato le decisioni conservative del modello senza ulteriore
source review umana: 9 `positive`, 4 `no_public_evidence` e 7 `unknown` per il Layer A. I disaccordi
originali restano conservati. Report: `../datasets/P1_GOLD_PILOT_REPORT.md`.

Il pilot è utilizzabile per sviluppo metodologico e sensitivity analysis, ma non è un gold benchmark
umano publication-grade. Layer B resta non validato e non deve essere esteso automaticamente.

### Gate 2 — Baseline reale e primo acquisition experiment

**Completati.** EXP-001B mostra segnale predittivo per la weak label SEC, ma il vantaggio decisionale
dipende dalla matrice di utilità. EXP-001C mostra un piccolo lift predittivo dalla storia SEC, mentre
la policy cost-aware non supera il gate in nessuno dei 15 scenari. Il test 2020 è ormai ripetutamente
ispezionato: ogni ulteriore uso è esplorativo.

### Gate 3 — Utilità e costi senza accesso ai buyer

Le interviste sono differite finché un PhD o un partner istituzionale non dà accesso a practitioner
qualificati. Nel frattempo lo sviluppo può continuare con una griglia low/base/high completa,
dichiarata prima dei risultati e mai ottimizzata sul test. Ogni risultato rimane **assumption-bound**:
può mostrare robustezza metodologica, non che i payoff rappresentino l'economia reale di un VC.

### Gate 4 — Secondo blocco informativo

L'audit SBIR/STTR su train/validation ha trovato 622/10.550 candidate match exact-name+state, ma ha
fallito il gate point-in-time. USPTO/PatentsView è access-gated: documentazione e schema sono pubblici,
ma metadata/file ODP richiedono account e API key personali. Non forzare mirror o matching non
verificabili. Possiamo continuare source engineering e preparare l'adapter senza credenziali.

### Gate 5 — Nuova valutazione

È pronta una coorte company-disjoint: 2.369 development 2021, 2.243 validation 2022 e 914 locked test
2023, con zero overlap CIK rispetto al 2016–2020. EXP-001D ha congelato la baseline anchor+SEC-history:
sul 2022 raggiunge ROC-AUC 0,6551 e log loss 0,4681; il vantaggio di utility è robusto soltanto nella
matrice balanced assunta. Non è un test VoI. Le label 2023 restano isolate in un vault locale con hash.
Il prossimo blocco deve essere sviluppato sul 2021 e validato una sola volta sul 2022 senza ulteriori
tuning; il vault resta chiuso fino al freeze completo del protocollo.

### Traccia commerciale parallela, differita

Buyer discovery, utility elicitation e commercial validation ripartono quando esiste accesso tramite
PhD o partner. Fino ad allora non costruire un SaaS completo e non inferire product-market fit da dati
SEC o risultati metodologici.

## 7. PhD o startup?

### Risposta breve

**Oggi: MVP scientifico per P1 e per aprire una traiettoria accademica. Domani, se validato: possibile
nucleo di una startup.**

### Perché non è ancora un fundraising MVP

Per raccogliere capitale per una startup servirebbero almeno:

- un buyer e un workflow molto specifici;
- evidenza che il problema sia urgente e pagato;
- un'interfaccia utilizzabile su casi reali;
- dati/integrazioni affidabili nel contesto del cliente;
- pilot o design partner;
- una tesi credibile su distribuzione, compliance e moat.

Oggi abbiamo un metodo, un protocollo, dati open e una pipeline di validazione: sono ottimi asset per
paper, grant e conversazioni con partner, ma non equivalgono a traction.

### Decision rule

- Se P1 produce evidenza forte ma le interviste non mostrano willingness to pay: proseguire come
  ricerca, paper e grant.
- Se le interviste mostrano dolore ma P1 non supera le baseline: non vendere il claim VoI; cercare un
  wedge prodotto più semplice.
- Se passano sia il gate scientifico sia quello buyer: costruire un product MVP con 1–2 design partner
  e valutare grant/spin-off/pre-seed.
- Se il percorso PhD/collaborazione non si concretizza dopo un ciclo completo di candidature e
  outreach, attivare il percorso prodotto. Il rifiuto accademico è un trigger operativo, **non** una
  prova di domanda commerciale: il prodotto deve comunque superare i propri gate cliente.

## 8. Percorso alternativo: prodotto autonomo

### Wedge commerciale iniziale

Non costruire subito un “Bloomberg per i private markets”. Il primo prodotto deve risolvere un solo
job-to-be-done:

> Aiutare un investment professional, durante screening o early diligence, a identificare le lacune
> informative che possono cambiare la decisione e a scegliere la prossima verifica più utile rispetto
> a costo e tempo.

Input minimo: deck o investment memo, dati dichiarati dal cliente e poche fonti pubbliche verificabili.
Output minimo: information-state snapshot, missing/contradictory evidence, 3–5 prossime verifiche
prioritizzate, motivazione, costo/tempo stimato e decision record esportabile. Non promettere una
previsione di successo o una decisione automatica d'investimento.

### Cosa manca per il commercial MVP

| Area | Requisito minimo prima di chiamarlo MVP commerciale |
|---|---|
| Cliente | un ICP stretto, inizialmente small VC/CVC/family office con screening frequente |
| Problema | almeno 10 interviste; 5 conferme dello stesso workflow doloroso |
| Design partner | 1–2 partner disposti a provare casi reali e fornire feedback strutturato |
| Workflow | scegliere un punto preciso: screening-to-first-meeting oppure early-DD-to-partner-review |
| Esperienza | upload/input guidato, report revisionabile, fonti cliccabili, export e feedback |
| Motore | gap detection e ranking delle verifiche; VoI avanzato entra solo quando validato |
| Dati | fonti legittime, provenance, freshness, entity matching e gestione degli unknown |
| Fiducia | ogni claim collegato alla fonte; separazione tra fatti, inferenze e dati mancanti |
| Privacy | retention esplicita, cancellazione, access control, nessun training sui documenti senza consenso |
| Sicurezza | cifratura, secret management, logging minimo e isolamento dei documenti cliente |
| Compliance | disclaimer, human-in-the-loop e verifica legale prima di trattare dati sensibili o dare raccomandazioni |
| Valutazione | tempo risparmiato, verifiche accettate, cambi di decisione documentati e false-confidence rate |
| Business | willingness to pilot, buyer, budget, prezzo ipotetico e canale di acquisizione |
| Operazioni | supporto manuale sostenibile e costo per analisi noto |

### Quando integrarlo

**Adesso — discovery, non software di produzione.** In parallelo al pilot gold-label, condurre le 10
interviste e mostrare mockup/report statici. Non deviare il lavoro P1 verso frontend, agenti o
infrastruttura multi-tenant.

**Dopo il pilot gold-label su 20 issuer — concierge prototype.** Se almeno 5 intervistati confermano
lo stesso problema e 1–2 accettano di portare casi reali, costruire un servizio assistito: il sistema
prepara il report, ma ricerca e controllo restano parzialmente manuali. Questo testa utilità e workflow
prima dell'automazione.

**Dopo 5–10 casi reali — commercial MVP.** Automatizzare soltanto le parti ripetitive dimostrate:
ingestion, evidence extraction, gap list, ranking, provenance, export e feedback. Integrare il motore
VoI sperimentale come decision support con etichetta beta, non come verità.

**Dopo un pilot pagato o una forte lettera d'intenti — prodotto e fundraising.** Solo allora aggiungere
autenticazione robusta, multi-tenancy, integrazioni, monitoring, billing e preparare grant/spin-off o
pre-seed. Il fundraising non deve precedere la prova che qualcuno usa e possibilmente paga il wedge.

### Gate commerciale autonomo

Procedere dal concierge al software solo se, entro i primi 10 casi reali:

- almeno 60% delle verifiche suggerite è giudicato pertinente dal professionista;
- il report riduce tempo o migliora completezza in modo misurabile;
- non emergono errori sistematici di identità/provenance;
- almeno un partner chiede di continuare, idealmente pagando o firmando una LOI;
- è identificato chi compra, non soltanto chi trova interessante la demo.

Se questi gate non passano, cambiare workflow o chiudere il percorso commerciale senza alterare i
risultati scientifici.

### Fallback se il PhD non parte

Il piano non diventa “costruire tutto da soli”. Diventa:

1. completare comunque il pilot gold-label e una baseline reale credibile;
2. terminare un ciclo di 10–15 interviste orientate al workflow;
3. scegliere il wedge sulla base delle interviste, non della tecnologia già costruita;
4. realizzare un concierge prototype in 2–4 settimane, riusando schema decisionale e provenance;
5. ottenere 1–2 design partner e processare 5–10 casi reali;
6. decidere tra bootstrap/consulenza productizzata, grant/acceleratore o startup finanziabile.

Il repository di ricerca rimane il laboratorio/evidence layer. Il prodotto deve essere separato in
un'applicazione distinta quando compaiono documenti cliente, autenticazione, dati riservati o logica
commerciale, per non mescolare benchmark riproducibili e asset proprietari.

## 9. Cosa non dobbiamo dichiarare

Non dichiarare ancora che:

- abbiamo predetto il successo delle startup;
- la coorte SEC rappresenta startup seed VC-backed;
- un successivo Form D è una Series A;
- il sistema migliora decisioni VC reali;
- esiste product-market fit;
- il progetto è pronto per venture fundraising.

Il claim corretto oggi è: **abbiamo costruito una base open-only riproducibile e falsificato il
valore dell'acquisizione selettiva della storia SEC nel design testato. SBIR ha poi fallito il gate
temporale prima del modelling. Il claim scientifico generale resta aperto e la validazione
commerciale è ancora B0.**

## 10. Prossima milestone

> Proseguire senza interviste sul binario scientifico assumption-bound: chiudere source/adaptor work,
sviluppare esclusivamente sui 2.369 casi 2021 e selezionare sui 2.243 casi 2022. Il vault di 914 casi
2023 resta chiuso. SBIR non supera il gate temporale e USPTO è access-gated; nessuna fonte va forzata.
Le interviste ripartono quando PhD o partner forniscono accesso e restano necessarie per utility
buyer-realistic, validità esterna e qualunque percorso commerciale, non per completare metodi e paper.
