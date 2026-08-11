# Outreach — Rapidata (Zurich)

**Drafted 2026-07-30.** Route: `join@rapidata.ai`, or the Needle form linked from
[Motivated Talent](https://rapidata.ai/join/motivated-talent). Attach the academic CV.

## Why this one and not the others

Rapidata, founded 2023, Zurich, backed by BlueYard Capital and Founderful. Human feedback at scale for
RLHF and DPO, over 20 million annotators across 192 countries. Products include Model Rank Insights
with public image and video model benchmarks, plus a Model Evaluation line. *Content rephrased for
compliance with licensing restrictions.*

**Eight roles open. Seven are irrelevant, and the eighth is a deliberate no.**

⛔ **Do not apply to Reward Model Research Engineer.** It requires hands-on reward model building for
LLMs or diffusion models, RL fundamentals, RLHF/DPO pipelines, inference-time guidance, PyTorch and
production ML. None of that is in the CV, and applying there burns the contact.

✅ **Apply to Motivated Talent**, which explicitly accepts people with no matching posting and states
that someone has already joined that way. Full-time, salaried, equity, Zurich. No student-status
problem, unlike the Agentic Systems Lab form.

**The hook is two lines inside the reward-model posting**, which is why reading it was worth it:
- "design data collection and **active learning** strategies that reduce reward model training
  bottlenecks" = information acquisition under a budget, which is P1 and P5
- "whether **noisy, large-scale human preference data becomes a reliable reward signal**", plus
  robustness to annotator noise and benchmarking reliability before deployment = label validity and
  circular evaluation, which is EXP-011

---

## The note

**Subject:** Motivated Talent: which labels are worth collecting, and benchmarks that measure themselves

Hi,

Two things I built that sit next to problems in your job posts.

Which labels are worth collecting. I preregistered a policy that decides case by case whether acquiring
more information beats its cost. It lost all 15 declared cost-by-objective cells. An oracle acquiring
where the realised gain exceeds cost beats the best baseline by 0.065 to 0.087, so a winning policy
exists, but the correlation between predicted and realised per-case gain is +0.015, -0.070 and +0.000.
The reason is structural: per-case gain is the base model's residual, so predicting it means beating the
base model at its own task. Consequence: label acquisition should be budgeted at population level, not
selected per item. Your active learning bottleneck is that decision.

Benchmarks that measure themselves. This week I ran Splink and classical record linkage against my own
matcher on 13,773 company-name pairs with regulator-assigned ground truth. Splink got 77.3% balanced
accuracy to my 80.7%. The more useful finding was my own error: I had defined the "hard" stratum using
the same similarity score I was evaluating, so every method scored 0% there by construction. It
reproduces on an unrelated person-record benchmark, which confirms it is definitional, not empirical.
Same failure mode as an LLM judge scoring against a document the retriever chose.

What I do not have: reward modelling, RL, PyTorch. My ML is tabular. My strength is evaluation design
and point-in-time data that cannot see the future.

PM at Amazon Business until September 2026, then based in Zurich. CV attached.

Alessandro Guidi

---

## Rules

- **No em dashes.** Checked.
- Opens with results, not biography, because they ask for what you built and say to skip the generic
  cover letter.
- The gap paragraph stays. Declaring it yourself moves the interview to where you are strong instead of
  losing it at the first PyTorch question.
- Every number is verified: EXP-005 `results.json` for the oracle range and correlations, EXP-011
  `results.json` for 77.3 vs 80.7 and the 13,773 pairs.
- Optional upgrade if there is time: their MRI image and video benchmarks are public. One specific,
  correct observation about that methodology would be stronger than any of the above. Not attempted here
  because it needs reading the benchmark first, and a wrong critique costs more than it gains.

---

## Application form: the four short answers

**Why Rapidata**

Your product is a ranking of models built from noisy human preference. Whether that ranking measures
what it claims is not a QA detail, it is the whole asset. That is the problem I work on, and I have run
it against my own work rather than only against other people's.

**Why a startup**

I want the loop short: question, result, consequence, same week. At Amazon a decision passes five
markets and four functions before it lands, and I have taken what I can from that. I also want nobody
standing between me and the data.

**Why me**

I break my own results before anyone else does. I have caught three circular findings in my own
projects, including one where the label turned out to be the lookup key, and I ran a preregistered
experiment that killed my own headline claim and then published the diagnosis. Separately, I can talk to
your partner labs and to the model, which rarely sits in one person: PM at Amazon Business, two years
consulting for Tier-1 banks.

**What I want next, and what would make me leave inside a year**

I want to own the evaluation and data-acquisition decisions end to end, with the result visible in a
live system rather than in a slide.

I have doctoral applications open at ETH and none has been answered. If one came through with a
supervisor working on this same problem, I would take it, and you would hear it from me the week it
happened rather than in a resignation letter. What would keep me is that here the research question has
a production system attached, which most doctorates do not.

### Why the last answer discloses the PhD instead of dodging

The question exists to test whether you are honest when honesty costs something. The ETH applications
are real and checkable, and if they surface later the damage is worse than disclosing now. The clause
that makes it acceptable is the notice period: the risk they care about is not that you have ambitions,
it is that you vanish three weeks after signing. Ending on the argument for staying is what turns a
liability into a reason to hire.

**Consistency check:** this must not contradict the Agentic Systems Lab email, which says the direction
wanted is research rather than product, or the D-INFK file. It does not. All three say the same thing:
research is the goal, and the paid route is whichever one has the research problem attached.

**The three circularities cited are all SEC-based** (846 overlapping CIKs in EXP-002, 1770/1770 in
EXP-006, the stratification in EXP-011). The fourth, in the agentic PR work, stays uncited per the
standing rule.
