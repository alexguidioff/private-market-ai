# Requirements Document

## Introduction

This document specifies a candid strategic assessment of Private Market AI as a research agenda, PhD candidacy platform, market opportunity, potential post-PhD spin-off, and source of personal earnings. The assessment uses only the original request and repository evidence. The assessment must separate evidence from inference, quantify uncertainty without guaranteeing outcomes, and define measurable rules that can invalidate the preferred paths.

## Glossary

- **Viability_Assessment**: The strategic assessment produced for the Private Market AI initiative.
- **Assessment_Date**: The calendar date on which the Viability_Assessment is issued; all deadlines and valuation dates are measured from this date unless a criterion states another date.
- **Candidate**: Alessandro Guidi, the person evaluating research, PhD, employment, and founder paths.
- **Original_Request**: The Italian-language request asking about Private Market AI, PhD admission, market existence, post-PhD spin-off viability, and earnings.
- **Repository_Evidence**: Information contained in the Private-Market-AI workspace at assessment time.
- **Evidence_Register**: A table containing one row per Material_Claim and the fields claim identifier, claim text, single evidence classification, source locator, verification status, Confidence_Level, strongest supporting item, strongest contradicting item, and decision affected.
- **Documented_Fact**: A claim directly supported by the Original_Request or Repository_Evidence.
- **Assumption**: A parameter or premise required for analysis but not established by Repository_Evidence.
- **Judgment**: An analytical conclusion derived from Documented_Facts and stated Assumptions.
- **Unverified_Claim**: A time-sensitive or external claim without current official verification in Repository_Evidence.
- **Evidence_Classification**: Exactly one of Documented_Fact, Assumption, Judgment, or Unverified_Claim assigned to a Material_Claim.
- **Material_Claim**: A claim capable of changing a recommendation, probability interval, scenario value, or Decision_Rule output.
- **Confidence_Level**: High, Medium, or Low confidence assigned from evidence quality, evidence consistency, and assumption sensitivity.
- **Research_Score**: An integer score with fixed meanings: 1 = unsupported or blocked, 2 = weak with a major unresolved dependency, 3 = mixed with a feasible resolution path, 4 = strong with a minor unresolved dependency, and 5 = verified by direct evidence with no identified material dependency.
- **Evidence_Maturity**: Exactly one study stage: M0 Concept, M1 Specified Design, M2 Data and Access Confirmed, M3 Analysis or Working Paper, or M4 Accepted, Published, or Independently Replicated.
- **Value_of_Information**: The expected benefit of acquiring additional information before an investment decision, net of information-acquisition cost.
- **P1**: The proposed flagship study testing whether Value_of_Information methods improve investment-decision outcomes against non-Value_of_Information baselines.
- **Simulator**: The proposed synthetic private-market decision environment used to generate evaluation cases and ground truth.
- **Net_Decision_Value**: The buyer-approved value of a decision outcome minus information-acquisition and decision costs under a preregistered calculation.
- **Probability_Interval**: Exactly one fixed numerical interval: Very Low [0%,10%), Low [10%,25%), Plausible [25%,50%), More Likely Than Not [50%,70%), or High [70%,100%].
- **Admissions_Tier_A**: Aspirational, highly selective methods-led CS or ML groups, including the repository's elite ETH-style targets.
- **Admissions_Tier_B**: Strong-fit Swiss interdisciplinary CS, information-systems, finance, or entrepreneurship groups identified in Repository_Evidence.
- **Admissions_Tier_C**: Broader applied Swiss groups and programs with relevant AI, data, finance, or innovation work.
- **Direct_PhD_Route**: Application directly to a funded doctoral position or doctoral program.
- **Bridge_Route**: Entry through a Research Assistant, Scientific Collaborator, or Research Engineer role before a later PhD decision or application.
- **Admissions_Combination**: One pairing of Admissions_Tier_A, Admissions_Tier_B, or Admissions_Tier_C with the Direct_PhD_Route or Bridge_Route, producing exactly six pairings.
- **Admission_Readiness**: Evidence that the Candidate can secure and complete research work, measured through publications, methods depth, references, supervisor fit, proposal quality, and funded-seat availability.
- **Proposed_Wedge**: A test hypothesis focused on value-of-information support for live venture-capital or growth-investment diligence.
- **Named_Buyer**: The budget owner identified as a Partner, Head of Investments, or Head of Due Diligence at a Swiss or European VC or growth fund.
- **Painful_Workflow**: Prioritizing which missing information to acquire before an investment decision under a limited diligence budget.
- **Buyer_Evidence_Stage**: Exactly one demand stage: B0 No Buyer Evidence, B1 Qualified Interview, B2 Written Design-Partner Commitment, B3 Completed Unpaid Pilot, B4 Paid Pilot, B5 Renewal or Annual Contract, or B6 Expansion.
- **Qualified_Buyer**: A Named_Buyer or a direct participant in the Named_Buyer's diligence workflow who has completed a documented interview or offer review.
- **Willingness_To_Pay_Evidence**: Buyer behavior at Buyer_Evidence_Stage B4, B5, or B6.
- **Competition_Set**: Existing private-market databases, internal fund tooling, consultants, general AI tools, and AI due-diligence vendors that can solve part of the Painful_Workflow.
- **Data_Barrier**: A licensing, redistribution, coverage, point-in-time reconstruction, identity-resolution, access, or terms-of-service constraint.
- **Regulatory_Barrier**: A privacy, confidentiality, financial-services, model-governance, explainability, or liability constraint affecting deployment.
- **Validation_Gate**: One of eight measurable gates: problem validation, solution validation, payment validation, retention validation, data rights, regulatory feasibility, technical performance, or founder commitment.
- **Spin_Off**: A company commercializing research assets developed through the Candidate's academic work.
- **Annual_Recurring_Revenue**: Contracted recurring company revenue normalized to twelve months, abbreviated ARR.
- **Cash_Earnings**: Personal cash received by the Candidate as gross salary, bonus, Founder_Compensation, or distributions, excluding company revenue and Equity_Value.
- **Company_Metrics**: Company revenue, company costs, company cash flow, customer count, and ARR, none of which is personal income.
- **Founder_Compensation**: Cash salary, bonus, and distributions paid to the Candidate by a Spin_Off.
- **Equity_Value**: The Candidate's non-cash, illiquid ownership value after Dilution and scenario adjustments.
- **Dilution**: Reduction of the Candidate's fully diluted ownership percentage after financing, options, or other issuances.
- **Tax_Estimate**: An explicitly assumed tax impact shown separately from gross Cash_Earnings.
- **Risk_Adjusted_Value**: Probability-weighted value after Dilution, taxes, time horizon, and liquidity assumptions.
- **Scenario_Set**: Conservative, Base, and Upside scenarios that are mutually exclusive, collectively exhaustive, and assigned probabilities totaling 100% for one path and horizon.
- **Opportunity_Cost**: Comparable-employment cumulative after-tax discounted Cash_Earnings minus the evaluated path's cumulative after-tax discounted Cash_Earnings over the same horizon; Equity_Value is reported separately.
- **Falsification_Criterion**: An observable result that rejects or materially weakens a thesis, market hypothesis, route recommendation, or earnings scenario.
- **Decision_Rule**: A complete mapping from a metric, comparison operator, threshold, observation window, and evidence source to exactly one Decision_Output.
- **Decision_Output**: Exactly one resulting action: continue, bridge, pivot, pause, or stop.
- **Core_Thesis**: Exactly one of research viability, admissions viability, market viability, Spin_Off viability, or earnings viability.
- **Action_Record**: A recommended action with a unique rank, owner, start date, due date, evidence deliverable, and decision updated.

