# Agentic Systems Lab (ETH D-MTEC) — application form answers

**Started 2026-07-29.** Lab: Agentic Systems Lab, Chair of Information Management (Fleisch / Wortmann).
Co-directors thanked by every pre-doc: **Kevin O'Sullivan** and **Robert Jakob**. Batch 2 open.

**Framing rules for this form** (carried over from the outreach email, deliberately):
- Stay in **finance / private markets**. Do not cite the agentic PR-review work.
- No em dashes.
- Their stated verticals include **Agentic AI in Finance** and **AI Evaluation Frameworks**. The second
  is the strongest bridge for the negative result, and it is an honest framing rather than a stretch.
- The paper has **three authors** (Guidi, Rashid & Zhong). The thesis is sole-author. Keep these separate
  in every sentence, since the earlier email already made that distinction explicitly.

---

## Q1. "Tell us about a project (or several) you have led or contributed to that you are especially proud of. If available, please include links to code, demos, or documentation."

**1. Can Non-Financial Signals Price Private Companies? (accepted, WI2026 Student Track)**

Co-authored with S. Rashid and Prof. H. Zhong. It grew out of my master's thesis at ESCP, which I wrote
as sole author. The question was whether private companies can be priced without financial statements.
On 3,403 PitchBook deals, under an out-of-time holdout deliberately placed across the 2022 valuation
correction, non-financial signals priced companies competitively with the strongest financial baseline
(RF R² 0.557, MAE 0.888), and SHAP attribution identified investor-syndicate capacity as the dominant
signal among those tested. The part I am proud of is the holdout choice. Testing across a regime break
rather than on a random split is the difference between a result and an artefact, and it cost us the
nicer numbers we would have reported otherwise.

**2. A point-in-time evaluation framework for information acquisition (ongoing, solo)**

The paper convinced me the predictive framing answers the wrong question. An investor does not buy a
prediction, they buy information that changes a decision. So I built a point-in-time pipeline on public
SEC filings, US technology issuers with non-amendment Form D anchors, which reconstructs only what was
observable at the decision date. Company-disjoint temporal splits, and the 2023 cohort locked and
untouched.

I then preregistered a cost-aware acquisition policy against five baselines, scored on decision value
net of information cost rather than on accuracy. It lost all 15 declared utility-by-cost cells. Instead
of tuning it, I built an oracle bound that acquires wherever the realised gain exceeds cost. The oracle
beats the strongest baseline by 0.065 to 0.087, six to nine times my declared margin, which proves a
winning policy exists and that the cost regime is not the obstacle. The selector is. The reason turned
out to be structural rather than a tuning failure: per-case gain is the base model's residual, so
predicting it means beating the base model at its own task. Correlation between predicted and realised
gain across the three utilities: +0.015, -0.070, +0.000.

That negative result is the piece I am proudest of. It converts a failed preregistration into a
stateable condition on when selective information acquisition can work at all, and I found it by
building the instrument that would break my own claim rather than waiting for a reviewer to do it.

**Links:** [see the blocking issue below before pasting anything]

---

## ⚠️ The links are currently a liability, and the form asks for them explicitly

Checked 2026-07-29.

### github.com/alexguidioff has two public repos, and neither is this work

| Repo | Content | Effect if linked here |
|---|---|---|
| `Portfolio_DataScience` | six coursework ML projects, "from wine quality classification to startup-style customer satisfaction prediction", 0 stars | invites the reviewer to treat a wine-quality notebook as the representative code sample |
| `alessandro.guidi.site` | Hugo personal site | neutral |

**Good news, and it closes an open thread:** `Idea_Falsification_Log.md`, `Startup_Ideas.md`,
`EF_startup_idea.md` and `docs/outreach/` are **not exposed**. Item 5 of
`NEXT_STEPS_after_DINFK_submission.md` can be marked resolved.

**Bad news:** a form that asks for code, answered with a link to a coursework portfolio, is worse than
answering "available on request". The described work has no public artefact.

### Recommended fix, in priority order

