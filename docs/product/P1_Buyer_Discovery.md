# P1 Buyer Discovery — narrow wedge

**Hypothesis, not fact:** a VC Partner needs help choosing the next diligence item under limited time.

## Frozen discovery scope
- Named buyer: Partner at a seed-focused VC fund.
- Geography: Switzerland plus DACH.
- Decision event: continue or stop diligence before an IC/term-sheet decision.
- Workflow: rank missing information by expected decision value net of cost and delay.
- Current stage: **B0**, because no qualifying buyer behavior is documented.

## Interview script
1. Walk me through the last deal where diligence time was constrained.
2. At what moment did you decide what to investigate next?
3. Which alternatives did you consider, and who made the choice?
4. What was already known versus missing at that moment?
5. How many people, hours, external vendors and elapsed days were involved?
6. Which missing item changed, or could have changed, the decision?
7. What did delay or a wrong call cost? Ask for a range, not a false point estimate.
8. Which tools or heuristics are used now, and where do they fail?
9. Rank this workflow among the three highest-cost diligence problems.
10. Would you provide a de-identified historical case or own a scoped pilot? Record behavior only.

## Quantitative utility and cost elicitation

Use one recent de-identified decision, not abstract preferences. Record ranges before showing model
results:

1. Of 100 comparable screened companies, how many would normally continue to deeper diligence?
2. What is the loaded internal cost of one unnecessary continuation: low/base/high?
3. What is the opportunity cost of stopping a company that later proves follow-on-ready: low/base/high?
4. What operational value should one correctly continued case receive relative to those costs?
5. For each information request, record analyst hours, external spend and elapsed days.
6. What does one day of delay cost in this workflow? When is delay immaterial versus deal-losing?
7. At what maximum cost would you buy the information? At what cost would you definitely stop?
8. Ask the interviewee to choose among three explicit policies: false-positive averse, balanced or
   opportunity averse, and explain why.

Normalize each interview so `TP = 1`; calculate `FP`, `FN`, direct cost and delay cost in the same
units. Preserve low/base/high separately. Do not average incompatible buyer segments. A utility/cost
scenario is eligible for the confirmatory acquisition experiment only if at least three qualified
buyers support it or if it is retained as a clearly labelled assumption-bound sensitivity case.

Use `P1_UTILITY_COST_ELICITATION.csv` for the structured record. Do not place fund names, deal names
or confidential case details in the repository.

## Qualification and gate
A qualified interviewee owns or materially influences live seed investment diligence. Log role, fund,
date, workflow volume, current alternative, hours, direct spend, rank, data willingness and next step.
After at least 10 interviews: fewer than 5 ranking the workflow top-three means **pivot**. Statements
of interest do not exceed B3; money or documented procurement effort is required for B4+.

Utility freeze gate: at least three qualified interviews with internally coherent low/base/high ranges;
otherwise keep the acquisition experiment exploratory and report the complete declared scenario grid.

## Do not pitch
Do not lead with an operating system, agents, foundation models or the full research programme.
Present the workflow and ask about the last real decision before describing a solution.