## Requirements

### Requirement 1: Evidence discipline and candor

**User Story:** As the Candidate, I want a candid evidence-based assessment, so that optimism from the project narrative does not substitute for validation.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL limit Documented_Facts to the Original_Request and Repository_Evidence.
2. WHEN the Viability_Assessment presents a Material_Claim, THE Viability_Assessment SHALL assign exactly one Evidence_Classification to the Material_Claim.
3. WHEN the Viability_Assessment presents a Material_Claim, THE Viability_Assessment SHALL include one Evidence_Register row containing every Evidence_Register field.
4. WHEN the Viability_Assessment classifies a Material_Claim as a Documented_Fact, THE Viability_Assessment SHALL cite a repository file path plus section, heading, page, or line locator and record the verification status.
5. WHEN the Viability_Assessment classifies a Material_Claim as a Judgment, THE Viability_Assessment SHALL identify the supporting Documented_Facts and Assumptions by Evidence_Register claim identifier.
6. IF Repository_Evidence contains conflicting claims, THEN THE Viability_Assessment SHALL record both claims, assign a Confidence_Level to the resulting Judgment, and state whether the conflict changes a Decision_Output.
7. IF a current external value lacks official verification in Repository_Evidence, THEN THE Viability_Assessment SHALL classify the value as an Unverified_Claim and exclude the value from deterministic Decision_Rules.
8. THE Viability_Assessment SHALL express admissions, market, Spin_Off, and earnings outcomes as conditional ranges rather than guarantees.
9. THE Viability_Assessment SHALL record the strongest supporting item, strongest contradicting item, missing evidence, and negative evidence separately for each Core_Thesis.