1. **Publish a scoped new repo** (not the existing one) containing the point-in-time pipeline, the
   experiment scripts, `EXP-005/REPORT.md` and `results.json`. This is the single highest-value action:
   it is exactly what an "AI Evaluation Frameworks" vertical wants to see, and the preregistration plus
   oracle bound reads better in code than in prose.
   - **Include:** SEC-derived code and outputs. SEC data is public, so no licensing problem.
   - **Exclude:** PitchBook data. It is licensed and cannot be redistributed, so the WI2026 dataset stays
     private and only the paper's numbers are cited.
   - **Exclude:** `Idea_Falsification_Log.md`, `Startup_Ideas.md`, `EF_startup_idea.md`, `docs/outreach/`,
     `Research_Agenda.md`. Commercial strategy and rejected hypotheses are not what a reviewer should find.
2. If there is no time for step 1, write "code and point-in-time pipeline available on request" and link
   only the paper and the site. **Do not link `Portfolio_DataScience`.**

### The personal site contradicts the CV in three places

This matters because the form invites a link, and a reviewer can hold the site and the paper side by side.

| Claim on alessandroguidi.site | Verified fact | Severity |
|---|---|---|
| "**10,000+** VC-backed companies" | **3,403** PitchBook deals (CV, paper) | **high** — a direct numerical contradiction |
| "two papers **under review** at ICIS 2026 and WI 2026" (repeated 4x) | WI2026 is **accepted**. ICIS status not verified anywhere in this repo | **high** — understates the accepted paper and asserts an unverified second one |
| "**beating** the baselines on early-stage valuation" | "competitively with, and more robustly than" the strongest financial baseline | medium — overclaim relative to the paper |
| no co-authors named | three authors: Guidi, Rashid & Zhong | medium — same single-author discrepancy already flagged for the LAS attachments |

