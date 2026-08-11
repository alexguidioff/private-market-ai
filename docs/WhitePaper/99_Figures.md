# Figures & Diagrams (tracker)

**Status:** ✅ all 13 drafted as Mermaid · **Source:** `figures/figures.md` · **Level:** 🧭 NORTH STAR

All figures exist as versionable Mermaid diagrams in `figures/figures.md`. This file tracks them and
what still needs polishing.

| Fig | Title | Chapter | Status | Notes |
|---|---|---|---|---|
| F1 | Valuation → Representation → Decision Intelligence | 1 | ✅ draft | flowchart |
| F2 | Landscape: coverage × reasoning-ready | 2 | ✅ draft | quadrantChart (needs recent Mermaid) |
| F3 | Research questions → chapters map | 3 | ✅ draft | flowchart |
| F4 | Six-layer Private Market Data Model | 4 | ✅ draft | core figure |
| F5 | Ontology (entities + relationships) | 5 | ✅ draft | property-graph view |
| F6 | KG + Digital Twins + Decision Graph | 6 | ✅ draft | shows the loop |
| F7 | Data ingestion architecture | 7 | ✅ draft | batch + streaming |
| F8 | Representation-learning stages | 8 | ✅ draft | tabular→GNN→multimodal→FM |
| F9 | Multi-agent investment system | 9 | ✅ draft | reference architecture |
| F10 | Decision object (uncertainty output) | 10 | ✅ draft | P10/P50/P90 + value of info |
| F11 | Paper × asset dependency graph | 11 | ✅ draft | roadmap DAG |
| F12 | Six-layer software architecture | 12 | ✅ draft | matches `Roadmap.md §3b` |
| F13 | Product evolution V1→V4 | 13 | ✅ draft | commercialization |

## Remaining polish
- [ ] Embed each figure into its chapter file (or reference `figures/figures.md#fN`).
- [ ] Verify `quadrantChart` (F2) renders in the target viewer; else fall back to a 2×2 table.
- [ ] For a publication/grant version, redraw as vector art; keep Mermaid as source of truth.

## Tooling
- Text-based diagrams (Mermaid) for versionability. Render in GitHub, VS Code (+Mermaid extension),
  Obsidian, etc.