### Requirement 2: Private Market AI thesis assessment

**User Story:** As the Candidate, I want the research thesis tested against its evidence and dependencies, so that I can distinguish an intellectually coherent agenda from a viable execution plan.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL evaluate novelty, methodological contribution, execution feasibility, data feasibility, partner dependence, publication potential, commercial transferability, and opportunity cost as eight separate research dimensions.
2. WHEN the Viability_Assessment scores a research dimension, THE Viability_Assessment SHALL assign one integer Research_Score from 1 through 5 using the fixed Research_Score meanings.
3. WHEN the Viability_Assessment scores a research dimension, THE Viability_Assessment SHALL cite at least one supporting Documented_Fact and one limiting Documented_Fact, contradicting item, or missing-evidence item.
4. THE Viability_Assessment SHALL assign one Evidence_Maturity category to the established valuation study, proposed Value of Information flagship, Decision Quality study, Human-AI committee study, and each continuation study.
5. WHEN the Viability_Assessment assigns Evidence_Maturity, THE Viability_Assessment SHALL cite the criterion satisfied by Repository_Evidence and identify the next category's unmet criterion.
6. WHEN the Viability_Assessment evaluates the proposed Simulator, THE Viability_Assessment SHALL treat construct validity as a systemic dependency for every study using simulator ground truth.
7. IF a proposed research contribution depends on private decision logs or investor subjects, THEN THE Viability_Assessment SHALL identify the access dependency, evidence of access, decision deadline, and repository-supported fallback.
8. THE Viability_Assessment SHALL identify at least three measurable conditions under which the Private Market AI thesis ranks below an alternative research agenda.
9. THE Viability_Assessment SHALL issue exactly one current research-viability verdict of strong, conditional, weak, or unsupported and state the Research_Score or evidence changes required to select each adjacent verdict.

### Requirement 3: Tiered PhD admissions assessment

**User Story:** As the Candidate, I want admission prospects segmented by target tier and route, so that I can allocate effort to paths with different selectivity and fit.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL assess all six Admissions_Combinations as separate rows.
2. WHEN the Viability_Assessment estimates an Admissions_Combination, THE Viability_Assessment SHALL assign exactly one Probability_Interval from the five fixed Probability_Intervals and SHALL state a Confidence_Level.
3. WHEN the Viability_Assessment estimates an Admissions_Combination, THE Viability_Assessment SHALL list supporting factors, blocking factors, and the next evidence capable of moving the estimate to an adjacent Probability_Interval.
4. THE Viability_Assessment SHALL evaluate publication evidence, academic references, quantitative and CS preparation, methods depth, supervisor fit, proposal maturity, funded-seat availability, and competition as separate Admission_Readiness factors for each Admissions_Combination.
5. WHEN Repository_Evidence reports an accepted publication, THE Viability_Assessment SHALL classify the publication by venue, review status, track, authorship position, and acceptance status rather than equating a student-track acceptance with a top-venue research record.
6. IF an Admissions_Combination has weak methodological fit, no verified funded seat, and no substantive supervisor engagement, THEN THE Viability_Assessment SHALL assign the Direct_PhD_Route a Low or Very Low Probability_Interval.
7. WHEN the Viability_Assessment evaluates a Bridge_Route, THE Viability_Assessment SHALL state separate conditional Probability_Intervals for later Direct_PhD admission after zero, one, or at least two verified outcomes among paid research work, publication submission, and supervisor sponsorship.
8. THE Viability_Assessment SHALL compare the Bridge_Route against immediate Direct_PhD applications using expected research signal, elapsed months, gross Cash_Earnings, and option value.
9. THE Viability_Assessment SHALL provide one deterministic Decision_Rule for apply now, pursue bridge first, broaden targets, and stop the admissions campaign.
10. IF the Candidate receives no substantive supervisor interest after at least 20 tailored contacts across at least two Admissions_Tiers within 12 weeks, THEN THE Viability_Assessment SHALL output pivot for the research pitch, target set, or route and SHALL identify which input evidence selects the pivot.

