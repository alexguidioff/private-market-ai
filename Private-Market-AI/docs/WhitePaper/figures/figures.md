# White Paper — Figures (Mermaid source)

**Level:** 🧭 NORTH STAR · All diagrams are text-based (Mermaid) so they are versionable and render
in most Markdown viewers. Each figure notes the chapter it belongs to.

---

## F1 — Valuation → Representation → Decision Intelligence (Ch. 1)

```mermaid
flowchart LR
    A["Paper #1<br/>Startup valuation<br/>(prediction)"] --> B["Representation<br/>data model · ontology · graphs"]
    B --> C["Reasoning<br/>LLMs · agents"]
    C --> D["Decision Intelligence<br/>decide under uncertainty"]
    D -. "learn / feedback" .-> B
    classDef done fill:#d9ead3,stroke:#38761d;
    classDef core fill:#cfe2f3,stroke:#1155cc;
    class A done;
    class B,C,D core;
```
*Caption: the programme reframes a completed prediction result as the first step toward a
representation-and-decision layer. Valuation is the entry point, not the destination.*

---

## F2 — Competitive landscape: coverage × reasoning-readiness (Ch. 2)

```mermaid
quadrantChart
    title Private-market tooling
    x-axis "Narrow coverage" --> "Broad coverage"
    y-axis "Database / point tool" --> "Reasoning-ready representation"
    quadrant-1 "Target: integrated + reasoning-ready"
    quadrant-2 "Ontologies elsewhere (UMLS/KG)"
    quadrant-3 "Point AI tools"
    quadrant-4 "Data platforms"
    "PitchBook": [0.82, 0.20]
    "Crunchbase": [0.70, 0.28]
    "Dealroom": [0.55, 0.22]
    "AI DD startups": [0.30, 0.40]
    "KG / UMLS (other fields)": [0.25, 0.85]
    "This programme": [0.80, 0.88]
```
*Caption: incumbents are broad-but-flat (databases) or narrow point tools; reasoning-ready
representation exists in other fields but not in private markets. The target sits top-right.*

---

## F3 — Research questions → chapters (Ch. 3)

```mermaid
flowchart LR
    subgraph Paper1["Paper #1 findings"]
        RQ1["RQ1: non-financial signals suffice"]
        RQ2["RQ2: syndicate is the driver"]
        RQ3["RQ3: financials add ~nothing"]
    end
    RQ1 --> Q1["Q1 Representation<br/>Ch. 4–6"]
    RQ2 --> Q4["Q4 Causality<br/>Ch. 10"]
    RQ3 --> Q3["Q3 Uncertainty / value of info<br/>Ch. 10"]
    Q1 --> Q2["Q2 Signals<br/>Ch. 8, 10"]
    Q1 --> Q5["Q5 Human-AI decisions<br/>Ch. 9, 10"]
    Q1 --> Q6["Q6 Standardisation<br/>Ch. 5"]
```
*Caption: each narrow, answered paper question opens a broad programme question. Representation
(Q1) is the hinge the rest depend on.*

---

## F4 — The six-layer Private Market Data Model (Ch. 4)

```mermaid
flowchart TD
    L6["Layer 6 — Reasoning objects<br/>hypothesis · risk · opportunity · founder quality"]
    L5["Layer 5 — Documents (multimodal)<br/>decks · filings · news · code · patents"]
    L4["Layer 4 — Signals (behavioral)<br/>hiring velocity · GitHub · syndication · web traffic"]
    L3["Layer 3 — Events (dynamic)<br/>funding round · hiring · launch · IPO · acquisition"]
    L2["Layer 2 — Relationships (ontology)<br/>FOUNDED · INVESTED_IN · COMPETES_WITH · SITS_ON_BOARD"]
    L1["Layer 1 — Entities<br/>company · founder · investor · fund · deal · market"]
    L6 --> L5 --> L4 --> L3 --> L2 --> L1
    U["Cross-cutting: TIME + UNCERTAINTY<br/>(confidence · provenance · distributions)"]
    U -.-> L1
    U -.-> L6
```
*Caption: a private investment as a dynamic system, represented in six layers, with time and
uncertainty running through all of them.*

