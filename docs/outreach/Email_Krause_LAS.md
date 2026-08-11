# LAS Application — email + submission checklist

**Status:** 📨 DRAFT — not yet sent
**Group:** Learning & Adaptive Systems (Prof. Andreas Krause), ETH Zurich D-INFK
**Verified:** las.inf.ethz.ch/openings and inf.ethz.ch doctoral pages, fetched 2026-07-28

---

## ⚠️ Why the previous ETH attempts got no reply

Both groups I contacted **do not accept direct email as an application channel**. This is almost
certainly why there was no response — the message never entered their process.

- **LAS** requires **two steps in parallel** (below). An email alone is not an application.
- **ODI (Niao He)** requires a Google form: `https://forms.gle/JxarVvNgiy83SQpr9`,
  inquiries to `odi.ethz.recruitment@gmail.com`. Email to her personally is not the channel.
- LAS states explicitly that they cannot respond to requests outside their stated programs.

**Do not repeat the mistake. Both LAS steps must be done, and step 1 matters more than step 2.**

---

## The two required steps

### Step 1 — D-INFK doctoral application (the one that counts)
- Portal: `https://www.lehrbetrieb.ethz.ch/BewDokFrontend/ealogin.view`
- **Application period is open all year — no deadlines.** Review is continuous.
- Two stages: (a) register a personal account — **a digital passport photograph is required**;
  (b) fill out the application form.
- Express interest in the Learning & Adaptive Systems group explicitly in the application.
- Questions: `phd@inf.ethz.ch` *(this is the portal's stated contact — not doctorate@inf.ethz.ch,
  which is the department's general doctoral-studies address)*
- Navigation warning from the portal: use "Continue"/"Back", not the browser back button.

### Step 2 — email the group
- **To:** `applications.las-group@lists.inf.ethz.ch`
  *(written on their site as "applications.las-group at lists.inf.ethz.ch" — anti-spam obfuscation)*
- **Attach:** academic CV, this outline (`Outline_Krause_LAS.md` → PDF), WI2026 one-pager
- Do **not** cc Krause personally. The list is the channel.

**Why this ordering matters:** the no-deadline D-INFK route is the only ETH channel compatible with
starting before March 2027. The AI Center and Max Planck CLS fellowships both start in September and
their portals are currently closed.

---

## Email draft

**Subject:** PhD application — decision-oriented information acquisition under costly, delayed tests

Dear Learning & Adaptive Systems Group,

I have submitted an application for doctoral studies at D-INFK expressing interest in your group, and
am writing to add a short CV and research outline as your application instructions request.

My interest is in decision-oriented information acquisition — acquiring enough information to make a
decision correctly rather than to identify a hypothesis precisely, in the sense of *Near-Optimal
Bayesian Active Learning for Decision Making* and the group's later work on submodular surrogates for
value of information.

What I would bring is a domain where that apparatus has not been tested and where its standard
assumptions bind hardest: private-market investment decisions, in which information is expensive and
slow to obtain, tests are correlated and partly unobservable, and the outcome arrives years later
under confounding. I have built a point-in-time pipeline on public SEC data that reconstructs what was
defensibly knowable at each decision time, with company-disjoint temporal splits and a locked test
cohort.

I should be direct about where it currently stands. A real information block is predictive, and
transports across cohorts. But my cost-aware acquisition policy **does not yet beat the preregistered
non-value-of-information baselines** on decision value net of cost. I do not know whether that is a
mis-specified utility model, a cost structure under which acquisition genuinely does not pay in this
regime, or a failure of the structural conditions that license adaptive greedy acquisition. Deciding
which of the three it is seems to me a methodological question rather than a finance one, and it is
the question I would want to work on.

My background is applied rather than theoretical. My degrees are in management, and my professional
roles have been in product management — currently at Amazon Business in Paris, previously consulting at
Capgemini — so the empirical and engineering work above is self-taught and self-directed. I am first
author on a paper accepted at the WI2026 Student Track (Business Informatics) on machine learning for
private-company valuation, with Saad Rashid and Prof. Hao Zhong. The theoretical depth is what I am
asking to acquire, and I would expect a domain co-advisor in entrepreneurial finance alongside
methodological supervision.

The outline, my CV, and a one-page summary of the accepted paper are attached. I would be grateful for
any assessment of fit, including a negative one.

With thanks for your time,

Alessandro Guidi
alexguidioff@gmail.com · alessandroguidi.site
linkedin.com/in/alessandroguidi1 · github.com/alexguidioff

---

## Notes on the draft

**Why lead with the negative result.** A methods group can verify the claim, and a hidden failure
found later costs more than an admitted one. It also converts a weak position ("my policy doesn't
work") into the actual research question ("why not, and under what conditions would it").

**Why not name Krause in the greeting.** The list is read by the group. Addressing him personally
where they asked for the list signals not having read the instructions — the exact failure mode that
sank the earlier attempts.

**Realistic expectation.** Krause is an ACM and IEEE Fellow, chairs the ETH AI Center, and sits on the
UN High-level Advisory Body on AI. `Group_Funding_DD.md` rates response probability as Low, and that
is accurate. Submit, then continue other tracks rather than waiting.

**Framing discipline.** P0 + P1 only, one hint of P2. No P3/P4/P5. No mention of the company —
`Startup_Ideas.md` stays out of academic outreach entirely.

---

## Pre-send checklist

- [ ] Verify all six LAS citations in the outline on las.inf.ethz.ch/publications
- [ ] Confirm ROC-AUC 0.6551 and the split sizes against `programme.yaml`
- [ ] Export `Outline_Krause_LAS.md` to PDF (2 pages max)
- [ ] Get a digital passport photograph ready for portal registration
- [ ] **Step 1 first:** complete the D-INFK portal application, naming LAS
- [ ] **Step 2:** email the list with CV + outline + WI2026 one-pager
- [ ] Log the submission date in `Group_Funding_DD.md`

## ⚠️ Prerequisite: eligibility pre-check

**Do not submit the portal application before the recognition question is answered.** My degrees
(MiM ESCP, BSc Business & Management) are not in computer science, and D-INFK invites applicants with a
Master's in CS *or a related field*. ETH's own procedure requires the central doctoral administration to
confirm that a candidate's studies are recognised **before** a professor can accept them — employment
follows only after provisional admission. See `Email_Gianesi_DINFK_Precheck.md`.

Possible outcome to expect: **extended doctoral studies** (additional graded credits for candidates
whose prior education does not cover the discipline). That is a route in, not a rejection.

## Related open actions

- **ODI (Niao He):** resubmit via the Google form — the earlier email was not the channel
- **SMI:** the PhD posting `JOPG_ethz_Haz6Toe6QaCjjkLESs` is **no longer live** (the smi.ethz.ch page
  is stale); three HiWi research-assistant roles remain listed, contacts `sherath@ethz.ch`
  (Python/R/Git) and `rudolfm@ethz.ch` (stats/econometrics, qualitative). PDFs are dated 2024 —
  verify they are current before applying.
- **HSG 1092 (Tykvová):** sent 9 July, no reply. Three weeks over Swiss academic holidays is not a
  rejection. Follow up early September, not August. The 10-working-day rule in
  `Group_Funding_DD.md` is too aggressive for July–August.