### Requirement 4: Narrow-wedge market assessment

**User Story:** As the Candidate, I want the market thesis tested through one buyer and one painful workflow, so that a broad private-market platform narrative does not masquerade as product demand.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL evaluate the Proposed_Wedge before evaluating broader Due Diligence Copilot, Investment Copilot, or Private Market Operating System concepts.
2. THE Viability_Assessment SHALL define one Named_Buyer, one Painful_Workflow, one investment stage, one geographic market, and one decision event for the Proposed_Wedge.
3. THE Viability_Assessment SHALL define the Named_Buyer's current alternative as a measurable baseline including tools, analyst roles, elapsed time, labor hours, and direct expenditure.
4. THE Viability_Assessment SHALL quantify annual workflow volume, analyst hours per decision, loaded labor cost, delay cost or error cost, addressable buyer count, annual contract value, and resulting bottom-up annual spend using Evidence_Classifications.
5. THE Viability_Assessment SHALL calculate a low and high bottom-up reachable-market estimate as addressable buyer count multiplied by annual contract value and SHALL expose both input values in the Evidence_Register.
6. THE Viability_Assessment SHALL classify repository statements about market opportunity or willingness to pay as Assumptions unless Repository_Evidence contains corresponding buyer behavior.
7. WHEN the Viability_Assessment evaluates buyer evidence, THE Viability_Assessment SHALL assign exactly one Buyer_Evidence_Stage from B0 through B6 and cite the observed behavior supporting the stage.
8. THE Viability_Assessment SHALL treat B1 through B3 as problem or solution evidence and B4 through B6 as Willingness_To_Pay_Evidence.
9. THE Viability_Assessment SHALL identify the Competition_Set by category and compare the Proposed_Wedge on data, workflow, model performance, integration, trust, and price.
10. THE Viability_Assessment SHALL identify at least one Data_Barrier for every required proprietary, public, academic, or restricted data category documented in Repository_Evidence.
11. THE Viability_Assessment SHALL identify applicable Regulatory_Barriers for fund, family-office, private-bank, and wealth-manager deployment and SHALL classify resulting statements as analytical issues rather than legal conclusions.
12. THE Viability_Assessment SHALL issue separate verdicts for problem existence, budget ownership, Buyer_Evidence_Stage, reachable market, differentiation, and deployability.
13. IF fewer than 5 Qualified_Buyers confirm the Painful_Workflow among the buyer's three highest-cost diligence problems after at least 10 completed Qualified_Buyer interviews, THEN THE Viability_Assessment SHALL output pivot or stop for the Proposed_Wedge.
14. IF no Qualified_Buyer commits money or documented procurement effort after three scoped pilot offers, THEN THE Viability_Assessment SHALL assign no stage above B3.

### Requirement 5: Post-PhD spin-off validation gates