---

## F5 — Ontology: entities & relationships (Ch. 5)

```mermaid
flowchart LR
    Founder -->|FOUNDED| Company
    Founder -->|WORKED_AT| Company
    Partner -->|WORKS_FOR| Investor
    Partner -->|SITS_ON_BOARD| Company
    Fund -->|MANAGED_BY| Investor
    Investor -->|LED_BY / INVESTED_IN| Deal
    Deal -->|FOR_COMPANY| Company
    Company -->|OPERATES_IN| Market
    Company -->|COMPETES_WITH| Company
    Company -->|ACQUIRED| Company2["Company"]
```
*Caption: the relationship layer as a property graph. The syndicate structure (INVESTED_IN
co-participation + LED_BY) is where the paper's dominant signal lives.*

---

## F6 — Knowledge Graph + Digital Twins + Decision Graph (Ch. 6)

```mermaid
flowchart TB
    ONT["Ontology (Ch.5)"] --> KG["Temporal Multimodal<br/>Knowledge Graph<br/><i>what is true</i>"]
    KG --> DT["Digital Twins<br/>per-entity dynamic state<br/>+ uncertainty"]
    KG --> DG["Decision Graph<br/><i>how choices were made</i>"]
    DT --> DG
    DG --> OUT["Outcome linked back<br/>(process quality)"]
    OUT -. "learn" .-> KG
    subgraph Decision node
        I["information used"]
        ALT["alternatives"]
        R["rationale"]
        DM["decision-maker<br/>human / AI / hybrid"]
    end
    DG --- I
```
*Caption: the world model (knowledge graph + twins) plus the record of action (decision graph)
close the loop represent → reason → decide → observe → learn.*

---

## F7 — Data ingestion architecture (Ch. 7)

```mermaid
flowchart LR
    subgraph Sources
        P["PitchBook / Orbis<br/>(licensed)"]
        C["Crunchbase / OpenVC / SEC"]
        G["GitHub / GDELT / news"]
        M["World Bank / OECD / GEM"]
    end
    P --> B["Batch ingest"]
    C --> B
    M --> B
    G --> S["Streaming / event-driven"]
    B --> N["Normalise to ontology<br/>+ identity resolution"]
    S --> N
    N --> Q["Quality: coverage · freshness<br/>provenance · confidence"]
    Q --> KG["Knowledge Graph<br/>(bitemporal)"]
    KG --> DT["Digital Twins (kept current)"]
```
*Caption: batch for bulk sources, streaming for the dynamic layer; everything normalised to the
ontology with identity resolution and quality/provenance attached.*

---

## F8 — Representation-learning stages (Ch. 8)

```mermaid
flowchart LR
    T["Tabular ML<br/>(paper #1)<br/>hand-engineered features"] --> GNN["Graph NNs<br/>learn over relationships"]
    GNN --> MM["Multimodal<br/>text · tables · code · time series"]
    MM --> FM["Foundation models<br/>reusable entity embeddings"]
    subgraph Cross-cutting
        X["interpretability + uncertainty at every stage"]
    end
    X -.-> T
    X -.-> FM
```
*Caption: each stage is motivated by the previous result and reduces bespoke feature engineering
while growing a shared representation.*

---

## F9 — Multi-agent investment system (Ch. 9)

```mermaid
flowchart TB
    ORCH["Orchestrator agent"]
    ORCH --> SRC["Sourcing agent"]
    ORCH --> SPEC["Specialist agents<br/>market · team · tech · financials · legal"]
    ORCH --> SYN["Synthesis agent<br/>drafts memo"]
    ORCH --> CRIT["Critic / red-team agent<br/>what don't we know?"]
    KG["Knowledge Graph + Digital Twins"] --> SPEC
    SPEC --> RO["writes Reasoning objects"]
    RO --> SYN
    CRIT --> SYN
    SYN --> DEC["Decision node<br/>rationale · alternatives · uncertainty"]
    DEC --> KG
```
*Caption: grounded, human-augmenting agents that read the represented world and write reasoning
objects and an auditable decision node — with a critic agent enforcing uncertainty.*

