# Datasets — Inventory & Access Notes

> ⚠️ **Never commit proprietary or licensed data (PitchBook, Orbis, etc.) to this repository.**
> Store only descriptions, schemas, and derived/shareable artifacts.

## Source inventory

| Category | Source | Type | Access | Notes |
|---|---|---|---|---|
| Deals | PitchBook | Proprietary | License | Used in thesis; do not redistribute |
| Deals | Dealroom | Proprietary / Freemium | Account | Partial free tier |
| Deals | Crunchbase | API | API key | Fundamentals + LLM insights |
| Financials | Orbis | Proprietary | License | Company financials |
| Founders | LinkedIn | Public / limited API | Restricted | Respect ToS |
| Code | GitHub | API | Token | Activity signals |
| Patents | Google Patents | Public | Open | |
| Research | OpenAlex | API | Open | |
| News | GDELT | API | Open | Events |
| Web | Common Crawl | Public | Open | |
| Hiring | LinkedIn Jobs | Limited API | Restricted | |
| Funding | SEC | Public | Open | Form D etc. |
| Macro | World Bank | API | Open | |
| Macro | OECD | API | Open | |
| Macro | GEM | Dataset | Academic | Used in thesis |
| VC | OpenVC | Public | Open | |

## For each dataset, document:
- Schema / fields used
- Coverage (geography, time, stage)
- Freshness / update cadence
- License / ToS constraints
- Identity-resolution approach (how entities are matched across sources)
