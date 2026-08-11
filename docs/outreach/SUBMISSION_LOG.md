# Submission log — ETH and related applications

One line per action, with the date. Kept because the previous two ETH attempts failed on *channel*
rather than on merit, and that only became visible once the history was written down.

---

## 2026-07-29 — D-INFK doctoral application + LAS group email

| Item | Detail |
|---|---|
| **Portal** | D-INFK doctoral application submitted, Learning & Adaptive Systems named |
| **Group email** | `applications.las-group@lists.inf.ethz.ch` — CV, outline (PDF), WI2026 one-pager |
| **Krause cc'd?** | No — correct; the list is the stated channel |
| **Research interests** | Machine learning (primary), Theory, Databases & information systems |
| **Referees entered** | Prof. Hao Zhong (ESCP, co-author/supervisor); Soukaina Hafidi (Amazon, line manager) |
| **Availability stated** | September 2026, on conferral of the ESCP Master in Management |
| **Documents used** | `Motivation_DINFK_Doctorate.md`, `Outline_Krause_LAS.html`, academic CV |

**Both LAS steps completed**, which is what the earlier attempts missed.

---

## 2026-07-29 — ODI (Prof. Niao He) + eligibility pre-check

| Item | Detail |
|---|---|
| **ODI application** | submitted via the Google form `https://forms.gle/JxarVvNgiy83SQpr9` |
| Documents used | `Outline_NiaoHe_ETH.html`, academic CV, WI2026 one-pager |
| **Eligibility pre-check** | query sent to `phd@inf.ethz.ch` — recognition of a management Master's for D-INFK doctoral admission, and whether extended doctoral studies would apply |

Three ETH channels now open on the same day: D-INFK portal (naming LAS), the LAS group list, and the
ODI form. All three used the channel each group actually specifies, which is the correction relative to
the earlier attempts.

**Note on applying to two groups in the same institute.** LAS and ODI read separately and both are in
the Institute for Machine Learning, so this is not duplication. The two outlines are deliberately framed
differently: LAS *built* the value-of-information apparatus, so that outline offers a domain where their
theory has never been stress-tested; ODI works on the bias–variance–cost trade-off and constrained MDPs,
so that outline frames acquisition as sequential optimisation under a budget. If both respond, the
framings are consistent — neither claims the other group's contribution.

---

## Open threads and when to touch them

| Thread | Status | Next action | When |
|---|---|---|---|
| D-INFK portal / LAS | submitted 2026-07-29 | nothing — **do not follow up** | — |
| ODI (Niao He) | submitted 2026-07-29 | nothing; `odi.ethz.recruitment@gmail.com` exists for inquiries but is not for chasing | — |
| Eligibility pre-check | sent 2026-07-29 | administrative queries do get answered; if silent, one polite follow-up | **~15 August** |
| **Referee letters** | requested by the portal on submission | confirm Zhong and Hafidi received the request and intend to submit | **within 3 days — the only item that can fail silently** |
| HSG 1092 (Tykvová) | sent 9 July, no reply | follow up — **not** in August, Swiss academic holidays | early September |
| SMI | PhD posting no longer live | verify the three HiWi roles are current (`sherath@ethz.ch`, `rudolfm@ethz.ch`); PDFs dated 2024 | if other tracks stall |
| GitHub exposure | ✅ checked 2026-07-29 — **no leak**, only 2 public repos and neither is this work | inverse problem: no public artefact represents the research. Publish a scoped SEC-only repo | before any form asking for code links |
| `alessandroguidi.site` accuracy | ⚠️ **3 contradictions vs CV** found 2026-07-29 | "10,000+ companies" vs 3,403; "under review" vs WI2026 accepted; "beating the baselines" vs the paper's wording. Details in `Form_AgenticSystemsLab.md` | **before linking the site anywhere** |
| Agentic Systems Lab form | Q1 drafted 2026-07-29 | `Form_AgenticSystemsLab.md` | in progress |
| WI2026 PDF metadata | unresolved? | confirm the copy actually attached was the clean re-export, not the one carrying the "Amazon Confidential" MSIP label | **check now** |

⚠️ **Two things to verify retroactively, since the documents are already out:**
1. Whether the WI2026 PDF attached to the LAS email was the clean re-export. If the labelled version
   went out, that is worth knowing now rather than discovering later — it is an employer-classification
   issue, not a formatting one.
2. That no attachment still describes the paper as single-author. It has three authors: Guidi, Rashid &
   Zhong.

---

## Expectation, recorded now rather than rationalised later

`Group_Funding_DD.md` rates the probability of a Krause response as **Low**, and that is an accurate
assessment: ACM and IEEE Fellow, chairs the ETH AI Center, sits on the UN High-level Advisory Body on
AI. This is a low-probability, high-value application.

Silence is the modal outcome and is not information about the quality of the work. **Do not follow up
with LAS.** They state they cannot respond to requests outside their process; a reminder email would be
the same error that sank the first two attempts, in a new form.

---

## The thing that actually moves the outcome

Admission is provisional until the aptitude colloquium, within 12 months, where a doctoral plan is
defended. That is also what makes a supervisor want to take someone.

The open question in the file was the one a methods group asks first: the cost-aware policy fails its
preregistered gates, and nothing distinguished (a) a mis-specified utility model, (b) a cost regime where
acquisition does not pay, from (c) failure of the structural conditions licensing adaptive greedy
acquisition.

### ✅ Answered 2026-07-29 — EXP-005

`experiments/EXP-005/REPORT.md`. Thresholds declared before running; nothing adjusted afterwards.

- **(c) was withdrawn as a category error, not tested.** Adaptive submodularity licenses greedy
  selection over a *sequence*; EXP-001C acquires one block under a binary decision. With no sequence
  there is nothing for the condition to constrain. Carrying it as a live hypothesis was my mistake.
- **It is not (a) or (b) either.** An oracle policy that acquires where the *realised* gain exceeds cost
  beats the strongest baseline by **+0.065 to +0.087**, six to nine times the declared 0.010 margin. A
  winning selective policy exists; the cost regime is not the constraint.
- **The failure is that per-case gain is unpredictable.** Pearson correlation between predicted and
  realised gain: +0.015, −0.070, +0.000. **13 of 15 cells are model-side, 2 problem-side, zero wins.**
- **And it is unpredictable for a structural reason, not a tuning one.** Predicting per-case gain means
  predicting whether the base model errs on that case, i.e. predicting its residual, i.e. predicting the
  outcome better than the model does. Circular. Stateable in general: *selective acquisition requires
  per-case gain to be more predictable than the outcome, and it usually is not.*

**Why this is a better thing to have in the file than a passing gate.** It converts a failed
preregistration into a named condition with an oracle bound proving the condition is what binds, plus a
correction of my own framing. That is the interrogation the two documents said was missing, and it did
not depend on anyone replying.

**What it does to the plan:** P1's flagship claim pivots per its own falsification clause (see
`Research_Agenda.md`); P5 is strengthened, since a budgeted portfolio needs the population-level
trade-off, which is exactly the estimable quantity here.
