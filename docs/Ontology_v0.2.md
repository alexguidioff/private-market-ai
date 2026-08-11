# Private Market Ontology — v0.2 (machine-readable)

**Level:** 🧭 NORTH STAR · Companion to `Ontology.md` (prose) and `WhitePaper/05_*` (chapter).

This is the **machine-readable** version of the ontology: JSON Schema (draft 2020-12) formalising the
entities, relationships, events, signals, and reasoning objects. JSON-schema-first was chosen (per
`WhitePaper/05_Private_Market_Ontology.md §5.7`) as the pragmatic, developer-friendly serialization;
an RDF/OWL export can be generated later for interoperability.

> The schema is kept as fenced code blocks in this single Markdown file so it stays versionable in
> one place. To use it, split each block into its own `.json` file (names given in headings) and run
> a JSON Schema validator.

## Design conventions
- **Identity:** every node has a stable `id` and a human-readable `name`.
- **Temporal / bitemporal:** `valid_from`/`valid_to` (world time) + `recorded_at` (system time).
- **Provenance & confidence:** every asserted fact/event/signal/reasoning object carries a
  `provenance` block and a `confidence` in [0,1].
- **Enums** are small and extensible; unknown values allowed via `"other"`.

---

## `common.schema.json` — shared types

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pm-ontology/v0.2/common.schema.json",
  "title": "Common types",
  "$defs": {
    "id": { "type": "string", "minLength": 1 },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "provenance": {
      "type": "object",
      "properties": {
        "source": { "type": "string" },
        "source_url": { "type": "string" },
        "recorded_at": { "type": "string", "format": "date-time" },
        "license": { "type": "string" }
      },
      "required": ["source", "recorded_at"]
    },
    "temporal": {
      "type": "object",
      "properties": {
        "valid_from": { "type": "string", "format": "date" },
        "valid_to": { "type": ["string", "null"], "format": "date" }
      }
    },
    "money": {
      "type": "object",
      "properties": {
        "amount": { "type": "number", "minimum": 0 },
        "currency": { "type": "string", "enum": ["EUR", "USD", "CHF", "GBP", "other"] }
      },
      "required": ["amount", "currency"]
    },
    "assertion": {
      "type": "object",
      "properties": {
        "provenance": { "$ref": "common.schema.json#/$defs/provenance" },
        "confidence": { "$ref": "common.schema.json#/$defs/confidence" },
        "temporal": { "$ref": "common.schema.json#/$defs/temporal" }
      }
    }
  }
}
```

---

## `entities.schema.json` — the nine core entities

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pm-ontology/v0.2/entities.schema.json",
  "title": "Entities",
  "$defs": {
    "Company": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "name": { "type": "string" },
        "type": { "const": "Company" },
        "sector": { "type": "string" },
        "sub_sector": { "type": "string" },
        "founded_year": { "type": "integer", "minimum": 1800, "maximum": 2100 },
        "country": { "type": "string", "description": "ISO 3166 alpha-2" },
        "business_model": { "type": "string" },
        "stage": {
          "type": "string",
          "enum": ["pre-seed", "seed", "series-a", "series-b", "series-c+", "growth", "pre-ipo", "other"]
        },
        "status": { "type": "string", "enum": ["active", "acquired", "ipo", "closed", "other"] },
        "provenance": { "$ref": "common.schema.json#/$defs/provenance" },
        "confidence": { "$ref": "common.schema.json#/$defs/confidence" }
      },
      "required": ["id", "name", "type"]
    },
    "Founder": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "name": { "type": "string" },
        "type": { "const": "Founder" },
        "education": { "type": "array", "items": { "type": "string" } },
        "prior_companies": { "type": "array", "items": { "type": "string" } },
        "prior_exits": { "type": "integer", "minimum": 0 },
        "role": { "type": "string", "enum": ["CEO", "CTO", "COO", "other"] }
      },
      "required": ["id", "name", "type"]
    },
    "Investor": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "name": { "type": "string" },
        "type": { "const": "Investor" },
        "investor_type": {
          "type": "string",
          "enum": ["vc", "pe", "cvc", "angel", "family-office", "growth", "other"]
        },
        "aum": { "$ref": "common.schema.json#/$defs/money" },
        "dry_powder": { "$ref": "common.schema.json#/$defs/money" }
      },
      "required": ["id", "name", "type"]
    },
    "Fund": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "name": { "type": "string" },
        "type": { "const": "Fund" },
        "vintage": { "type": "integer" },
        "strategy": { "type": "string" },
        "size": { "$ref": "common.schema.json#/$defs/money" },
        "geography": { "type": "string" }
      },
      "required": ["id", "name", "type"]
    },
    "Partner": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "name": { "type": "string" },
        "type": { "const": "Partner" },
        "investor_id": { "$ref": "common.schema.json#/$defs/id" },
        "focus": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["id", "name", "type"]
    },
    "Market": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "name": { "type": "string" },
        "type": { "const": "Market" },
        "country": { "type": "string" },
        "sector": { "type": "string" },
        "tam": { "$ref": "common.schema.json#/$defs/money" },
        "funding_climate": { "type": "string", "enum": ["hot", "neutral", "cooling", "cold", "other"] }
      },
      "required": ["id", "name", "type"]
    },
    "Deal": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "type": { "const": "Deal" },
        "company_id": { "$ref": "common.schema.json#/$defs/id" },
        "round": { "type": "string" },
        "date": { "type": "string", "format": "date" },
        "amount": { "$ref": "common.schema.json#/$defs/money" },
        "valuation_pre": { "$ref": "common.schema.json#/$defs/money" },
        "valuation_post": { "$ref": "common.schema.json#/$defs/money" },
        "lead_investor_id": { "$ref": "common.schema.json#/$defs/id" },
        "participant_ids": { "type": "array", "items": { "$ref": "common.schema.json#/$defs/id" } }
      },
      "required": ["id", "type", "company_id", "round", "date"]
    },
    "Product": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "type": { "const": "Product" },
        "company_id": { "$ref": "common.schema.json#/$defs/id" },
        "repository": { "type": "string" },
        "website": { "type": "string" },
        "technology_stack": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["id", "type", "company_id"]
    },
    "Customer": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "type": { "const": "Customer" },
        "company_id": { "$ref": "common.schema.json#/$defs/id" },
        "segment": { "type": "string", "enum": ["enterprise", "smb", "consumer", "other"] },
        "retention": { "type": "number", "minimum": 0, "maximum": 1 }
      },
      "required": ["id", "type", "company_id"]
    }
  }
}
```

