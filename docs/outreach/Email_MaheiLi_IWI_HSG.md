# Email — Dr. Mahei Li, IWI-HSG

**Date drafted:** 2026-07-31
**To:** mahei.li@unisg.ch
**Institute:** Institute of Information Systems and Digital Business (IWI-HSG), University of St.Gallen
**Group:** Prof. Dr. Jan Marco Leimeister — Management of Agentic AI and GenAI in Organizations
**Trigger:** Job ID 2780, "Research Associate/PhD Candidate in Building and Scaling Agentic AI in
Organizations". Li is named on the posting for job-related questions, which is why he is the
correct recipient rather than Leimeister.

## Why this email exists, and why it is not an application to 2780

Two stated requirements of 2780 are not met, and pretending otherwise would waste both sides' time:

1. **German.** The posting requires excellent written and verbal German. Current languages are
   Italian (native), English C1 / IELTS 7.0, French B2. No German.
2. **Agentic stack.** The posting asks for production-quality software engineering plus hands-on
   LangChain/LangGraph, Agents SDKs, RAG, MCP/A2A. Actual stack is scientific Python
   (scikit-learn, XGBoost, SHAP, DuckDB, Playwright, Streamlit) and SQL. Applied ML and data
   engineering, not agentic systems engineering.

The GPA gate is met: minimum 5.0 on the Swiss scale, against 3.8/4.0 at ESCP (roughly 5.5-5.7).

So the email does not ask for that role. It asks whether the institute has a position or project
where an empirical profile on financial and decision data fits. This follows the outreach principle
already recorded in `docs/Professors.md`: do not ask for supervision or funding, ask whether the
work can become a research agenda.

## Positioning

IWI-HSG is design-oriented Information Systems research, and **WI is the flagship conference of
that field**. A paper accepted at WI 2026 is the single most relevant credential available here, and
it is stronger than anything in the finance framing used for HSG finance chairs. Lead with it.

## Wording discipline

Use the paper's own careful phrasing. `SUBMISSION_LOG.md` records three over-claims found on
`alessandroguidi.site`: "10,000+ companies" against the real 3,403; "under review" against
accepted; "beating the baselines" against the paper's actual wording. The email below says
**"competitive with, and more robust than"**, which is what the paper says.

The paper has **three authors: Guidi, Rashid and Zhong.** The email says co-author.

---

## The email

**Subject:** WI 2026 author — research fit at IWI-HSG (re: job ID 2780)

Dear Dr. Li,

You are named as the contact for job ID 2780, so I am writing to you rather than to Prof. Leimeister.

I am not applying for that position. It requires excellent German, which I do not have, and hands-on
experience with agentic frameworks and production engineering, which is not my stack. I would rather
say that plainly than send an application you would have to filter out.

I am writing because I publish in your institute's field. I am a co-author of a paper accepted at
**WI 2026** (Student Track), "A Data-Driven Decision Support System for Venture Capital Valuation":
a decision support system predicting private-company valuations from investor co-investment network
features, on 3,403 PitchBook-backed deals, benchmarked against DCF and comparables on an
out-of-time holdout spanning the 2022 correction. The models performed competitively with, and more
robustly than, the traditional baselines, and the SHAP analysis identified investor-syndicate
capacity as the dominant driver, which we read as evidence of information saturation.

Since then I have been working on two things that may be more relevant than the paper itself. First,
a point-in-time dataset for public equities built from scratch, with a documented bias audit:
survivorship, look-ahead and backfilled metadata treated explicitly, and features removed when
ablation showed they contributed nothing. Second, a preregistered study on cost-aware information
acquisition that **failed its own gates**, and where the useful output was a stated condition rather
than a positive result: selective acquisition requires per-case information gain to be more
predictable than the outcome itself, and it usually is not.

My question is simple. Is there a position or a project at IWI-HSG where an empirical profile on
financial and organisational decision data would be useful, and would German be a firm requirement
across the institute or only for roles with executive education exposure? If the answer to the
second is that it is firm everywhere, I would rather know now.

I hold an ESCP Master in Management (Corporate Finance / Financial Markets), conferred September
2026, and I am an EU citizen eligible to work in Switzerland. I have attached a one-page summary of
the WI 2026 paper and my academic CV.

Thank you for your time.

Kind regards,
Alessandro Guidi
+39 347 291 1103 · alexguidioff@gmail.com
linkedin.com/in/alessandroguidi1

---

## Before sending — checklist

- [ ] **Verify the WI 2026 PDF is the clean re-export**, not the copy carrying the "Amazon
      Confidential" MSIP label. Open `SUBMISSION_LOG.md`: this is flagged as unresolved and it is an
      employer-classification issue, not a formatting one.
- [ ] Confirm the attachment does **not** describe the paper as single-author.
- [ ] Do **not** link `alessandroguidi.site` until the three contradictions logged on 2026-07-29 are
      fixed.
- [ ] Attach exactly two files: `WI2026 article - One-Pager.pdf` and
      `Alessandro Guidi — Academic CV.pdf`. Not the thesis, not the professional CV.
- [ ] Confirm `mahei.li@unisg.ch` on the posting or the IWI-HSG staff page before sending.

## After sending

- Log it in `SUBMISSION_LOG.md` with the date.
- Expect silence to be the modal outcome; it is not information about the work.
- One polite follow-up is reasonable **in early September**, not in August: Swiss academic holidays,
  the same reason the Tykvová follow-up is already parked to September.
- If Li replies that German is firm institute-wide, that is a genuinely useful answer: it removes
  IWI-HSG from the map and redirects effort to Ademi, Borth, Gonon and Barbon, who sit in
  English-working finance and computer science groups at the same university.
