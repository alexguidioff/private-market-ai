# P1 Public Point-in-Time Data Contract

**Version:** 0.1-P0 · **Status:** proposed; no source is approved until the access gate passes.

## Cohort key and timestamps
One row represents `company_id` at `decision_time`. Required timestamps:
- `event_time`: when the underlying event occurred;
- `available_time`: earliest defensible time the investor could have observed it;
- `recorded_at`: ingestion time;
- `source_version`: immutable source snapshot identifier.

A feature is eligible only when `available_time <= decision_time`. Unknown availability is treated
as unavailable, never imputed backward. Company-level grouping is mandatory in every split.

## Proposed public-source slice
| Information block | Candidate source | Acquisition action | PiT requirement |
|---|---|---|---|
| financing anchor | SEC Form D bulk filings | baseline state | filing acceptance and first-sale dates retained separately |
| technical activity | GitHub public API/archive | acquire technical signal | event timestamps and capture version |
| issuer filing history | SEC Form D history | tested block; predictive pass / VoI fail | every included filing has filing time no later than decision cutoff |
| public R&D awards | SBIR/STTR award dump | blocked after audit | award/notification dates do not prove first public availability; archived release history required |
| patent publications | USPTO/PatentsView pre-grant | conditional candidate | publication date plus audited assignee-to-issuer resolution; ODP access/version freeze required |
| crowdfunding disclosures | SEC Form C | blocked after audit | filing date is defensible and exact CIK matching passes, but only 52/2,369 development issuers have a filing known by decision time |
| founder research | OpenAlex | blocked candidate | requires reviewed founder-author identity and publication/first-indexed cutoff |
| public attention | GDELT | discovery candidate only | article timestamp no later than cutoff and primary-source verification |
| macro regime | World Bank/OECD/FRED | baseline context | vintage/revision timestamp where available |

Source status and citations are maintained in `P1_SOURCE_AUDIT.md`. SEC Form D is conditionally
accepted as the financing anchor, but not as proof of round type or institutional/priced status.
No LinkedIn scraping is permitted. Crunchbase, PitchBook and Orbis remain optional licensed layers,
not dependencies of the reproducible base.

## Future temporal evaluation and censoring
A separate company-disjoint cohort uses 2021 anchors for development, 2022 for validation and 2023
for a process-locked test. Every CIK in the historical 2016–2020 model-ready cohort is excluded. Label
windows must end by 2025-12-31, a three-month buffer before the latest available 2026 Q1 archive
boundary; incomplete windows are censored rather than mapped to zero. Test labels are physically
separated and null in operational feature/panel copies. The lock manifest and hashes are in
`P1_FUTURE_COHORT_LOCK.md`.

Buyer elicitation may be deferred while institutional access is unavailable. Development may proceed
on 2021/2022 with a complete, predeclared utility/cost assumption grid. Such analysis is
**assumption-bound** and cannot establish buyer-realistic economics. Buyer evidence remains mandatory
before commercial claims or before describing any utility scenario as empirically representative.

## Minimum fields
`company_id`, `source_entity_id`, `decision_time`, `event_time`, `available_time`, `source`,
`source_version`, `feature_name`, `feature_value`, `missing_reason`, `match_confidence`, `provenance`.
The label table is physically separated and contains `outcome_time`, `outcome_type`, `label_horizon`
and `censoring_status`.

## Entity resolution
Canonical IDs are assigned by deterministic normalized name + jurisdiction blocking, then reviewed
for ambiguous matches. A gold set records candidate pairs, reviewer decision and rationale. Matching
features computed after `decision_time` cannot enter the model.