---

## `relationships.schema.json` — typed edges

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pm-ontology/v0.2/relationships.schema.json",
  "title": "Relationships",
  "type": "object",
  "properties": {
    "id": { "$ref": "common.schema.json#/$defs/id" },
    "predicate": {
      "type": "string",
      "enum": ["FOUNDED", "WORKED_AT", "INVESTED_IN", "OWNS", "MANAGED_BY", "WORKS_FOR",
               "SITS_ON_BOARD", "OPERATES_IN", "COMPETES_WITH", "ACQUIRED", "FOR_COMPANY", "LED_BY"]
    },
    "subject_id": { "$ref": "common.schema.json#/$defs/id" },
    "object_id": { "$ref": "common.schema.json#/$defs/id" },
    "temporal": { "$ref": "common.schema.json#/$defs/temporal" },
    "provenance": { "$ref": "common.schema.json#/$defs/provenance" },
    "confidence": { "$ref": "common.schema.json#/$defs/confidence" }
  },
  "required": ["id", "predicate", "subject_id", "object_id"]
}
```

---

## `events.schema.json` — state-changing events

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pm-ontology/v0.2/events.schema.json",
  "title": "Event",
  "type": "object",
  "properties": {
    "id": { "$ref": "common.schema.json#/$defs/id" },
    "event_type": {
      "type": "string",
      "enum": ["FundingRound", "Hiring", "Departure", "FounderLeft", "NewCEO", "ProductLaunch",
               "PatentFiling", "Acquisition", "IPO", "CustomerWin", "CustomerLoss", "Lawsuit",
               "Grant", "OpenSourceRelease", "GitHubActivity", "PressMention", "other"]
    },
    "entity_id": { "$ref": "common.schema.json#/$defs/id" },
    "timestamp": { "type": "string", "format": "date-time" },
    "payload": { "type": "object", "description": "Event-type-specific fields." },
    "provenance": { "$ref": "common.schema.json#/$defs/provenance" },
    "confidence": { "$ref": "common.schema.json#/$defs/confidence" }
  },
  "required": ["id", "event_type", "entity_id", "timestamp"]
}
```