**User Story:** As the Candidate, I want the Spin_Off decision gated by observable validation, so that a PhD completion event does not automatically justify company formation.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL treat research completion, publication, and technical novelty as insufficient for full-time Spin_Off formation without passage of all eight Validation_Gates.
2. WHEN the Viability_Assessment defines a Validation_Gate, THE Viability_Assessment SHALL state the metric, comparison operator, threshold, deadline, evidence source, current status, and exactly one failure consequence.
3. THE Viability_Assessment SHALL set the problem-validation gate to at least 15 completed Qualified_Buyer interviews with at least 10 buyers ranking the Painful_Workflow among the three highest-cost diligence problems before the post-PhD decision date.
4. THE Viability_Assessment SHALL set the solution-validation gate to at least 5 written design-partner commitments containing a named workflow, data contribution, pilot owner, and target metric before the post-PhD decision date.
5. THE Viability_Assessment SHALL set the payment-validation gate to at least 3 paid pilots and at least CHF 50,000 of contracted ARR before full-time Spin_Off formation.
6. THE Viability_Assessment SHALL set the retention-validation gate to at least 2 paid pilot renewals or annual contracts completed within 12 months after the first paid pilot starts.
7. THE Viability_Assessment SHALL set the data-rights gate to documented collection, processing, model-use, and commercial-use rights for every production data source before the corresponding source enters a paid deployment.
8. THE Viability_Assessment SHALL set the regulatory-feasibility gate to a dated deployment assessment covering privacy, confidentiality, financial regulation, explainability, model governance, and liability, with an assigned owner and mitigation deadline for every identified blocker before a paid deployment.
9. THE Viability_Assessment SHALL set the technical-performance gate to at least a 25% improvement on one buyer-approved workflow metric against the documented current-alternative baseline in at least 2 completed pilots before full-time Spin_Off formation.
10. THE Viability_Assessment SHALL set the founder-commitment gate to a signed 12-month personal runway plan and a Candidate commitment of at least 40 hours per week beginning within 30 days after the formation decision.
11. IF payment validation, retention validation, data rights, regulatory feasibility, technical performance, or founder commitment is failed at the applicable deadline, THEN THE Viability_Assessment SHALL output pivot, pause, or stop rather than continue to full-time Spin_Off formation.
12. WHERE a university owns or restricts relevant intellectual property, THE Viability_Assessment SHALL require written licensing terms, founder ownership terms, and commercialization permission before passing the data-rights gate.
13. WHEN a Validation_Gate is evaluated, THE Viability_Assessment SHALL map pass and fail outcomes to exactly one Decision_Output.

### Requirement 6: Earnings and wealth scenarios

**User Story:** As the Candidate, I want earnings modeled by path and scenario, so that salary, business revenue, founder income, and speculative equity are not conflated.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL model the Direct_PhD_Route, Bridge_Route followed by PhD, research or industry employment without PhD, and PhD followed by Spin_Off as four separate paths.
2. THE Viability_Assessment SHALL provide one Scenario_Set for each path at annual, five-year, and ten-year horizons.
3. WHEN the Viability_Assessment assigns scenario probabilities within a Scenario_Set, THE Viability_Assessment SHALL define non-overlapping outcome conditions and probabilities totaling exactly 100%.
4. WHEN the Viability_Assessment presents an earnings scenario, THE Viability_Assessment SHALL report Cash_Earnings, Company_Metrics, and Equity_Value in three separate sections.
5. WHEN the Viability_Assessment reports Cash_Earnings, THE Viability_Assessment SHALL separate gross salary, bonus, Founder_Compensation, distributions, Tax_Estimate, and net cash.
6. WHEN the Viability_Assessment reports Company_Metrics, THE Viability_Assessment SHALL separate company revenue, company costs, company cash flow, customer count, and ARR and SHALL label Company_Metrics as non-personal income.
7. WHEN the Viability_Assessment reports Equity_Value, THE Viability_Assessment SHALL show pre-financing ownership, Dilution by financing stage, valuation or exit assumption, time to liquidity, failure probability, and Risk_Adjusted_Value and SHALL label Equity_Value as illiquid before the modeled liquidity event.
8. WHEN the Viability_Assessment models taxes, THE Viability_Assessment SHALL identify jurisdiction and effective-rate Assumptions and SHALL label the Tax_Estimate as an analytical estimate rather than tax advice.
9. THE Viability_Assessment SHALL calculate the probability-weighted value of each Scenario_Set and SHALL distinguish the probability-weighted value from the Base scenario.
10. THE Viability_Assessment SHALL perform sensitivity analysis for salary growth, PhD duration, time to revenue, pricing, customer count, gross margin, funding raised, Dilution, failure probability, and exit value using documented or explicitly justified lower and upper bounds.
11. IF an earnings input requires official external verification, THEN THE Viability_Assessment SHALL classify the input as an Unverified_Claim and show the output at both sensitivity bounds.
12. THE Viability_Assessment SHALL calculate Opportunity_Cost for each non-employment path against the same comparable-employment path, horizon, currency, tax treatment, inflation basis, and discount rate.
13. THE Viability_Assessment SHALL report nominal values, currency, valuation date, inflation treatment, and discount rate for every earnings table.

