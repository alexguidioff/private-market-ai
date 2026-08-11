# Email — Prof. Dr. Ivo Blohm, IWI-HSG

**Date drafted:** 2026-07-31
**Institute:** Institute of Information Systems and Digital Business (IWI-HSG), University of St.Gallen
**Group:** Research group of Prof. Dr. Ivo Blohm — business analytics and hybrid creativity.
Heads the Competence Center Crowdsourcing at IWI-HSG.
**Replaces:** the drafted email to Dr. Mahei Li (`Email_MaheiLi_IWI_HSG.md`). Do not send both.

> ⚠️ **Two corrections, 2026-07-31.**
> 1. The paper title in the second paragraph was **wrong** in the first version of this draft. The
>    real title is *"Can Non-Financial Signals Price Private Companies? A Machine Learning Approach
>    to Startup Valuation"* (Guidi, Rashid & Zhong). Fixed below.
> 2. **Demoted to priority 6** by the backward derivation in `phd-svizzera/dal-dopo-al-prima.md`.
>    Blohm passes on industry funding and reachability but is weak on domain: he studies
>    organisations and platform/crowdsourced data, the object here is asset valuation from
>    proprietary financial databases. **Send Ademi first.** This one is a September item, if at all.

## Why Blohm and not the other three IWI-HSG chairs

| Chair / group | Stated focus | Fit |
|---|---|---|
| **Ivo Blohm** (research group) | business analytics, hybrid creativity; data science on platform data to improve decision-making; Competence Center Crowdsourcing | **best by a wide margin.** ML applied to investment and funding decisions is his actual output |
| Jan Marco Leimeister (chair) | crowdsourcing, service engineering, digital business, now Management of Agentic AI | biggest name, worst fit for this agenda. Job 2780 sits here |
| Reinhard Jung (chair) | health information systems, digital nudging, business ecosystems | health IS is the core. Weak |
| Andrea Back (chair) | digital strategies, transformation, innovation | least quantitative of the four. Weakest |

Verified from his own ResearchGate profile: *"I research how organizations can leverage data science
and business analytics in organizations with (crowdsourced) data from digital platforms in order to
improve decision-making, collaboration, and innovation."*

Verified from two independent author bios (INFORMS, FEPS): heads the **Competence Center
Crowdsourcing** at IWI-HSG, bundling publicly and industry-funded projects on crowdfunding,
crowdsourcing, open innovation, data science and the Internet economy.

Structural note: he is listed as **research group**, not chair. That usually means associate or
assistant level, which is the level that replies to email and needs people. The opposite of the
Krause bet.

## ⚠️ One thing to verify before sending

A paper titled **"It's a Peoples Game, Isn't It?! A Comparison Between the Investment Returns of
Business Angels and Machine Learning Algorithms"** surfaced as the top result on a Blohm-specific
query. Its question, whether ML algorithms make better early-stage investment decisions than humans
and why, is almost exactly the question of the WI 2026 paper.

**Authorship not confirmed.** SAGE returned 403 and a follow-up search went off target.

→ **Check HSG Alexandria for his publication list and confirm before citing it.** If he is an author,
the paragraph marked `[[IF CONFIRMED]]` below is the strongest sentence in the email. If he is not,
delete that paragraph and send the rest. Citing a paper someone did not write is the one error that
ends the conversation immediately.

## What changes relative to the Li draft

- **Do not mention German.** It was a requirement of job 2780, tied to executive education in
  Leimeister's chair. Blohm publishes in English. Opening with a limitation nobody asked about is
  self-sabotage. If he asks, answer honestly then.
- **Do not mention job 2780.** Different chair. Referencing it invites the reply "that role needs
  German" and closes the thread on the wrong question.
- **Lead with the research overlap, not with what you cannot do.**

---

## Revision 2 — anchored on the group's own stated research areas

