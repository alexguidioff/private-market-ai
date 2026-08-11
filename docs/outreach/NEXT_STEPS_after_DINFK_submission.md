# After the D-INFK submission — what actually needs doing

**All sent 2026-07-29:** D-INFK doctoral portal (LAS named), LAS group email, ODI Google form,
eligibility pre-check to `phd@inf.ethz.ch`. See `SUBMISSION_LOG.md` for the record.

**Status of this file:** items 2, 3 and 4 below are **done**. What remains is item 1 (referees), item 5
(GitHub exposure), and the two retroactive checks at the end. Kept rather than deleted so the reasoning
behind each channel is still available if a reply arrives in three months.

---

## Still open — and item 1 is the only one that can fail silently

### 1. ⏳ Tell both referees, now — NOT DONE UNTIL CONFIRMED

The portal contacts referees only after submission, and the deadline for their letters is the same as
for the application. So the clock is already running and they may not know it.

Send each of them, today:
- the academic CV
- the motivation letter as submitted
- three lines on what would help most if they mentioned it

For **Prof. Hao Zhong**, ask specifically for the thing no one else can attest: which parts of the
thesis work were mine, and whether I can carry out empirical ML research independently. That is the
single most load-bearing claim in the file, because the degrees are in management.

For **Soukaina Hafidi**, note that she will learn from this that you are applying elsewhere. Better
heard from you first than from an automated ETH request.

### 2. ✅ DONE — LAS group email (step 2 of 2)

- **To:** `applications.las-group@lists.inf.ethz.ch`
- **Attach:** academic CV, `Outline_Krause_LAS.md` as PDF, WI2026 one-pager
- **Do not** cc Prof. Krause personally. The list is the stated channel.
- Draft is in `Email_Krause_LAS.md`; the "engineering at Amazon" error in it has been corrected.

⚠️ **Before attaching anything:** the WI2026 PDF carries an **"Amazon Confidential" MSIP label** in its
metadata (flagged in `papers/notes/WI2026_paper_summary.md`). Re-export a clean, unclassified copy.
Attaching an employer-classified document to an external application is a real problem, not a
formatting one.

⚠️ **Also fix everywhere:** the paper has **three authors** — Guidi, Rashid & Zhong. Earlier documents
said single-author. Any surviving single-author claim next to a three-author PDF is the worst kind of
discrepancy.

---

## Sent — kept for the reasoning

### 3. ✅ DONE — ODI (Prof. Niao He), via the form
- Google form: `https://forms.gle/JxarVvNgiy83SQpr9`
- Inquiries: `odi.ethz.recruitment@gmail.com`
- Outline already written: `Outline_NiaoHe_ETH.md`
- ODI is arguably the closer methodological fit (bias–variance–cost trade-off, constrained MDPs). Two
  applications to two groups in the same institute is normal, not duplicative — they read separately.

### 4. ✅ DONE — Eligibility pre-check
Sent to `phd@inf.ethz.ch`: whether a Master in Management is recognised for admission to the D-INFK
doctorate, and whether extended doctoral studies would apply. A neutral administrative query, not a
second application. **Administrative addresses usually do answer**, unlike research groups — so if there
is no reply by roughly 15 August, one polite follow-up is appropriate here (and only here).

### 5. ✅ RESOLVED 2026-07-29 — GitHub exposure, but it inverts into a different problem

Checked the live profile. `github.com/alexguidioff` has **two public repos only**: `Portfolio_DataScience`
(coursework ML, wine-quality classification) and the Hugo personal site. So `Idea_Falsification_Log.md`,
`Startup_Ideas.md`, `EF_startup_idea.md` and `docs/outreach/` are **not exposed**. No leak.

⚠️ **The opposite problem is now live.** Nothing that represents the actual research is public either, so
any application asking for code links has only a coursework portfolio to point at. That is worse than
"available on request". Fix and constraints (PitchBook data cannot be redistributed; SEC-derived code can)
are written up in `Form_AgenticSystemsLab.md`, along with three factual contradictions between
`alessandroguidi.site` and the CV that need correcting before the site is linked anywhere.

---

## Expectation management, stated plainly

`Group_Funding_DD.md` rates the response probability for Krause as **Low**, and that assessment is
accurate: he is an ACM and IEEE Fellow, chairs the ETH AI Center, and sits on the UN High-level Advisory
Body on AI. This is a low-probability, high-value application. Submit, then continue other tracks
rather than waiting.

Two other threads already open, per `Email_Krause_LAS.md`:
- **HSG 1092 (Prof. Tykvová)** — sent 9 July, no reply. Three weeks over Swiss academic holidays is not
  a rejection. Follow up **early September**, not August.
- **SMI** — the PhD posting is no longer live; three HiWi research-assistant roles remain, contacts
  `sherath@ethz.ch` and `rudolfm@ethz.ch`. The PDFs are dated 2024 — verify they are current first.

---

## What to do while waiting, and this is the real answer

Nothing in this list changes the outcome much. What changes it is the aptitude colloquium, which comes
within 12 months of provisional admission and requires defending a doctoral plan. That is also what
makes a supervisor want to take you.

The strongest use of the next months is therefore the research itself, and there was a specific gap worth
closing: the cost-aware policy failed its preregistered gates and nothing distinguished a misspecified
utility, an unprofitable cost regime, or a violation of the structural conditions licensing adaptive
greedy acquisition.

**✅ Closed 2026-07-29 by EXP-005** (`experiments/EXP-005/REPORT.md`). Summary: the third explanation was
withdrawn as a category error — submodularity governs sequential selection and this design acquires one
block under a binary decision. An oracle policy beats the strongest baseline by +0.065 to +0.087, so a
winning policy exists and the cost regime is not the constraint. The actual cause is that per-case gain
correlates with its prediction at +0.015 / −0.070 / +0.000, and it does so structurally: predicting
per-case gain is predicting the base model's residual, which is harder than the prediction task itself.

So this item is done, and it did not depend on a reply. What remains genuinely open on this page is
**item 1 (referees)** and **item 5 (GitHub exposure)** — note that item 5 now matters slightly more, since
`Idea_Falsification_Log.md` records ten dead commercial hypotheses that a reviewer following a repo link
should not be reading.

The next research question is no longer diagnostic but constructive: EXP-005 says the estimable quantity
is the **population-level** trade-off, so the natural follow-on is the budgeted-portfolio formulation
(P5) evaluated on tail-lift rather than average discrimination, per EXP-002.