### Requirement 7: Decision rules and falsification

**User Story:** As the Candidate, I want explicit decision rules and disconfirming tests, so that new evidence can change the strategy.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL define Decision_Rules producing continue, bridge, pivot, pause, or stop for each Core_Thesis.
2. WHEN the Viability_Assessment defines a Decision_Rule, THE Viability_Assessment SHALL specify one metric, one comparison operator, one threshold, one observation window, one evidence source, and exactly one Decision_Output for every possible measured result.
3. WHEN more than one Decision_Rule applies to the same decision date, THE Viability_Assessment SHALL select exactly one Decision_Output using the precedence stop, pause, pivot, bridge, then continue.
4. THE Viability_Assessment SHALL define at least two Falsification_Criteria for each Core_Thesis.
5. WHEN the Viability_Assessment defines a Falsification_Criterion, THE Viability_Assessment SHALL specify the tested claim, metric, threshold, deadline, evidence source, and Decision_Output.
6. IF P1 fails to outperform non-Value-of-Information baselines on net decision value across the preregistered evaluation settings, THEN THE Viability_Assessment SHALL output pivot for P1 as the flagship methodological contribution.
7. IF the Simulator fails preregistered external-validity or multi-world recovery thresholds during the first research year, THEN THE Viability_Assessment SHALL output pause for simulator-dependent claims pending independent empirical validation.
8. IF no target supervisor offers a documented meeting, requested application, funded-role discussion, or collaboration step after 20 tailored contacts across at least two Admissions_Tiers within 12 weeks, THEN THE Viability_Assessment SHALL output pivot for the current target-and-pitch combination.
9. IF paid-pilot conversion is below one-third after at least 6 qualified pilot proposals, THEN THE Viability_Assessment SHALL output pivot for the current buyer-workflow-price combination.
10. IF fewer than 2 paid customers renew after receiving the contractually agreed workflow outcome, THEN THE Viability_Assessment SHALL output stop for claims of repeatable product value for the Proposed_Wedge.
11. IF the risk-adjusted ten-year Spin_Off outcome is below the comparable-employment outcome under Base assumptions and no documented non-financial preference is assigned a compensating value, THEN THE Viability_Assessment SHALL output stop for full-time Spin_Off formation.
12. WHEN the Viability_Assessment assigns a Probability_Interval, THE Viability_Assessment SHALL state the dated observation that moves the estimate to each adjacent interval.

### Requirement 8: Recommendation and action sequence

**User Story:** As the Candidate, I want an actionable recommendation with checkpoints, so that the assessment changes near-term behavior rather than ending with a narrative verdict.

#### Acceptance Criteria

1. THE Viability_Assessment SHALL provide a current recommendation for the next 90 days, next 12 months, PhD period, and post-PhD decision point.
2. THE Viability_Assessment SHALL rank the Direct_PhD_Route, Bridge_Route, continued industry employment, and immediate startup path from 1 through 4 with no tied ranks.
3. WHEN the Viability_Assessment ranks a path, THE Viability_Assessment SHALL score expected value, downside, reversibility, evidence generation, and strategic option value on a stated common scale and show the ranking calculation.
4. THE Viability_Assessment SHALL define at least three Action_Records and assign each Action_Record a unique rank.
5. WHEN the Viability_Assessment defines an Action_Record, THE Viability_Assessment SHALL provide an owner, calendar start date, calendar due date, evidence deliverable, and Decision_Rule updated.
6. THE Viability_Assessment SHALL distinguish Action_Records supported by Repository_Evidence from Action_Records dependent on Assumptions.
7. THE Viability_Assessment SHALL include a one-page decision table with exactly five rows, one for each Core_Thesis.
8. WHEN the Viability_Assessment adds a decision-table row, THE Viability_Assessment SHALL include current verdict, Confidence_Level, next test, pass threshold, failure action, and calendar review date.
9. IF evidence remains insufficient for a yes-or-no conclusion, THEN THE Viability_Assessment SHALL return a conditional verdict and identify the minimum evidence and deadline required for resolution.
10. THE Viability_Assessment SHALL conclude with a candid answer to each question in the Original_Request without converting uncertainty into reassurance.