---

## `signals.schema.json` — behavioral signals

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pm-ontology/v0.2/signals.schema.json",
  "title": "Signal",
  "type": "object",
  "properties": {
    "id": { "$ref": "common.schema.json#/$defs/id" },
    "entity_id": { "$ref": "common.schema.json#/$defs/id" },
    "metric": {
      "type": "string",
      "enum": ["hiring_velocity", "employee_churn", "github_commits", "founder_posting_frequency",
               "investor_syndication", "patent_velocity", "release_frequency", "customer_growth",
               "web_traffic", "developer_activity", "conference_talks", "other"]
    },
    "value": { "type": "number" },
    "window": { "type": "string", "description": "e.g. 30d, 12m." },
    "timestamp": { "type": "string", "format": "date-time" },
    "provenance": { "$ref": "common.schema.json#/$defs/provenance" },
    "confidence": { "$ref": "common.schema.json#/$defs/confidence" }
  },
  "required": ["id", "entity_id", "metric", "value", "timestamp"]
}
```

---

## `reasoning.schema.json` — reasoning objects + the decision object

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pm-ontology/v0.2/reasoning.schema.json",
  "title": "Reasoning objects and decision object",
  "$defs": {
    "ReasoningObject": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "reasoning_type": {
          "type": "string",
          "enum": ["Hypothesis", "Risk", "Opportunity", "Competition", "MarketFit",
                   "TechnologyRisk", "ExecutionRisk", "CapitalEfficiency", "FounderQuality", "Governance"]
        },
        "entity_id": { "$ref": "common.schema.json#/$defs/id" },
        "statement": { "type": "string" },
        "evidence_ids": {
          "type": "array",
          "items": { "$ref": "common.schema.json#/$defs/id" },
          "description": "IDs of events/signals/documents supporting the statement."
        },
        "confidence": { "$ref": "common.schema.json#/$defs/confidence" },
        "author": { "type": "string", "enum": ["human", "ai", "hybrid"] }
      },
      "required": ["id", "reasoning_type", "entity_id", "statement", "author"]
    },
    "DecisionObject": {
      "type": "object",
      "description": "The programme's signature output (WhitePaper Ch.10 §10.6). Never a point.",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "entity_id": { "$ref": "common.schema.json#/$defs/id" },
        "target": { "type": "string", "description": "e.g. fair_value_pre_money." },
        "distribution": {
          "type": "object",
          "properties": {
            "p10": { "type": "number" },
            "p50": { "type": "number" },
            "p90": { "type": "number" },
            "currency": { "type": "string" }
          },
          "required": ["p10", "p50", "p90"]
        },
        "confidence": { "$ref": "common.schema.json#/$defs/confidence" },
        "reasons": { "type": "array", "items": { "type": "string" } },
        "missing_information": { "type": "array", "items": { "type": "string" } },
        "value_of_information": {
          "type": "array",
          "description": "Which missing item would most reduce uncertainty, ranked.",
          "items": {
            "type": "object",
            "properties": {
              "item": { "type": "string" },
              "expected_uncertainty_reduction": { "type": "number", "minimum": 0, "maximum": 1 }
            },
            "required": ["item"]
          }
        }
      },
      "required": ["id", "entity_id", "target", "distribution", "confidence"]
    },
    "DecisionNode": {
      "type": "object",
      "description": "Decision Graph node (WhitePaper Ch.6): how a choice was made.",
      "properties": {
        "id": { "$ref": "common.schema.json#/$defs/id" },
        "decision": { "type": "string" },
        "information_used_ids": { "type": "array", "items": { "$ref": "common.schema.json#/$defs/id" } },
        "alternatives": { "type": "array", "items": { "type": "string" } },
        "rationale": { "type": "string" },
        "decision_maker": { "type": "string", "enum": ["human", "ai", "hybrid"] },
        "timestamp": { "type": "string", "format": "date-time" },
        "outcome": { "type": ["string", "null"], "description": "Linked back when it materializes." }
      },
      "required": ["id", "decision", "decision_maker", "timestamp"]
    }
  }
}
```

