# WI2026 Paper — extracted summary & references (from PDF, verified)

**Source:** `Machine Learning for Startup Valuation_v09_HZ.pdf` (17 pp, extracted 2026-07).
**Level:** reference note — the authoritative facts about the paper.

> ⚠️ **Compliance flag:** the PDF carries an **"Amazon Confidential" MSIP label** in its metadata.
> Re-export a clean (unclassified) copy before posting to GitHub or attaching to applications.

---

## Exact title & authorship
**Can Non-Financial Signals Price Private Companies? A Machine Learning Approach to Startup Valuation**
- **Authors:** Alessandro Guidi¹, **Saad Rashid¹**, **Hao Zhong²** — ESCP Business School.
  (¹ Students; ² Information & Operations Management — hzhong@escp.eu)
- ⚠️ **Three authors** — earlier docs said single-author. Correct everywhere.

## Research questions
- **RQ1:** How do ML models trained only on non-financial signals compare to traditional financial
  valuation baselines under market stress?
- **RQ2:** Which structural / macro-environmental features are the primary drivers of algorithmic pricing?
- **RQ3:** Does adding traditional financial data give marginal predictive utility, or are
  non-financial signals alone sufficient?

## Data
- **3,403 VC deals** from PitchBook + macro data from **GEM (Global Entrepreneurship Monitor)**.
- **Out-of-time holdout:** train on pre-April-2022 (bull), test on post-April-2022 correction.
  Train n=2,723; holdout test n=680.

## Method — progressive 3-layer design
- **Layer 1:** OLS baselines on financials (Revenue, EBITDA, VC round; Revenue Multiple).
- **Layer 2:** ML on **non-financial** features only (firmographics, deal context, investor
  syndicate) — financial features excluded.
- **Layer 3:** ML on full feature set (Layer 2 + Revenue, EBITDA, GEM).
- Models: Random Forest, Gradient Boosting (lr 0.05, 300 est., max depth 3), ElasticNet.
- Interpretability: **SHAP** (Lundberg et al., 2020).

## Results (out-of-sample holdout, n=680)
| Model | R² | MAE |
|---|---|---|
| Baseline Median | 0.110 | 1.280 |
| OLS Revenue | 0.293 | 1.173 |
| OLS EBITDA | 0.163 | 1.241 |
| OLS Revenue+EBITDA | 0.408 | 1.058 |
| OLS Revenue Multiple (Model 4) | **0.643** | 0.895 |
| **Random Forest — Layer 2 (non-financial)** | **0.557** | **0.888** (best MAE) |
| Gradient Boosting — Layer 2 | 0.558 | 0.897 |
| ElasticNet — Layer 2 | 0.419 | 1.066 |
| Gradient Boosting — Layer 3 (full) | 0.552 | 0.901 |
| Random Forest — Layer 3 (full) | 0.547 | 0.893 |

## Key findings
1. **Non-financial ML models are competitive** with the best financial baseline. Layer-2 Random
   Forest has the **best absolute error (MAE 0.888)**.
2. Revenue Multiple (OLS) has the highest R² (0.643) but **highest CV instability**
   (CV R² std 0.048) → poor generalization across regimes; ML models are more robust.
3. **"Information Saturation":** adding financial + macro data (Layer 3) gives virtually identical
   performance to non-financial-only (Layer 2) → trailing financials add minimal value (answers RQ3).
4. **Investor syndicate capacity** (not firm financials) is the dominant pricing driver (SHAP) —
   consistent with the "certification effect" (Hochberg et al., 2007).

> ⚠️ **Correction:** the "R² ≈ 0.45 / half the variance unexplained" framing (from the ChatGPT
> chat) is **inaccurate**. Best non-financial ML ≈ R² 0.56; the real headline is *non-financial
> signals suffice and are more robust*, not "low R²".

---

## References (verbatim from the paper, 17 entries)
1. Damodaran, A. (2009). *The dark side of valuation: Valuing young, distressed, and complex businesses* (2nd ed.). FT Press/Pearson. ISBN 978-0-13-712689-7.
2. Garkavenko, M., Beliaeva, T., Gaussier, E., Mirisaee, H., Lagnier, C., & Guerraz, A. (2023). Assessing the factors related to a start-up's valuation using prediction and causal discovery. *Entrepreneurship Theory and Practice*, 47(5), 2017–2044.
3. Gornall, W., & Strebulaev, I. A. (2020). Squaring venture capital valuations with reality. *Journal of Financial Economics*, 135(1), 120–143.
4. Hochberg, Y. V., Ljungqvist, A., & Lu, Y. (2007). Whom you know matters: Venture capital networks and investment performance. *Journal of Finance*, 62(1), 251–301.
5. Miloud, T., Aspelund, A., & Cabrol, M. (2012). Startup valuation by venture capitalists: An empirical study. *Venture Capital*, 14(2–3), 151–174.
6. Molnar, C. (2022). *Interpretable machine learning: A guide for making black box models explainable* (2nd ed.). Independently published. ISBN 979-8411463330.
7. Pratt, S. P., & Niculita, A. V. (2008). *Valuing a business: The analysis and appraisal of closely held companies* (5th ed.). McGraw-Hill. ISBN 978-0-07-144180-3.
8. Metrick, A., & Yasuda, A. (2010). The economics of private equity funds. *The Review of Financial Studies*, 23(6), 2303–2341.
9. Blanquet, L. B., Pereira, M. A., & Petrov, S. (2025). An interpretable machine learning framework for explaining company valuation. *Decision Analytics Journal*, 16, 100611.
10. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proc. 22nd ACM SIGKDD*, 785–794.
11. Dhochak, M., Pahal, S., & Doliya, P. (2024). Predicting the startup valuation: A deep learning approach. *Venture Capital*, 26(1), 1–25.
12. Dixon, M. F., Halperin, I., & Bilokon, P. (2020). *Machine Learning in Finance: From Theory to Practice*. Springer.
13. Koller, T., Goedhart, M., & Wessels, D. (2015). *Valuation: Measuring and Managing the Value of Companies* (6th ed.). John Wiley & Sons. ISBN 978-1-118-87370-0.
14. Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S. I. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56–67.
15. Te, Y.-F., Wieland, M., Frey, M., Pyatigorskaya, A., Schiffer, P., & Grabner, H. (2023). Making it into a successful Series A funding: An analysis of Crunchbase and LinkedIn data. *The Journal of Finance and Data Science*, 9, 100099.
16. Zhang, R., Tian, Z., McCarthy, K. J., Wang, X., & Zhang, K. (2023). Application of machine learning techniques to predict entrepreneurial firm valuation. *Journal of Forecasting*, 42(2), 402–417.
17. Geertsema, P., & Lu, H. (2023). Relative valuation with machine learning. *Journal of Accounting Research*, 61(1), 329–376.