---

## F10 — The decision object (Ch. 10)

```mermaid
flowchart LR
    IN["Evidence<br/>signals · documents · twin state"] --> MODEL["Model / agent"]
    MODEL --> OUT["DECISION OBJECT"]
    OUT --> D["distribution<br/>P10 / P50 / P90"]
    OUT --> CF["confidence"]
    OUT --> RE["reasons<br/>(which signals)"]
    OUT --> MI["missing information"]
    OUT --> VOI["value of information<br/>→ what to diligence next"]
    VOI -. "directs" .-> IN
```
*Caption: never a point estimate. Value-of-information turns the output into an active
recommendation about what to find out next.*

---

## F11 — Paper × asset dependency graph (Ch. 11)

```mermaid
flowchart TB
    P1["#1 Valuation (done)"] --> P2["#2 Data Model"]
    P2 --> P3["#3 KG / GNN"]
    P2 --> P5["#5 Uncertainty"]
    P3 --> P4["#4 Multimodal"]
    P5 --> P6["#6 Causal signals"]
    P4 --> P7["#7 Agentic DD"]
    P6 --> P7
    P3 --> P8["#8 Human-AI IC"]
    P7 --> P10["#10 Decision Intelligence"]
    P8 --> P10
    BENCH["PrivateBench (#9)<br/>built early, grows"] -. "evaluates" .-> P2
    BENCH -. "evaluates" .-> P10
    SIM["Simulator"] -. "enables" .-> P7
    SIM -. "enables" .-> P8
    class P1 done;
    classDef done fill:#d9ead3,stroke:#38761d;
```
*Caption: one question in layers. A 4-year PhD draws #2–#4; PrivateBench and the Simulator are the
enabling assets.*

---

## F12 — Six-layer software architecture (Ch. 12)

```mermaid
flowchart TB
    HI["Human Interface Layer<br/>analysts · IC · memos"]
    DEC["Decision Layer<br/>Decision Graph"]
    REA["Reasoning Layer<br/>LLMs · agents"]
    REP["Representation Layer<br/>Digital Twins · embeddings"]
    KNO["Knowledge Layer<br/>Knowledge Graph · Ontology"]
    DAT["Data Layer<br/>sources · ingestion"]
    HI --> DEC --> REA --> REP --> KNO --> DAT
    UNC["Uncertainty<br/>(cross-cutting)"]
    UNC -.-> HI
    UNC -.-> DAT
```
*Caption: the engineering counterpart to the science; uncertainty runs through every layer.*

---

## F13 — Product evolution V1 → V4 (Ch. 13)

```mermaid
flowchart LR
    V1["V1 Valuation Assistant<br/>uncertainty-first"] --> V2["V2 Due Diligence Copilot<br/>agentic + memo"]
    V2 --> V3["V3 Investment Copilot<br/>sourcing → IC support"]
    V3 --> V4["V4 Private Market OS<br/>decision-intelligence platform"]
    R["research foundations first<br/>(Ch. 4–12)"] -.-> V1
```
*Caption: products are productised layers of the architecture; each depends on the research being
done first. Science first, company last.*

---

## Rendering notes
- Mermaid renders in GitHub, VS Code (with a Mermaid extension), Obsidian, and many viewers.
- `quadrantChart` (F2) needs a recent Mermaid version; if it fails to render, a simple 2×2 table is
  a fallback.
- These are schematic. Publication-quality versions (for a real paper/grant) may be redrawn in a
  vector tool, but the Mermaid source stays the version-controlled source of truth.