---

## `example.nimbusai.json` — the Ch.4 §4.6 worked example, encoded

> ⚠️ Synthetic/illustrative data (matches `WhitePaper/04 §4.6`). Not a real company.

```json
{
  "entities": [
    { "id": "co_nimbus", "type": "Company", "name": "NimbusAI", "sector": "dev-tools/AI-infra",
      "founded_year": 2021, "country": "CH", "business_model": "open-core-saas", "stage": "series-a",
      "status": "active", "confidence": 0.9,
      "provenance": { "source": "synthetic", "recorded_at": "2026-07-01T00:00:00Z" } },
    { "id": "fnd_f1", "type": "Founder", "name": "F1", "prior_exits": 1, "role": "CEO",
      "prior_companies": ["Google"] },
    { "id": "inv_alpha", "type": "Investor", "name": "Alpha Ventures", "investor_type": "vc" },
    { "id": "deal_a", "type": "Deal", "company_id": "co_nimbus", "round": "series-a",
      "date": "2023-03-01", "amount": { "amount": 12000000, "currency": "EUR" },
      "valuation_pre": { "amount": 40000000, "currency": "EUR" }, "lead_investor_id": "inv_alpha" }
  ],
  "relationships": [
    { "id": "r1", "predicate": "FOUNDED", "subject_id": "fnd_f1", "object_id": "co_nimbus" },
    { "id": "r2", "predicate": "LED_BY", "subject_id": "deal_a", "object_id": "inv_alpha" },
    { "id": "r3", "predicate": "OPERATES_IN", "subject_id": "co_nimbus", "object_id": "mkt_ai_infra_eu" }
  ],
  "events": [
    { "id": "e1", "event_type": "OpenSourceRelease", "entity_id": "co_nimbus",
      "timestamp": "2022-04-01T00:00:00Z" },
    { "id": "e2", "event_type": "FundingRound", "entity_id": "co_nimbus",
      "timestamp": "2023-03-01T00:00:00Z", "payload": { "round": "series-a" } }
  ],
  "signals": [
    { "id": "s1", "entity_id": "co_nimbus", "metric": "investor_syndication", "value": 3,
      "window": "series-a", "timestamp": "2023-03-01T00:00:00Z" }
  ],
  "decision_object": {
    "id": "do1", "entity_id": "co_nimbus", "target": "fair_value_pre_money",
    "distribution": { "p10": 30000000, "p50": 42000000, "p90": 58000000, "currency": "EUR" },
    "confidence": 0.6,
    "reasons": ["syndicate quality", "founder track record", "OSS traction"],
    "missing_information": ["revenue/retention detail", "enterprise pipeline"],
    "value_of_information": [
      { "item": "churn data", "expected_uncertainty_reduction": 0.4 },
      { "item": "enterprise pipeline", "expected_uncertainty_reduction": 0.3 }
    ]
  }
}
```

---

## Status & TODO
- v0.2 draft; the worked example is encoded but the schema has **not** yet been run through a
  validator.
- [ ] Validate all blocks with a JSON Schema validator (draft 2020-12); split into `.json` files.
- [ ] Add cardinality/uniqueness constraints from `WhitePaper/05 §5.3`.
- [ ] Generate an RDF/OWL export for interoperability.
- [ ] Expand enums (sectors, event types) from a real public-data sample.
