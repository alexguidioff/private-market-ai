# Can Non-Financial Signals Price Private Companies?
## A Machine Learning Approach to Startup Valuation — One-Pager

**Authors:** Alessandro Guidi, Saad Rashid, Hao Zhong (ESCP Business School)
**Venue:** WI2026 Student Track (accepted)
**Level:** 📣 **[OUTREACH — public]** — attach to emails. One page. Not the full paper.

> ⚠️ Before sharing: re-export a clean copy of the PDF — the source file carries an
> "Amazon Confidential" metadata label (see `papers/notes/WI2026_paper_summary.md`).

---

### Problem
Private startups are hard to price: extreme information asymmetry, non-linear growth, and short
histories make DCF impractical and comparables unstable during market swings. **Can non-financial
signals substitute for traditional financial metrics in startup valuation?**

### Data
- **3,403 venture-capital deals** from PitchBook + macro data from **GEM** (Global Entrepreneurship Monitor).
- **Out-of-time holdout** spanning the post-2022 correction: train on pre-April-2022 (bull, n=2,723),
  test on post-April-2022 (contraction, n=680) — a genuine regime shift for all models.

### Method — a progressive 3-layer design
- **Layer 1:** OLS financial baselines (Revenue, EBITDA, Revenue Multiple).
- **Layer 2:** ML on **non-financial** features only (firmographics, deal context, investor syndicate).
- **Layer 3:** ML on the full set (Layer 2 + financials + macro) — an *ablation* to measure the
  marginal value of financial data.
- Models: Random Forest, Gradient Boosting, ElasticNet. Interpretability via **SHAP**.

### Results (out-of-sample, n=680)
- **Non-financial ML is competitive with the best financial baseline.** Layer-2 Random Forest
  achieves the **best absolute error (MAE 0.888; R² 0.557)**.
- The OLS Revenue Multiple has a higher R² (0.643) but the **highest cross-validation instability**
  → poor generalization across regimes; the ML models are more robust.
- **"Information Saturation":** adding financial + macro data (Layer 3) yields virtually identical
  performance to non-financial-only (Layer 2) — trailing financials add minimal value.
- **SHAP:** **investor-syndicate capacity**, not firm financials, is the dominant pricing driver
  (a "certification effect").

### Contribution
1. Evidence that **non-financial signals alone can price private companies** competitively — and
   more robustly across market regimes — than financial baselines.
2. A **progressive, interpretable 3-layer framework** that quantifies the marginal value of
   financial data (answering: it is largely redundant here).
3. A foundation for a deeper question: **how to *represent* a startup and its ecosystem** so AI
   systems can support investment decisions (the direction of Paper #2).

### Why it matters / what's next
Especially useful for **pre-revenue or data-sparse** startups, where financials are absent. The
natural next step is a structured **representation** of private companies (entities, relationships,
events, signals) with **uncertainty-aware** outputs — the basis of the broader research agenda.

---
*Contact: alexguidioff@gmail.com · alessandroguidi.site · github.com/alexguidioff ·
linkedin.com/in/alessandroguidi1 · Full paper available on request.*
