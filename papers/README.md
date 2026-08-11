# Papers

Index of your own papers and where to drop the PDFs.

## Your papers
| # | Title | Authors | Venue | Status | File |
|---|---|---|---|---|---|
| 1 | Can Non-Financial Signals Price Private Companies? A ML Approach to Startup Valuation | Guidi, Rashid & Zhong (ESCP) | WI2026 Student Track | Accepted | `WI2026.pdf` *(add clean copy)* |
| P1 | Cost-Aware Value of Information for Private-Market Diligence | Guidi | Working paper | Evidence + diagnosis complete (v2026-07-29, 7.6k words); **literature review pending** | `P1_Cost_Aware_VoI_Working_Paper.md` |

### P1 status detail (2026-07-29)

The draft now carries the full diagnostic sequence, not just the falsified policy. What changed:

- **§§4.5–4.8 added** — EXP-005 (oracle decomposition), EXP-007 (slice restriction), EXP-008 (null
  ordering and the retraction of EXP-007's reading), EXP-009 (calibrated null and change targeting).
- **§8.6 added, and it is now the paper's central claim** — selective value of information requires the
  *direction* of a decision change to be predictable, not its *incidence*. Incidence reaches ROC-AUC
  0.950 while direction sits at r ≈ 0, and the policy built on incidence passes 0 of 15 gates.
- **§5 and §11 rewritten** around the condition instead of around EXP-001C's failure.
- **§6.1 strengthened** with the measured entity-resolution ceiling (80.8% balanced accuracy, 0–11% on
  lexically dissimilar same-entity pairs), so the OpenAlex rejection rests on measurement.
- **§7.2 extended** with the condition's own limits, including the optional-stopping disclosure for
  §§4.6–4.8, and §8.x numbering collision fixed.

**What remains before this is submittable, in order:**

1. **Literature review — §1.1 now drafted, but at abstract level only.** Eight entries verified
   bibliographically with differentiation written from abstracts: Chaloner & Verdinelli, Rainforth et al.,
   Javdani et al., Ma et al. (EDDI), Golovin & Krause (JAIR 42, 2011 — cited for the *vacuous* condition
   in §4.5), Gompers/Gornall/Kaplan/Strebulaev, and the *Information* 2026 leakage-controlled startup
   prediction paper. **New find worth reading first:** Alur et al., "Auditing for Human Expertise"
   (arXiv:2306.01646) — it tests whether expert predictions are conditionally independent of the outcome
   given the features, which is structurally the same question §8.6 answers for a purchasable information
   block. Their hypothesis test and our oracle bound are complementary and their test should be adopted.
   **Still required:** read the full texts. The differentiation lines position the contribution; they do
   not survive examination as written.
   ✅ **Both previously-unverified references supplied and confirmed 2026-07-29, now cited:**
   - Dong, W., Saar-Tsechansky, M. and Geva, T., "A Machine Learning Framework for Assessing Experts'
     Decision Quality", *Management Science* **71(7):5696–5721, 2025** (not 2024 — correct the year
     wherever internal notes say otherwise). DOI 10.1287/mnsc.2021.03357; preprint arXiv:2110.11425.
     Their setting is abundant past decisions with scarce ground truth, which is exactly P1's weak-proxy
     situation and P2's core problem.
   - VCBench, arXiv:2509.14448, leaderboard at vcbench.com. Founder-success prediction, 22 systems
     across 9 organisations. **Unexpected bonus:** its headline metric is precision-weighted
     (F<sub>0.5</sub>), which is independent corroboration of §8.3's argument that a capacity-constrained
     decision must not be judged on average discrimination. Cited as support, not as a competitor.
     Also worth noting for P2/P3: the leaderboard carries human baselines, with Tier-1 VCs at
     F<sub>0.5</sub> 10.7 and Y Combinator at 8.6 against a random baseline of 9.0.
2. **Venue decision**, which determines framing: an ML workshop rewards the transferable condition in
   §8.6; Management Science or an IS venue rewards the source-gate and protocol discipline in §6 and §9.
3. **A second information block** — the largest threat to §8.6, and blocked on four fronts already
   documented in §6. USPTO/PatentsView is the only credential-limited one rather than fundamentally
   blocked.
4. Buyer utility elicitation. Deferred, not eliminated (§8.5).

The locked 2023 vault (914 issuers) remains unopened and no result in the draft uses it.
| — | Machine Learning for Startup Valuation | Guidi (ESCP) | MSc thesis | Completed | `Thesis.pdf` *(add)* |

- Full extracted summary + real reference list: `notes/WI2026_paper_summary.md`.
- ⚠️ **Compliance:** the current PDF (`Machine Learning for Startup Valuation_v09_HZ.pdf` on the
  Desktop) carries an **"Amazon Confidential" metadata label** — re-export a clean, unclassified
  copy before committing here, posting to GitHub, or attaching to applications.
- **Do not commit any file that contains proprietary PitchBook data.**

## Reading notes
External-paper reading notes live in `notes/`. One file per paper, or append to
`../docs/Research_Log.md`.