**Also worth a decision, not a correction.** The site's headline counters are "HOURS SPENT ON EXCEL" and
"DUCKS APPROVED THIS SITE", and the copy is written in game language ("quest", "final boss", "party of
Sales, Tech, Legal and Ops"). For a product-manager audience this works. For a lab screening research
capability, Excel hours as a headline metric and a live feed surfacing a wine-quality notebook are
arguing against the answer above. Either fix the site before linking it, or link the paper only.

---

## Open items for the rest of the form

- [ ] Publish the scoped repo, or decide on "available on request"
- [ ] Fix 10,000+ to 3,403 on the site
- [ ] Fix "under review" to "accepted" for WI2026; verify ICIS 2026 status before repeating it anywhere
- [ ] Soften "beating the baselines" to the paper's own wording
- [ ] Name the co-authors on the site
- [ ] Google Scholar profile (still open from `Research_Log.md`)
- [ ] Confirm the WI2026 PDF used anywhere here is the clean re-export without the "Amazon Confidential" label

---

## Q2. "If you had no constraints, what kind of agentic AI system would you build?"

> **Trap avoided, and it is worth stating why.** The natural answer here is "an agent that decides what
> to retrieve next, case by case". That is **precisely the design EXP-005 falsified**: per-case gain is
> the base model's residual, so an agent claiming to know which single document will change its mind is
> claiming to beat itself. Answering that way would contradict Q1 in the same form. The answer below
> takes the constraint I measured and makes it a design commitment, which is a stronger position than
> not knowing about it.
>
> **Hook into their work:** the lab's Next-Gen RAG line is autonomous retrieval planning. This answer is
> that question with the economics and the leakage control attached, so it lands inside their agenda
> rather than beside it.

I would build a diligence agent whose central capability is knowing when to stop looking. Three
components, and the first is the one I care about most.

**A point-in-time retrieval layer.** Retrieval-augmented systems evaluated against historical decisions
usually leak the future, because the index contains documents published after the decision date. The
agent retrieves the analyst note written six months later and looks brilliant. I have already built this
layer for SEC filings, so the agent sees only what a decision maker could have seen at time t. Without
it, evaluating an agent on past decisions measures hindsight and reports it as skill.

**Retrieval as a costed action with a stopping rule.** Every retrieval carries a price and a delay, and
the objective is decision value net of that cost rather than answer quality. The question shifts from
what to retrieve to whether the next retrieval is worth its cost, and if it is not, to deciding now and
saying so.

**An evaluation harness as a first-class component.** This is what my own negative result taught me. I
built an acquisition policy that looked entirely reasonable and turned out to select at chance, and the
only way I could prove it was by constructing an oracle bound to compare against. So the system ships
with the instrument that distinguishes a real acquisition policy from a random one, because without it
you cannot tell, and a plausible-looking agent is the easiest thing in the world to build.

One design commitment follows from what I measured rather than what I hoped. The acquire-or-stop decision
belongs at the portfolio level, not per case. I would build the version that allocates a finite
information budget across a pipeline of decisions and abstains loudly when the information does not
support a call, rather than the version that promises per-case insight I now have evidence is not there.

*(~300 words. If the form has a tighter limit, cut the third component's last sentence and the closing
paragraph's final clause.)*

---

## Q2 — alternative considered and rejected: "continuously match startups to the possibility of raising"

Considered 2026-07-29 as a replacement answer for Q2. **Rejected as an answer, with one reformulation
that survives.** Recorded so it is not re-proposed.

### Four reasons it fails as written

1. **It contradicts Q1 in the same form.** "Continuously match the possibility of raising" is a
   readiness score plus a ranking of counterparties, i.e. a prediction engine. Q1 opens by saying the
   predictive framing answers the wrong question. Submitting both means arguing against prediction on one
   line and proposing it on the next.
2. **My own paper undercuts it.** WI2026's finding is that investor-syndicate capacity (mean co-investor
   AUM) is the dominant signal among those tested, which we read as information saturation. If who is
   already in the syndicate dominates, a matching engine largely re-derives existing network position. It
   tells a founder with a weak network that they have a weak network, which is true, already known, and
   not actionable on the timescale of the decision.
3. **Feedback loop makes it unevaluable, and the signals are gameable.** If the system says "you can
   raise now" and investors act on it, the signal causes the outcome, so it cannot be validated on
   history and cannot be validated live without contaminating the control. Worse, the inputs (hiring
   pace, web presence, filing timing) are cheap to manipulate the moment the score matters. This is
   exactly the P4 gaming-robustness problem, and here it is not a research topic but a product-killing
   defect.
4. **Saturated, and recently.** A single search surfaced at least six products doing readiness scoring
   plus investor matching inside the last eight months: [Evalyze](https://somi.ai/products/evalyze) with
   a 350 to 850 readiness score and an
   [investor matching engine launched December 2025](https://www.globenewswire.com/news-release/2025/12/05/3200960/0/en/Evalyze-Launches-AI-Investor-Matching-Engine-to-Help-Startups-Fundraise-Faster.html),
   [Cogently Pitch Partner](https://markets.businessinsider.com/news/stocks/cogently-launches-ai-pitch-partner-that-gives-founders-a-vc-grade-deck-audit-in-less-than-30-seconds-and-lets-them-rehearse-the-boardroom-pitch-before-it-s-real-1036371752),
   [VC Boom](https://productcool.com/product/vc-boom), [IQ Pitch](https://iqpitch.com/) and
   [Beacon Score](https://score.raisebeacon.com/). *Content rephrased for compliance with licensing
   restrictions.* Proposing it to a lab whose co-directors screen AI product ideas for a living invites
   the obvious question.

### The reformulation that does survive

Drop the match, keep the timing. The interesting object is not which investor fits, it is **when a
founder should go to market, and what they should go find out or build first**. That is a stopping
problem, not a prediction: acquisition of costly information under a budget, with the founder as the
decision maker acting on their own state. It is the P1 apparatus pointed at the **founder side**, which
is genuinely less studied than investor-side screening, and it partly escapes objection 3 because the
agent advises the party whose own information it is reading rather than broadcasting a score to the
market.

It also makes the setting **two-sided**, which is a real research object: both sides pay to learn about
each other, and each side's acquisition changes what the other should acquire. That is a harder and more
interesting problem than either side alone, and nothing in the VoI literature I have read addresses it.

**Verdict:** keep the drafted Q2 answer. Hold this reformulation for a later question if the form asks
about research directions, where the two-sided framing is an asset rather than a contradiction.

---

## Q3. "What do you see as a key challenge or limitation in building agentic AI systems, and how might you begin to address or explore it?"

> **Distinct from Q2 on purpose.** Q2's failure mode is "you cannot tell a good acquisition policy from a
> random one". Q3's is one level worse: "the benchmark itself is circular, so it reports a perfect score".
> The two do not overlap and should not be merged if the form is read as a whole.
>
> **Facts verified before use** (`Idea_Falsification_Log.md`, EXP-006): first run reported 100% attribute
> agreement on same-entity pairs; attributes were looked up by CIK while a positive pair is *defined* as
> two names sharing a CIK; 1770/1770 positive pairs resolved to a single CIK; re-keying on `(cik, name)`
> dropped agreement to 87–96%. Third circularity caught in the project, after 846 overlapping CIKs in
> EXP-002. The third instance is in the agentic PR work and is deliberately not cited here.

The limitation I keep hitting is that agentic systems are increasingly graded by other models, on
benchmarks their own pipeline helped produce. The dangerous failure is not that the agent is wrong. It is
that the evaluation is circular and returns a clean score, so nobody looks again.

I have done this to myself and caught it, which is why I pick it. Building an entity-resolution benchmark
on SEC filings, my first run reported 100% agreement on same-entity pairs. I did not believe the number
and probed it. Attributes were being looked up by company identifier, while a positive pair was *defined*
as two names sharing that identifier. Both sides returned the same record, so agreement was guaranteed:
1770 of 1770 positive pairs resolved to a single identifier. The label was the lookup key. Re-keying so
that each side is described only by the filings carrying its own name string, which is the information a
real system would have, dropped agreement to 87 to 96 percent. A plausible number instead of a tautology.

That is structurally the same defect as an LLM judge scoring an answer against a document the retriever
chose, or an agent generating the test cases it is then measured on. The grader's information path and
the label's information path are not disjoint, and the score silently measures the overlap.

How I would begin. First, make the information path of the label and of the system explicit and check
disjointness, as a stated artefact rather than an assumption. Second, treat a suspiciously clean score as
a symptom to investigate rather than a result to report, which is the only reason I caught mine. Third,
run the cheap ablation: permute or remove the suspected shared key and see whether the metric collapses.
If a metric does not move when you corrupt the thing it supposedly depends on, it was never measuring
that thing.

In my own project, every result that looked clean turned out to be circular, and three were caught by
assertions rather than by insight. So the concrete step is to make those assertions a component of the
system instead of a habit of the person operating it.

*(~340 words. If cut is needed, drop the third "how I would begin" item, not the worked example.)*

---

## Q4. "On the Tizz/Rizz Founder Matrix (TRFM), where do you land?"

> **Reference checked.** Origin is Arielle Zuckerberg / Long Journey Ventures, "rizz and tizz", their
> [framework for magical weirdness](https://flamingo-star-y3dj.squarespace.com/news/founderrizzandtizz);
> rizz is charisma and storytelling, tizz is obsessive depth. A
> [viral matrix](https://www.the-founders-corner.com/p/openais-devday-ai-native-gtm-playbook) plots quiet
> builders against charismatic fundraisers. *Content rephrased for compliance with licensing restrictions.*
>
> **Register:** culture question, so short and light. Do not write an essay here. Every claim below is
> evidenced in the CV or in this project, which is the only reason the joke earns the right to be made.

### ✅ Use this — the field wants a position, not an essay

```
Quiet builder end. Low rizz, high tizz, and the tizz is epistemic: I obsess over whether a result is
actually true rather than over the stack.
```

Minimal fallback: `Low rizz, high tizz.`

**⚠️ Corrected 2026-07-29 after Alessandro's own pushback, and the correction is on me.** My first draft
claimed high rizz on the evidence of the 180DC presidency and the Amazon stakeholder role. Those are
*roles*, and rizz in the Long Journey sense is a *trait*: magnetism, the thing that makes someone fall in
love with your vision. Inferring the trait from the job title is the same pattern-matching error I was
corrected on when reading a lab member's background. His self-assessment stands: he can hold a room when
the substance is his own, which is credibility rather than charisma.

**Strategically this helps rather than hurts.** Rizz is the axis that matters for the AI Founder track.
The AI Research track needs someone who can produce a first-author paper. Declaring low rizz is therefore
consistent with the outreach email's "the direction I want is research, not product", and it steers the
reader toward the right track instead of against it.

### Long version, kept in case the field turns out to be free text

A self-reported spot on a founder matrix is the kind of unfalsifiable claim I usually try to break, so
treat it as a prior.

High rizz: consultant to president of my 180DC chapter, and at Amazon I get Sales, Tech, Legal and Ops
across five countries to agree on one roadmap.

Odd tizz: not obsession with a stack, obsession with whether a result is true. I refused to accept a 100%
score on my own benchmark until I found the tautology producing it, and I killed my own flagship claim
this year.

Not a deep systems engineer, and better said now than found out in week two.

If there is a corner for people who can sell a result and cannot stop interrogating it, that is me.

*(~130 words.)*