The group page states three areas: **Hybrid Intelligence** (*"how experience and AI can be combined
in the best possible way"*), **Business Analytics**, and **Crowdsourcing**. The group's overall
statement names *"innovation and software development, entrepreneurship and digital work"* as focus
areas.

This changes the anchor for the better. **Hybrid Intelligence is the exact frame of the EXP-005
result**, and citing the group's own published framing removes the need to cite the business-angels
paper whose authorship could not be confirmed. Safer and more specific at the same time.

The reframing of EXP-005 for this audience: deciding when a model should stop, defer to a human, or
buy more information requires predicting where the model is wrong, which is harder than being right.
That is the deferral problem at the centre of hybrid intelligence, stated as a condition with an
oracle bound showing the condition is what binds.

## The email

**Subject:** WI 2026 paper on ML for VC valuation — a hybrid intelligence result, and a question

Dear Professor Blohm,

I am a co-author of a paper accepted at **WI 2026** (Student Track), and I am writing because of your
group's work on hybrid intelligence and on entrepreneurship, which is where my last two years of
work has ended up pointing.

The paper, "Can Non-Financial Signals Price Private Companies? A Machine Learning Approach to
Startup Valuation" (with S. Rashid and H. Zhong), predicts private-company valuations from
firmographic, deal-context and investor-syndicate features on 3,403 PitchBook deals, benchmarked
against financial baselines on an out-of-time holdout spanning the 2022 correction. The models performed competitively with, and more robustly than, the traditional
baselines. What interests me is not the accuracy but the SHAP attribution: investor-syndicate
capacity, measured as mean co-investor AUM, dominates the financial features. We read that as
evidence of information saturation, which is a statement about how much more information is worth
acquiring rather than about model quality.

That question is what I have worked on since, and it produced a negative result I think is the more
useful of the two. I preregistered a study on cost-aware information acquisition: given a budget,
which diligence step should a decision-maker take next. **It failed its own gates.** An oracle policy
that acquires only where the realised gain exceeds cost beats the strongest baseline by six to nine
times the declared margin, so a winning selective policy exists and the cost regime is not the
constraint. The correlation between predicted and realised per-case gain, however, is essentially
zero. The reason is structural rather than a matter of tuning: predicting the gain from acquiring
information means predicting whether the model errs on that case, which means predicting the outcome
better than the model does.

Stated generally, and this is where it touches your hybrid intelligence work: **selective acquisition,
and by the same argument selective deferral to a human, requires per-case gain to be more predictable
than the outcome itself, and it usually is not.** I would be glad to be shown where that is already
known, or wrong.

Alongside this I built a point-in-time dataset for public equities from scratch, with a documented
bias audit: survivorship, look-ahead and backfilled metadata handled explicitly, and features removed
when ablation showed they contributed nothing.

I am not writing to ask for supervision. I would like to know whether this line of work could become
something in your group, whether that is a research assistant position, a doctoral project, or a
collaboration on an existing funded project.

I hold an ESCP Master in Management (Corporate Finance / Financial Markets), conferred September
2026, with a 3.8/4.0 GPA, and I am an Italian and therefore EU citizen, eligible to work in
Switzerland. I have attached a one-page summary of the WI 2026 paper and my academic CV.

Thank you for your time.

Kind regards,
Alessandro Guidi
+39 347 291 1103 · alexguidioff@gmail.com
linkedin.com/in/alessandroguidi1

---

## Before sending

- [ ] **Confirm his direct email on the IWI-HSG staff page.** The group page lists only
      `christina.brem@unisg.ch`, which is the institute contact, not him. HSG format is usually
      `firstname.lastname@unisg.ch`, so `ivo.blohm@unisg.ch` is likely, but verify rather than guess.
      If only the institute address is findable, write to Brem asking her to forward, and say why.
- [ ] Read **two** of his papers on hybrid intelligence or business analytics, so a reply can be
      answered substantively within a day. This is the step your own `Professors.md` sets as
      mandatory before any outreach, and the email now claims familiarity with his research areas.
- [ ] Optional and only if verified: the business-angels-versus-algorithms paper. If HSG Alexandria
      confirms he is an author, one sentence naming it strengthens the second paragraph. If not
      confirmed, leave it out. The email no longer depends on it.
- [ ] **Verify the WI 2026 PDF is the clean re-export**, not the copy carrying the "Amazon
      Confidential" MSIP label. `SUBMISSION_LOG.md` flags this as unresolved.
- [ ] Confirm the attachment does not describe the paper as single-author. Three authors: Guidi,
      Rashid and Zhong.
- [ ] Do not link `alessandroguidi.site` until the three contradictions logged 2026-07-29 are fixed.
- [ ] Attach two files only: `WI2026 article - One-Pager.pdf` and
      `Alessandro Guidi — Academic CV.pdf`.

## After sending

- Log in `SUBMISSION_LOG.md` with the date.
- No follow-up in August, Swiss academic holidays. Early September if silent, same rule already
  applied to Tykvová.
- Do **not** also write to Mahei Li or to Leimeister. Two emails into one institute with the same
  framing reads as scattershot. The LAS and ODI double-submission was defensible only because the
  two outlines made genuinely different claims; that does not apply here.
