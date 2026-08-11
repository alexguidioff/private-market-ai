# Outreach Brief
## The ONLY thing you show professors (+ the WI2026 one-pager)

**Author:** Alessandro Guidi — v0.1
**Level:** 📣 **[OUTREACH — public]** — this is deliberately small. That is the point.

> Golden rule: talk about **the paper you have** and **the next paper (Paper #2)**. Maybe two
> possible directions. Nothing else. No "Bloomberg of private markets", no 2033 roadmap, no
> PrivateBench, no theory. The bigger the vision, the less you say early.

---

## Version C — Elevator pitch (30 seconds)

> "I'm working on AI to support investment decisions in private markets. My first piece is on
> startup valuation, but I've come to think the more interesting problem isn't valuation itself —
> it's *how you represent a startup in a structured way* so that models can reason about it. I'd
> like to turn that into a research line."

That's it. Then **stop and listen**. Let the professor pull.

---

## Version B — The 5-pager (attach to emails / bring to calls)

### 1. Title
**Explainable Machine Learning for Startup Valuation — and toward a structured representation of
private companies.**

### 2. Short abstract (5–6 lines)
Using 3,403 PitchBook deals and GEM macro data, and a strict out-of-time holdout across the 2022
correction, we show that interpretable ML trained **only on non-financial signals** (firmographics,
deal context, investor syndicate) prices private companies competitively with the best financial
baselines — and more robustly across market regimes — while adding financial/macro data adds
negligible value. Accepted at the **WI2026 Student Track** (Guidi, Rashid & Zhong). The work points
to a broader problem: how to *represent* a startup and its ecosystem so AI systems can support
investment decisions.

### 3. Main result
- ML on **non-financial signals alone** matches the best financial baseline (Layer-2 Random Forest:
  MAE 0.888, R² 0.557) and generalizes more robustly than the OLS Revenue Multiple.
- Adding financial + macro data yields near-identical performance ("information saturation").
- **SHAP:** investor-syndicate capacity, not firm financials, is the dominant pricing driver.
- Especially relevant for **pre-revenue / data-sparse** startups.

### 4. What I'm looking for
- Methodological feedback from your group.
- Whether this could become a **collaboration / RA / research project**.
- Access to relevant datasets or industry partners, if any.
- (If it fits) a path toward a **BRIDGE / Innosuisse** application later.

### 5. Two possible research directions *(mention at most these two)*
1. **Representation (Paper #2):** a structured, unified representation of private companies
   (entities, relationships, events, signals) as the basis for downstream decision support.
2. **Uncertainty:** moving from point valuations to distributional, confidence-aware outputs
   (what we know, what we don't, and what it's worth finding out).

> Everything beyond these two lives in the NORTH STAR documents and is **not** presented here.

---

## Email template (Wave 1 — personalize per professor)

```
Subject: Methodological feedback — explainable ML for startup valuation (WI2026)

Dear Prof. [Name],

I read your work on [specific paper / topic] and found [specific point] closely related to a
question I'm working on.

My paper "Can Non-Financial Signals Price Private Companies?" was accepted at the WI2026 Student
Track. It applies interpretable ML (Random Forest + SHAP) to startup valuation using firm, deal,
investor and macro signals on 3,403 PitchBook deals.

While finishing it, I became more interested in a deeper problem than valuation itself: how to
*represent* a startup and its ecosystem in a structured way so models can reason about it. I'd
value your view on whether this could grow into a research line — and whether there might be room
for a collaboration or research project in your group.

Would you be open to a 30-minute call?

Best regards,
Alessandro Guidi
[one-pager attached · GitHub · Scholar]
```

---

## The 3 questions to ask in the call
1. "Is the most interesting contribution here *finance*, *AI methodology*, or *information systems*?"
2. "Do you have access to datasets or industry partners relevant to private markets / fintech?"
3. "Is there a realistic paid path — RA, scientific assistant, BRIDGE, Innosuisse, or fellowship?"

---

## Reminders
- Bring the **5-pager + WI2026 one-pager**, not the full thesis, not this repository.
- If asked "have you thought about knowledge graphs / agents / a platform?" — acknowledge briefly,
  stay focused on Paper #2. You already know where it goes; you don't need to say so.
- Verify the professor's exact title/affiliation before sending (see `Professors.md`).
