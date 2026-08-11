# Motivation — Doctorate in Computer Science, D-INFK, ETH Zurich

**Alessandro Guidi** · alexguidioff@gmail.com · alessandroguidi.site
github.com/alexguidioff · linkedin.com/in/alessandroguidi1

> **Status:** draft for the D-INFK doctoral application portal.
> **Group named in the application:** Learning & Adaptive Systems (Prof. Andreas Krause).
> Alternative/parallel: Optimization & Decision Intelligence (Prof. Niao He) via the ODI form.
>
> **Framing decision:** built on the master's thesis and the WI2026 paper. The SEC / Form D work is
> deliberately left out — it is unpublished, its headline result is negative, and it would spend the
> reader's attention on an apparatus rather than on completed, reviewed work. Numbers below are taken
> from `CV_Professional_Guidi.html`, not from notes.

---

## Version A — one page, for the portal's motivation field

I am applying to the doctoral programme at D-INFK because a result in my own master's research
convinced me that the question I had been asking was the wrong one, and the right one is a computer
science question.

My master's thesis at ESCP Business School, *A Data-Driven Decision Support System for Venture Capital
Valuation*, built an end-to-end machine learning pipeline to value private companies from
investor-syndicate network structure, funding history and market signals, on 3,403 PitchBook-backed
deals. I engineered graph features from investor co-investment networks — centrality, clustering,
syndicate overlap — and benchmarked ensemble models against DCF and comparables baselines on an
out-of-time holdout deliberately spanning the 2022 market correction. The best model performed
competitively with, and more robustly than, the traditional baselines (Random Forest R² = 0.557, MAE =
0.888). The work was accepted as a paper at the **WI2026 Student Track**, an information systems
conference (Guidi, Rashid & Zhong).

The finding that redirected me was not the accuracy figure. It was **which feature carried the
signal**: investor-syndicate capacity, measured as mean co-investor AUM, dominated every firm-level
financial feature. In other words, the model was largely reading *who had already decided to invest*
rather than any property of the company being valued. That is a useful empirical result and an honest
ceiling. Improving such a predictor further does not help the person who has to act, because they are
not short of a prediction — they are short of information, and information costs money and time to
obtain.

So the question I want to work on is the prior one: **given a decision under uncertainty, which costly,
delayed test should be run next?** This is decision-oriented information acquisition — acquiring enough
information to act correctly rather than to estimate a parameter precisely. It is squarely a computer
science question, with an existing apparatus in sequential decision making, Bayesian experimental
design, and value of information under budget constraints. My interest is in the regime where that
theory's assumptions bind hardest: tests that are expensive, correlated, partly unobservable, and whose
outcome arrives years later under confounding. Private capital markets are that regime, but the
formulation is domain-general — the same structure appears in credit, in M&A, and outside finance
entirely.

I have not only argued this. Since the thesis I have built, independently and outside any institutional
programme, a reproducible pipeline on public regulatory filings that reconstructs what was defensibly
knowable at each decision time, with company-disjoint temporal splits, a locked test cohort I have not
accessed, and programmatic assertions for disjointness and feature/outcome separation. It has produced
one clear negative result: a learned cost-aware acquisition policy fails to beat its preregistered
non-value-of-information baselines. I report that as a failure rather than reframing it, and I do not
know whether the cause is a misspecified utility model, a cost regime where acquisition genuinely does
not pay, or a violation of the structural conditions that license adaptive greedy acquisition.
Distinguishing between the three is a methods question, and it is the one I would want supervision on.

I should be plain about my background. My degrees are in management (MiM, ESCP; BSc Business &
Management), not computer science, and my professional roles have been in product management — currently
at Amazon Business in Paris, previously consulting at Capgemini. I hold no engineering title and do not
claim one. My programming, data engineering and experimental practice are self-taught and applied. I am
aware that my file may require a recognition assessment and possibly extended doctoral studies with
additional graded coursework; I would regard that as part of the work rather than an obstacle.

What I would bring is a completed piece of reviewed empirical research, an apparatus that already runs,
and the habit of declaring falsification thresholds before running an experiment. What I am asking for
is the theoretical depth I do not have, in the group where these methods live. I would be grateful for
an assessment of fit, including a negative one.

---

## Version B — condensed, if the portal field has a tight character limit

I am applying because a result in my own master's research convinced me the question I was asking was
the wrong one, and the right one belongs to computer science.

My ESCP master's thesis, *A Data-Driven Decision Support System for Venture Capital Valuation*, built an
ML pipeline valuing private companies from investor co-investment network features, funding history and
market signals across 3,403 deals, benchmarked against DCF and comparables on an out-of-time holdout
spanning the 2022 correction (Random Forest R² = 0.557, MAE = 0.888). It was accepted at the **WI2026
Student Track**, an information systems conference.

The decisive finding was not the accuracy but which feature dominated: investor-syndicate capacity, not
firm financials. The model was largely reading who had already invested. That is an honest ceiling for
the predictive framing — an investor is not short of a prediction, but of information, which costs money
and time.

Hence the question I want to work on: **which costly, delayed test should be acquired next, given a
decision under uncertainty?** Decision-oriented information acquisition, in the regime where its
assumptions bind hardest — expensive, correlated, partly unobservable tests with outcomes arriving years
later under confounding.

Since the thesis I have built, independently, a point-in-time pipeline on public filings with
company-disjoint splits, a locked untouched test cohort, and assertions enforcing disjointness and
feature/outcome separation. Its headline result is negative: a cost-aware acquisition policy does not
beat its preregistered baselines. Whether that is a misspecified utility, a cost regime where
acquisition does not pay, or a failure of the structural conditions licensing adaptive greedy
acquisition, I cannot currently tell — and that distinction is the methods question I want supervision
on.

My degrees are in management, not computer science; my roles have been in product management (Amazon
Business, previously Capgemini) and I hold no engineering title. The technical work is self-taught. I
accept that extended doctoral studies may be required.

---

## Portal field — Research interests

Multiple selections are permitted. **Select three, not more.** These tags route the file to reading
groups; selecting six makes no group feel addressed and reads as an applicant without a direction.

1. **Machine learning** — mandatory. Both target groups sit in the Institute for Machine Learning at
   D-INFK: Learning & Adaptive Systems (Krause) and Optimization & Decision Intelligence (He).
   Sequential decision making, Bayesian experimental design and value of information under budget
   constraints are classified here.
2. **Theory** — the differentiator. Whether the structural conditions licensing adaptive greedy
   acquisition (submodularity, or its absence) hold in this setting, and what regret guarantees survive
   when they do not, is optimisation theory. Selecting it signals interest in *why* the policy fails,
   not only in making it work.
3. **Databases and information systems** — include only because three slots are available. The WI2026
   paper was accepted at an *information systems* conference, so this tag makes the track record
   consistent with the stated interests.

**Revision note:** an earlier version of this file advised *against* selecting "Databases and
information systems". That advice held when only one or two selections were possible, where it would
have diluted the signal and routed the file toward data-management groups. With three slots it earns its
place through the IS venue. If the portal allows only two, drop it and keep Machine learning + Theory.

**Do not select**, despite apparent adjacency:
- *Computational science* — scientific simulation, not decision theory.
- *Human-computer interaction* — would only apply to the investment-committee study (P3), which is not
  part of this application.
- *Natural language processing*, *Computer vision* — unrelated to the question.

---

## Portal field — Additional relevant information

*Free-text field. Purpose: evidence the claims, pre-empt the recognition question, and keep everything
checkable. Trim from the bottom if the field is shorter than this.*

**Reviewed research output.** First-author paper accepted at the WI2026 Student Track — an information
systems conference — titled *Can Non-Financial Signals Price Private Companies?* (Guidi, Rashid &
Zhong), derived from my master's thesis at ESCP Business School. Out-of-time holdout across the 2022
correction on 3,403 deals; Random Forest R² = 0.557, MAE = 0.888, competitive with and more robust than
DCF and comparables baselines. Manuscript and code available on request.

**Master's thesis.** *A Data-Driven Decision Support System for Venture Capital Valuation* (2025–2026),
ESCP Business School, Paris/Turin. End-to-end pipeline: graph feature engineering over investor
co-investment networks (centrality, clustering, syndicate overlap), ensemble models (Random Forest,
XGBoost) with SHAP attribution, benchmarked against financial baselines.

**Independent research since the thesis.** A reproducible point-in-time pipeline over public regulatory
filings with company-disjoint temporal splits, an untouched locked test cohort, and programmatic
assertions enforcing disjointness and feature/outcome separation. It reports its own negative result
against preregistered baselines. Available for inspection; github.com/alexguidioff.

**On the degree-recognition question.** My Master's is in management (MiM, ESCP Business School), not
computer science, so I expect a recognition assessment and possibly extended doctoral studies with
additional graded credits. I raise it here rather than leaving it to be discovered, and I would accept
extended studies.

**Professional background, stated precisely.** Product management, not engineering: currently EU5 3P
Product Manager at Amazon Business, Paris (apprenticeship within the ESCP MiM programme), previously
consulting at Capgemini. I have owned product strategy and data-driven workflow redesign; I have never
held a software engineering title and do not claim one. All technical research work is self-taught and
self-directed.

**Supervision sought.** Methodological depth in sequential decision making and information acquisition,
with a domain co-advisor in entrepreneurial finance. I have contacted HSG (Prof. Tykvová) regarding the
domain side.

**On earlier contact with ETH.** I previously wrote directly to two ETH groups by email. I have since
understood that direct email is not an application channel for either, which is why this is the first
properly submitted application. I mention it so that any record of those messages is not read as a
repeated approach through the wrong route.

**Availability and language.** Available from **September 2026**, on conferral of the Master in
Management. English C1 (IELTS 7.0), Italian native, French B2; willing to take German coursework if
required.

---

## Portal field — "What have you been doing since the last degree?"

*Covers September 2022 to present. The explanation of the four-year span is the substantive part: a
two-year programme extended by a deliberate pause, not a delay.*

Since completing my Bachelor's in Business & Management at the University of Turin in September 2022
(110/110 summa cum laude), I have been enrolled in the Master in Management at ESCP Business School
(GPA 3.8/4.0), which I will complete in September 2026.

**On the length of the programme.** The ESCP Master in Management is a two-year degree. My enrolment
spans four years because I deliberately interrupted my studies to work full-time in consulting rather
than progressing straight through. I joined Capgemini Technology Consulting in Milan (September 2023 –
August 2025) to build substantive experience in financial services before returning to complete the
degree — delivering financial modelling and process reengineering for Tier-1 banking clients in highly
regulated environments, contributing to approximately €2M in documented cost savings. That choice was
made for depth of domain experience, and it is what allowed me to formulate the research question I am
now applying with: I had seen how these decisions are actually made before I tried to model them.

**Since September 2025** I have been EU5 3P Product Manager at Amazon Business in Paris, an
apprenticeship position within the ESCP programme, owning product strategy for onboarding strategic B2B
sellers across five European markets.

**Research during this period.** My master's thesis, *A Data-Driven Decision Support System for Venture
Capital Valuation* (2025–2026), built an end-to-end machine learning pipeline valuing private companies
from investor co-investment network features, funding history and market signals across 3,403 deals,
benchmarked against DCF and comparables baselines on an out-of-time holdout spanning the 2022 market
correction (Random Forest R² = 0.557, MAE = 0.888). It was accepted as a paper at the **WI 2026 Student
Track** (Business Informatics).

Independently and alongside these commitments, I have continued the line the thesis opened: a
reproducible point-in-time pipeline over public regulatory filings, with company-disjoint temporal
splits and a locked test cohort, to study decision-oriented information acquisition. It has produced a
preregistered negative result, which I report as such rather than reframing it.

**Also in this period:** progressed from Consultant to President at 180 Degrees Consulting Turin
(September 2022 – July 2025), and obtained the PMP certification (2025).

**Availability:** September 2026, on conferral of the Master in Management.

---

### ⚠️ Two facts to handle deliberately, not to hide

1. **The Master is not yet conferred.** Completion is scheduled for September 2026, so this application
   is submitted before conferral. ETH requires a Master's for the regular doctorate; admission would
   therefore be conditional on conferral. Because the D-INFK portal has no deadlines, waiting until
   September 2026 and applying with the degree in hand is a legitimate alternative that removes an
   administrative complication. Decide which route is preferable rather than defaulting.
2. **The four-year span on a two-year programme will be noticed.** It is better explained as a
   deliberate professional interruption — which it was — than left for a reader to interpret as a delay
   or a repeated year. The framing above states the reason and connects it to the research question.

---

## Notes on choices made in this draft

**Why the thesis leads and the regulatory-filings work is secondary.** The thesis and WI2026 paper are
finished and externally reviewed; the filings work is unpublished with a negative headline. Leading with
reviewed output and using the negative result to justify the *research direction* is stronger than
leading with an apparatus. The negative result still appears — hiding it would be worse — but as
motivation rather than as the main claim.

**Why the syndicate finding is the pivot.** It converts "I want to study value of information" from a
preference into a conclusion forced by evidence the applicant produced. A methods group can check the
reasoning: if the dominant feature is who already invested, then a better predictor is not what the
decision-maker lacks.

**Why WI2026 is named as an information systems conference.** A CS department will not recognise the
venue. Saying what it is prevents both overclaiming and silent undervaluation.

**Excluded deliberately.** P3, P4, P5 from `Research_Agenda.md`; any mention of commercialisation; the
`Idea_Falsification_Log.md` material.

---

## ⚠️ Accuracy note — a correction made during drafting

An earlier draft described the Amazon role as "software engineering". **That was wrong** — it was copied
from an internal note rather than checked against the CV. The actual role is EU5 3P Product Manager
(apprenticeship) at Amazon Business, Paris, from September 2025.

This matters beyond wording: an application to a computer science department that overstates an
engineering title is checkable in one search and would discredit every other claim in the file. The text
now deliberately understates — it states there is no engineering title and that the technical work is
self-directed.

**Rule: every biographical and numerical claim must be checked against `CV_Professional_Guidi.html` or a
primary artefact, never against notes or summaries.**

---

## Pre-submission checklist

- [ ] Confirm the exact WI2026 paper title and author order against the acceptance email
- [ ] Confirm the ESCP degree title exactly as written on the diploma
- [ ] Confirm thesis title and date range against the submitted thesis
- [ ] R² = 0.557 and MAE = 0.888 — confirmed against the CV; re-check against the manuscript
- [ ] 3,403 deals — confirmed against the CV; re-check against the manuscript
- [ ] Digital passport photograph ready for portal registration
- [ ] If the GitHub repository is public, verify `Idea_Falsification_Log.md`, `Startup_Ideas.md` and
      other private working documents are not exposed
- [ ] Name Learning & Adaptive Systems explicitly in the portal application
- [ ] After the portal step: email `applications.las-group@lists.inf.ethz.ch` with CV, outline and the
      WI2026 one-pager — do not cc Krause personally
- [ ] Correct the same "engineering at Amazon" error in `Email_Krause_LAS.md` before sending
- [ ] Separately, submit the ODI Google form if applying to He's group in parallel
