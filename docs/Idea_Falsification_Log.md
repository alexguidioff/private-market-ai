# Idea Falsification Log

**Started:** 2026-07-28 · **Mode:** autonomous search + falsification until stopped
**Rule:** every candidate must pass the *non-prediction filter* — it must be useful even if its
predictive accuracy is zero. Verdicts are recorded whether they are positive or negative.

## Why this log exists

Four ideas died in the preceding work (agentic PR risk gate, model authority graph, controllable
agent practices, harness comparison). Each died at contact with data, which is the desired outcome,
but none was recorded in a way that stops the same idea being re-proposed in a different vocabulary.
This file is the record. An idea that appears here with a verdict does not get re-litigated without
new evidence.

## Standing constraints

| Constraint | Source |
|---|---|
| No prediction as the core value proposition | four consecutive predictive failures, AUC ceiling ~0.61 |
| No validation by investor interviews | owner's explicit preference; behavioural evidence only |
| Must be buildable by one technical founder | no commercial cofounder at present |
| Model-agnostic, B2B, recurring, sticky | owner's stated target |
| Must not overclaim the research | WI2026 = valuations not returns; P1 = 0/15 gates; EXP-002 largely mechanical |

## Assets actually available

| Asset | Status | Predictive? |
|---|---|---|
| Point-in-time reconstruction pipeline (SEC, dated evidence) | built, working | no — retrieval |
| Source gates / provenance discipline | built | no — verification |
| Decision record | built | no — record keeping |
| Tail-lift estimator (`code/tail_lift.py`) | validated on synthetic + real | measurement tool |
| Relation screen (`bench/rank/discriminates.py`) | calibrated | measurement tool |
| 1,000 labelled agentic PRs (GitHub Copilot only) | collected | dataset |
| OpenRouter app→model graph, 87 apps × 31 days | collected | dataset |

---

## Verdict table

| # | Hypothesis | Verdict | Killed by |
|---|---|---|---|
| H0a | Agentic PR risk is predictable pre-review | **dead** | AUC 0.538–0.587, flat calibration |
| H0b | Model authority is derivable from app→model graph | **dead** | recursion ≈ token count; AUC 0.555 vs 0.557 baseline |
| H0c | Controllable practices separate PR outcomes | **dead** | 0/8 actionable, stratified gaps ≈ 0 |
| H0d | Harness choice measurably changes real-code outcomes | **unresolved, abandoned** | 0/51 repos shared two harnesses; confounder not removable |
| H1 | Point-in-time evidence layer ("was this knowable at date X") is an open product space | **dead — occupied** | see below |

---

## H1 — Point-in-time evidence retrieval as a product

**Why it was a candidate.** The PIT reconstruction pipeline is the owner's strongest non-predictive
asset, and "this claim was knowable on that date" is a verification question, not a forecast.

**Killed by prior art, found 2026-07-28.** BackSearch, launched by Ross Taylor (General Reasoning;
previously Meta AI, Llama), accepts an `as_of` date and returns web information as it stood at that
date, specifically to stop future-data leakage when backtesting agents and RL environments
([Digg summary](https://digg.com/ai/divhrbm1)). Commentary in the trade press goes further and argues
the point-in-time LLM is now public infrastructure, removing the excuse for look-ahead-contaminated
backtests ([The Specification](https://thespecification.substack.com/p/the-open-point-in-time-llm-and-what)).
Time-locked models trained only on content from a chosen era are also being built as a research
method ([CACM](https://cacm.acm.org/news/are-llms-unstuck-in-time/)).

Content rephrased for compliance with licensing restrictions.

**Consequence.** The generic version of the idea is taken by someone with more distribution and
more credibility. What is *not* covered is the regulated-document version, where the corpus is not
the open web. That is a narrower claim and is treated separately below, not as a rescue of H1.

---

## H2 — Deterministic attribution verification (under test)

**The observation that motivates it.** Adoption is near universal but the benefit is being eaten by
checking. In a 2026 CRE investing survey, 97% report AI is in their investment process, yet only 51%
say it saves time once output verification is counted, and 41% say AI-involved work takes *longer*
than doing it manually because every output must be checked
([Dealpath survey via BusinessWire](https://www.businesswire.com/news/home/20260708631611/en/)).
A separate estimate puts the annualised cost of verification activity at roughly $78,000 per senior
finance leader ([diginomica on Sage/IDC](https://diginomica.com/ais-verification-tax-real-sage-and-idc-warn-finance-leaders-are-having-adapt-meet-fresh-challenge)).

**The specific failure being verified.** Not fabricated sources — a well-built retrieval system
already links to real documents. The measured failure is *attribution hallucination*: the answer is
right while the cited region is wrong. An audit of 20 multimodal models found this pervasive, with
the strongest system reaching a source-attribution accuracy of 76.0 and the best open-source model
22.5 ([arXiv 2605.12882](https://arxiv.org/abs/2605.12882)). Deep-research agents keep link validity
above 94% while factual accuracy sits at 39–77%
([arXiv 2605.06635](https://arxiv.org/html/2605.06635v1)). In finance specifically, bibliographic
hallucination rates around 20% have been measured
([Springer](https://link.springer.com/article/10.1007/s41060-025-00731-0)).

Content rephrased for compliance with licensing restrictions.

**Hypothesis.** For *quantitative* claims about regulated filings, attribution can be verified
deterministically — the number either appears in the cited document, in the cited units, in a
consistent context, or it does not. No model judgement, no predictive accuracy, passes or fails.

**Falsification condition, declared before building.** The idea dies if either holds:
1. the share of claims that are deterministically checkable is small (< ~40%), leaving the hard
   cases exactly where they were, or
2. an off-the-shelf LLM verifier already matches deterministic checking, in which case there is no
   product, only a wrapper.

### H2 result — EXP-003, run 2026-07-28

Tool: `code/claim_verify.py` (17/17 constructed self-test cases correct after two bugs were fixed
during development, both recorded below). Experiment: `code/exp003_verifiability.py`, 3,537 claims
generated from 4,000 real Form D filings, half correct and half corrupted with a known error class.

| Measure | Precision-aware verifier | Naive string equality |
|---|---:|---:|
| Coverage (decidable at all) | **100.0%** | — |
| False alarms on correct claims | **0.00%** | **38.81%** |
| Scale error caught | 100.0% | 81.8% |
| Wrong field caught | 98.1% | 99.6% |
| Stale value caught | 98.2% | 100.0% |
| Transposed digits caught | 69.5% | 100.0% |

Both declared conditions pass: coverage far above the 40% floor, and the careful verifier removes a
38.8-point false-alarm rate that the naive one produces. **The false-alarm number is the finding.**
A verifier that cries wolf on two out of five correct claims is worse than no verifier, because the
reviewer stops trusting it and goes back to checking everything by hand — which is exactly the
verification tax being paid today.

**Two bugs found and fixed during development**, both of which would have inverted conclusions:

1. Thousands separators were replaced with spaces, so `$5,000,000` parsed as `5` and a correct claim
   was reported as contradicted.
2. `exactly` was not treated as a precision marker, so "exactly $5 million" accepted $5.4 million.
   Rounding tolerance must be *removed* by an exactness word, not widened.

**The transposed-digit gap is not a defect.** Probed directly: when a transposition lands in a digit
position that the stated rounding already discards, `$5.2 million` against an actual 5,234,000 is a
*correct* rendering, and flagging it would be the false alarm. The naive checker "catches" 100% of
these only because it flags nearly everything. Reporting 69.5% is the honest number; a verifier
tuned to reach 100% here would reintroduce the false alarms.

### Independent confirmation from the literature, found after the run

The false-alarm failure is not something only my naive baseline suffers from — it is measured in
frontier LLMs. FinVerBench reports that on clean financial statements, nine of fourteen complete LLM
runs produced 95–100% false positives under a guided-checklist prompt
([arXiv 2605.29586](https://arxiv.org/html/2605.29586v1)). On multi-document accounting
reconciliation, six contemporary LLMs reach at most 46% exact final-balance-sheet accuracy
([arXiv 2606.15949](https://arxiv.org/html/2606.15949)). Content rephrased for compliance with
licensing restrictions.

That is stronger than my own result: models do not merely fail to catch errors, they *invent* errors
on clean input at rates that make them unusable as gatekeepers. Deterministic arithmetic produced
0.00% on the same class of task.

### What this does and does not establish

Established: for quantitative claims resolvable against structured source fields, deterministic
verification is complete (100% coverage on this field set) and does not generate false alarms, where
both naive matching and, per the literature, frontier LLMs do.

**Not** established, and these are the load-bearing gaps:
* The corpus is Form D structured fields — clean, typed, few fields. Real memos cite PDFs, tables
  spanning pages, and figures needing arithmetic across line items. Coverage there is unknown and
  certainly below 100%.
* Claims were machine-generated. Human-written claims include qualitative and comparative assertions
  that no arithmetic can settle.
* This verifies attribution, not truth. A correctly cited wrong number passes.

### Competitive position

Deterministic citation verification already exists as a product category: CitateGenie advertises a
fully deterministic pipeline with no AI in the verification path, for scholarly, legal and
professional publications ([press release](https://www.einpresswire.com/article/929129446/evidite-announces-citategenie)),
and GPTZero, CoChat and CiteTrue operate in the academic segment. Those verify *whether a reference
exists*. None of them, as far as this search found, verifies *whether a quantitative claim matches
the value in the cited regulatory source* — a different check requiring scale, precision and
point-in-time handling.

### H2 second test — EXP-004, real annual reports. **FAILS the declared threshold.**

The EXP-003 result did not carry over. Tested on six recent 10-K filings (Apple, Microsoft, Amazon,
Alphabet, Nvidia, Meta), 150 claims sampled *from the documents themselves* so the figure is
guaranteed present and `not_found` can only mean the matcher failed:

| Measure | Scale-aware verifier | Digit-string baseline |
|---|---:|---:|
| Uniquely attributable | **31.3%** | 15.3% |
| Ambiguous | 68.7% | 12.7% |
| Not found | 0.0% | 72.0% |

Declared threshold was 40% unique attribution. **31.3% fails it.**

**What went wrong, and it is not a bug.** Real filings average 994 numeric figures each, and 80.7%
of them inherit their denomination from a table header rather than stating it. When a figure is
quoted at memo precision ("$5.2 billion"), on average 4.2 genuinely distinct locations in the same
document match it. The number being present in the cited document is therefore *not* evidence that
the citation is correct — which is the precise mechanism behind attribution hallucination, now
measured rather than asserted.

**A first attempt measured a mistake, not the world.** The initial version pointed at Form D
`primary_doc.xml`, which turned out to be the structured source itself: about a thousand characters
of addresses and one or two figures. It reported one number per document and 0% attribution. Testing
the easy case a second time and calling it the hard case is exactly the failure this log exists to
catch, so it is recorded rather than quietly fixed.

**The scale handling does work, and that part is worth keeping.** The digit-string baseline fails to
find 72% of figures that are demonstrably in the document, because table denominations make
5,234 mean 5,234,000. Handling units correctly is necessary. It is just not *sufficient* for
attribution.

### H2 verdict

**Dead as a standalone deterministic product.** Arithmetic can confirm a number is consistent with a
document, and it does that with no false alarms where LLMs produce 95–100% false positives on clean
statements. What it cannot do is decide *which* of several matching locations was cited, and that is
the question a reviewer actually needs answered. Two thirds of real cases land there.

What survives is narrower and worth stating precisely, because it is the only defensible claim
produced by two experiments:

> Deterministic checking is a sound *filter*, not a verifier. It settles unit and precision
> consistency at zero false-alarm cost, and it can prove a claim is *inconsistent* with its source.
> It cannot confirm attribution when a figure recurs, which is the common case in real filings.

A product built on this would have to sell the filter and be honest that ~69% of quantitative
citations still need a human or a model to disambiguate. That is a smaller claim than "we remove the
verification tax", and the survey numbers that motivated the idea are about the whole tax.

---

## Running score

| # | Hypothesis | Verdict |
|---|---|---|
| H0a–H0d | agentic PR risk, model authority graph, agent practices, harness effect | dead / abandoned |
| H1 | point-in-time evidence layer | dead — occupied by BackSearch |
| H2 | deterministic attribution verification | dead as product; survives as a filter component |

Six hypotheses tested, six negative or narrowed. The consistent pattern across all six: the
*measurement* is sound and cheap, the *market claim* does not survive the measurement. That is now a
finding about the search itself, not about any one idea.

**Method change after H2.** Six failures shared one cause: each began with a capability and looked
for a buyer. The next candidates come from the opposite direction — observed payments for manual
work — because a task someone already pays for does not need its demand hypothesised.

---

## Behavioural evidence: what is already being paid for (collected 2026-07-28)

Job postings, marketplace bids and vendor price lists, gathered because they are payments rather
than opinions. Prices are as published.

**Data vendors staff manual collection as a standing function.**
PitchBook advertises an Operations Associate at $72,000 in Seattle whose stated work is web
scraping, entering data from public documents, researching hard-to-find information and contacting
executives and investors directly — and the posting says the role audits output from PitchBook's
Mumbai data operations team
([Built In](https://builtin.com/job/operations-associate/8565876)). PitchBook's own process page
describes crawlers feeding secondary sources into over 100 proprietary processes with a team
improving the data before publication ([PitchBook](https://pitchbook.com/research-process)), at 2,203
headcount. S&P Global hires Private Markets Data Operations analysts in Mumbai at ₹5–8 lakh to
download GP-portal documents, tag metadata, and extract figures from capital account statements and
cash flow statements ([listing](https://www.talentd.in/jobs/s-p-global-hiring-data-analyst-in-mumbai-5l-8l)).
Preqin (BlackRock) hires analysts whose job is phoning fund managers to obtain proprietary
fundraising and performance data ([Built In](https://builtin.com/job/analyst-preqin-fund-manager-data/8502402)).

**The same work clears on freelance marketplaces at hourly rates.**
A live Freelancer.com project for a Middle East alternative-investor list — 200–500 entries with AUM,
mandate, ticket size and named decision-makers plus source URLs — was posted at £10–15/hour and drew
23 proposals at an average bid of £14/hour, awarded at £13
([project](https://www.freelancer.com/projects/data-collection/middle-east-alternative-investor-list)).
Multiple bidders named PitchBook, Preqin, Bloomberg and SWFI as their sources. Fiverr's own category
page states investor-sourcing services typically run $45–50
([Fiverr](https://www.fiverr.com/categories/finance/fundraising/investors-sourcing)), with sellers
openly advertising PitchBook access.

**Outsourcing vendors publish price lists for deal sourcing.**
CAPTARGET sells outsourced deal origination at a flat $2,000/month with no success fee, and on the
same page states buy-side retainers historically averaged $5K/month, that the average finder fee its
middle-market clients paid exceeded $240,000, and that one BD professional with tooling costs $400K+
a year ([CAPTARGET](https://www.captarget.com/insights/deal-origination-cost-comparison)). SourceCo
publishes $4,000–8,000/month plus success fee, against an in-house alternative it puts at $250K+ in
year one ([SourceCo](https://www.sourcecodeals.com/deal-sourcing-alternative)). Magistral sells an
LP/GP database at $2,500 for six months plus $1 per custom lead, built by an in-house team
([Magistral](https://magistralconsulting.com/investors-database/)). SG Analytics lists the scope as
screening, benchmarking, contact-information pull, outreach, profiles, comps and sector valuation,
and says explicitly that it identified the manual, repetitive tasks and built them into its suite
([SG Analytics](https://www.sganalytics.com/investment-research/private-equity-services/)).

**Size, with the honest caveat.** BFSI is about 28.4% of a KPO market variously put at $104–143bn for
2026, and analytics/market research is the largest service segment at 37.4%; India delivers 70%+ of
it. No published source isolates "investment research outsourcing" as its own category, so the
defensible statement is a bound of roughly $30–40bn of BFSI knowledge-process spend containing this
work among several sub-functions, not a market size for it
([compiled statistics](https://stealthagents.com/research/knowledge-process-outsourcing-statistics-2026),
[Mordor](https://www.mordorintelligence.com/industry-reports/knowledge-process-outsourcing-market)).

Content rephrased for compliance with licensing restrictions.

**Two countervailing signals, recorded because they cut against the thesis.** Upwork data-entry
demand reportedly fell 43% year over year, and more than 52% of KPO tasks already integrate some form
of automation. Both suggest the automatable portion is being automated by incumbents who already hold
the customer relationship, which is a serious objection to entering here.

---

## H3 — The bottleneck is entity resolution, not extraction (under test)

**What the evidence actually points at.** Across every posting and vendor listing above, the recurring
verb is not "read the document" — models do that adequately now. It is *match*: tie this filing to
that fund, this fund to that manager, this person to that firm, and decide whether two records are
the same entity. PitchBook pays a Seattle associate to audit Mumbai's output; S&P pays analysts to
resolve QC exceptions; freelance bidders assemble one list from five overlapping sources.

**Why it fits the non-prediction filter.** Two records either refer to the same entity or they do
not. It is a matching problem with a ground truth, not a forecast.

**Why it might still be worthless, declared in advance.** Entity resolution is a mature field with
mature tooling (Splink, Dedupe, Zingg, commercial MDM). If standard string-similarity matching
already resolves private-market entities well, there is no problem left to solve and H3 dies.

**Falsification conditions, declared before the test:**
1. If off-the-shelf fuzzy matching resolves SEC issuer identities at high accuracy, H3 is dead — the
   problem is solved and the market is buying labour out of inertia.
2. If the hard cases are hard for reasons no method can fix (genuinely ambiguous public records),
   H3 is also dead, because a product cannot beat missing information.

### H3 result — EXP-005. **Survives.** First hypothesis to do so.

Ground truth is free and unlabelled by hand: SEC assigns a CIK per issuer, while filers type the
issuer name as free text. Same CIK with different name strings gives known positives; different CIKs
give known negatives. 35,366 CIKs, 1,654 with more than one name variant, 13,773 labelled pairs.

Matcher: `max(token-set Jaccard, sequence ratio)` with legal-form suffixes stripped — the standard
approach, with the threshold swept so a negative result cannot be blamed on a bad cut-off.

| Stratum | n | Accuracy at 0.75 |
|---|---:|---:|
| positive_easy (same CIK, similar names) | 1,480 | 87.6% |
| **positive_hard** (same CIK, dissimilar names) | 293 | **0.0%** |
| negative_easy (random different CIKs) | 6,000 | 100.0% |
| **negative_hard** (different CIKs, similar names) | 6,000 | **73.3%** |

Best achievable threshold 0.78: balanced accuracy 80.0%, sensitivity 70.9%, specificity 89.0%.

**Neither declared kill condition fires.** Hard-negative accuracy is 73.3%, far below the 95% floor
at which the problem would have counted as solved. And the failures are not caused by missing
information — the information is there, string similarity is simply the wrong instrument.

The examples show why, and they are the most useful output of this whole search:

*Different companies scoring as identical:* `GOBI INVESTMENT PARTNERS LP` vs
`GOBI INVESTMENT FUND LTD.` scores **1.00** after suffix stripping and is a false merge.
`Barrington Holdings, LLC` vs `Barrington Mill Holdings, LLC` scores 0.90.
`SERVANT PHARMACY OF VIRGINIA LLC` vs `SERVANT HEALTH OF VIRGINIA LLC` scores 0.84.

*Same company scoring as unrelated:* `Cyalume Technologies Holdings, Inc.` vs
`Vector Intersect Security Acquisition Corp.` scores 0.19 — a SPAC merger.
`DOR BIOPHARMA INC` vs `SOLIGENIX, INC.` scores 0.40 — a rebrand.
`Desert Hawk Gold Corp.` vs `LUCKY JOE MINING CO` scores 0.30.

Every hard positive here is a *corporate event*: rebrand, SPAC merger, holding-company
restructure. No string method can recover those, because the evidence is not in the name — it is in
the filing history, which is exactly what the point-in-time pipeline already reconstructs. That is
the first genuine overlap found between the research assets and an observed, priced pain.

**Caveat that must be tested next.** Suffix stripping causes some of the false merges, so part of the
73.3% is an artefact of the specific matcher rather than intrinsic difficulty. The next test must
check whether a stronger baseline (blocking + probabilistic matching, e.g. Splink-style) closes the
gap. If it does, H3 narrows sharply.

### H3 second test — EXP-006. **Survives a stronger baseline.**

Seven matchers on the same pair construction, each given its best threshold by sweep. **Numbers below
are the reproducible post-fix values, corrected 2026-07-29** — see the note after the table.

| Matcher | Balanced acc. | neg_hard | pos_hard | pos_easy |
|---|---:|---:|---:|---:|
| Jaccard, suffixes stripped | 77.4% | 68.7% | 4.4% | 83.6% |
| Jaccard, suffixes kept | 79.2% | 60.2% | 7.5% | 92.4% |
| Sequence ratio | 80.1% | 78.3% | 0.0% | 85.2% |
| **Character 3-grams** | **80.8%** | 74.4% | 1.0% | 89.1% |
| IDF-weighted tokens | 78.3% | 66.1% | 3.4% | 87.4% |
| IDF + head-token | 76.0% | 62.9% | 7.5% | 83.1% |
| Best of all | 80.2% | 78.2% | 0.0% | 85.3% |

**The string ceiling is about 81% balanced accuracy.** Adding IDF weighting — the mechanism inside
probabilistic record linkage — makes it *worse*, not better. Hard positives stay at 0–8% across every
method, and taking the best of all seven (80.2%) does not beat the best single one (80.8%), which is the
signature of a ceiling. The gap EXP-005-ER found is real and is not an artefact of a weak matcher.

> ⚠️ **Why these numbers changed, and why that is itself a finding.** A reproducibility check on
> 2026-07-29 (`code/verify_p1_reproducibility.py`) found that this experiment did **not** reproduce
> between runs despite a fixed seed. Three separate executions gave a best matcher of 81.1%, 81.0% and
> 80.8%. The cause: the pair construction iterated over Python *sets of strings*, and string hashing is
> randomised per interpreter process, so the blocking lists were assembled in a different order each
> time and the truncated sample of hard negatives differed. **A seed does not protect against this** —
> which is the transferable lesson, because the code looked correctly seeded.
>
> The iteration points are now sorted and both entity-resolution experiments reproduce byte-identically.
> Every figure in this section, in EXP-006's report and in the working paper §6.1 has been replaced with
> the post-fix values. The qualitative conclusion never moved across any of the three runs: the ceiling
> sits near 81%, the best-of-all does not beat the best single matcher, and hard positives collapse.
> Earlier readings of the pre-fix artefacts should be treated as draws from a distribution.

### A circular test caught and corrected

The first run of EXP-006 reported **100% attribute agreement on same-entity pairs** and I did not
believe it. Probed directly: attributes were being looked up by CIK, while a positive pair is
*defined* as two names sharing a CIK. Both sides returned the same record, so agreement was
guaranteed. Verified: 1770/1770 positive pairs resolved to a single CIK. **The label was the lookup
key.**

Fixed by keying attributes on `(cik, name)`, so each side is described only by the filings that
carried its own name string — the information a matcher would actually have. After the fix, agreement
on positives drops from 100% to 87–96%, which is a plausible number rather than a tautology.

This is the third circular or invalid result caught by an assertion in this project (after the 846
overlapping CIKs in EXP-002 and the 578/586 zero-file records in the agentic PR work). The pattern is
consistent enough to be worth stating: **every result that looked clean turned out to be circular.**

### The corrected, valid result

| Attribute | Agreement, same entity | Agreement, different entity | Gap |
|---|---:|---:|---:|
| State of incorporation | 91% | 37% | **+54%** |
| Entity type | 95% | 56% | **+39%** |
| Industry group | 87% | 61% | **+26%** |

Coverage 99.8% of pairs. All three separate the cases strings cannot decide, and they are cheap
public fields already in the filings.

**What this means, stated carefully.** Strings top out at 81%. Non-name evidence that any filing
carries — state, entity type, industry, and by extension filing timeline — separates same-entity from
different-entity pairs by 26–54 points precisely where string similarity is at chance. The hard
positives are corporate events (rebrands, SPAC mergers, restructures) whose evidence lives in filing
*history*, not in the name.

That is the first real overlap found between the point-in-time pipeline and a pain someone is
observably paying for: PitchBook staffs a Seattle associate to audit Mumbai's matching output, S&P
staffs analysts to clear QC exceptions, and freelancers charge £13–14/hour to reconcile overlapping
sources by hand.

**Still not a product claim.** Three gaps remain, and the third is the serious one:
1. Ground truth here is SEC CIK, which exists *because* the SEC assigns it. In the commercial problem
   there is no CIK — that is what has to be inferred. This measures difficulty, not solvability.
2. The corpus is Form D issuers, not the LP/GP/fund graph where the freelance money actually flows.
3. Incumbents already own the customer and already automate: over 52% of KPO tasks reportedly involve
   some automation, and Upwork data-entry demand fell 43% year on year. Being right about the
   bottleneck does not create an entry point.

**Status:** survives two falsification attempts as a *technical* claim. Rejected as a company shape —
see below.

### H3 rejected on shape, not on evidence (owner objection, 2026-07-28)

The owner's objection: entity resolution is a feature inside someone else's product, not a company.
It is correct, and the reasoning matters more than the conclusion.

Entity resolution has one buyer type — organisations that maintain a database — and there are
perhaps a few hundred of them worldwide. Each has already built an internal version, staffed it, and
is already automating it. The measured 81% string ceiling is a real gap, but selling into it means
selling a component to companies whose core competence is that component. That is a services or
acquisition outcome, not the thing being looked for.

**A precedent worth noting, because it is the counter-example.** The identifier layer *can* be a
large business: D&B built one around the DUNS number, which is issued free and yet underpins a public
company, because it became the identifier everyone else quotes. GLEIF's LEI passed 3 million active
records in Q1 2026 with roughly 100,000 organisations obtaining one in the quarter, and nine US
financial agencies finalised a joint rule in June 2026 promoting interoperability of regulatory data
([GLEIF](https://www.gleif.org/en/newsroom/blog/the-lei-in-numbers-active-lei-population-surpasses-3-million-in-q1-2026),
[GLEIF on the FDTA rule](https://www.gleif.org/en/newsroom/blog/number-22-in-the-lei-lightbulb-blog-series-the-lei-in-u-s-law-what-the-fdta-final-joint-rule-means/)).
OpenCorporates holds over 220 million companies from 145 jurisdictions, provenanced to official
sources ([GLEIF](https://www.gleif.org/en/lei-data/lei-mapping/download-oc-to-lei-relationship-files/)).
Content rephrased for compliance with licensing restrictions.

So the difference between "feature" and "the obvious place to look" is not the technical work — it is
whether the output becomes the thing others cite. D&B and GLEIF got there through free issuance plus
a regulatory or procurement mandate. Neither is available to a single founder, and the identifier
space for legal entities is already occupied by both a free public utility and an incumbent.

**Recorded consequence for the search, not just for H3.** The behavioural-evidence method that
produced H3 has a systematic bias: observed payments for manual work point to *back-office* problems,
because that is where labour is itemised and invoiced. Back-office problems have few buyers by
construction. Finding "the obvious place to look" requires the opposite signal — many people
searching for the same thing and not finding it — which is a demand signal, not a payroll signal.

---

## What the owner is actually asking for, stated as testable properties

Rejecting H3 clarified the target. The requirement is not "a big market"; it is a specific structure:

| Property | Why it matters | Observable before building? |
|---|---|---|
| Many independent seekers | few buyers caps the outcome regardless of quality | yes — search volume, forum questions |
| The same question recurs | one-off lookups do not build habit | yes — repetition in public questions |
| Answer exists but is scattered | if it does not exist, no retrieval helps | yes — check whether sources exist |
| Being cited compounds | otherwise it stays a tool, not a reference | partly — check for existing citation |
| No incumbent owns the query | D&B/GLEIF own legal-entity identity already | yes — search and see who ranks |

The fifth column is the important one: all five are checkable from public data *before* writing code.
That is the method correction. The previous seven hypotheses each began with a capability; the next
must begin with an unanswered recurring question.

**Search signal to look for, declared before searching:** many people, asking repeatedly, a question
whose answer is public but scattered, where the current top result is a forum thread or a paywall
rather than a purpose-built source.

**Status of the search:** method redirected.

---

## H4 — Query-space search in AI / public / private markets. **Dead: occupied.**

Searched for recurring public questions without a purpose-built source.

* **13F / institutional holdings** — saturated: 13f.info, WhaleWisdom, Fintel, HoldingsChannel,
  GuruFocus, WallStRank, all free.
* **"Who owns this brand / is it PE-owned?"** — occupied within the last year by at least four consumer
  sites: [Know The Owners](https://knowtheowners.com/), [PE Reveal](https://www.pereveal.com/)
  (free, starting with veterinary care), [peruinedthis.com](https://peruinedthis.com/),
  [FreeFromPE.com](https://freefrompe.com/). Demand was real — KFF documented close to $1 trillion
  invested through thousands of healthcare deals in a decade
  ([KFF](https://www.kff.org/health-costs/kffs-kaiser-health-news-investigates-private-equitys-stealth-takeover-of-health-care-in-the-united-states/))
  — which is precisely why supply arrived.

Content rephrased for compliance with licensing restrictions.

**Structural conclusion, recorded so it is not re-tested.** A question that is publicly visible,
frequently asked, and answerable from public sources attracts builders in months. Anything findable
by search has been found by search. The two known routes to becoming the default reference — free
issuance plus a regulatory mandate (D&B's DUNS, GLEIF's LEI), or a two-decade head start with a
terminal (Bloomberg) — are not available to a solo founder.

---

## H5 — An orchestration layer that runs several models and derives a better output. **Dead, twice over.**

Owner's hypothesis: with AI you now get lost inside building a product, a feature, a piece of
research, the way you used to get lost looking for a page on the web. So something should *order* the
models' work for ordinary users, cheaply, running several outputs and deriving a better one.

### Problem 1 — the consumer product exists and is being sold at commodity prices

ChatPlayground puts 20+ models behind one prompt with side-by-side comparison, and is currently being
marketed as a **lifetime deal at $60–79** across PCWorld, Macworld, BleepingComputer, PopSci and
Lifehacker ([PCWorld](https://www.pcworld.com/article/3188274/access-chatgpt-claude-and-gemini-for-a-flat-60.html),
[Macworld](https://www.macworld.com/article/3187213/chatgpt-is-20-month-but-this-app-gives-you-chatgpt-claude-and-gemini-for-life-for-60.html)).
OpenRouter ships Fusion for exactly this multi-model comparison
([guide](https://app.therundown.ai/guides/how-to-test-multiple-ai-models-with-the-same-prompt-fast)).
A lifetime licence at $60 sold through discount-deal channels is the price of a category with no
pricing power left.

### Problem 2 — the technical premise is contested, and this is the real objection

The idea assumes that combining outputs from *different* models yields a better one. The strongest
published test of that assumption says otherwise. **Self-MoA** — ensembling repeated outputs from only
the single best-performing model — beat standard Mixture-of-Agents mixing different LLMs, by 6.6% on
AlpacaEval 2.0 and 3.8% on average across MMLU, CRUX and MATH
([arXiv 2502.00674](https://arxiv.org/abs/2502.00674),
[OpenReview](https://openreview.net/forum?id=K6WwK8URlV)). Related work finds multi-agent committees
suffer *representational collapse*, contributing correlated rather than complementary evidence
([arXiv 2604.03809](https://arxiv.org/pdf/2604.03809)), and that useful aggregation has to happen at
the level of the reasoning trace rather than the final answer
([arXiv 2605.29116](https://arxiv.org/pdf/2605.29116v1)).

Content rephrased for compliance with licensing restrictions.

**Why this kills it rather than narrowing it.** Mixing models pays only when the models make
*different* mistakes. Frontier models are trained on overlapping data with overlapping methods, so
their errors correlate — and averaging correlated errors adds cost without adding information. This
is the same failure as H0b (the app→model graph): the diversity that the idea depends on is not there.

**What is not dead.** The owner's *diagnosis* — that the bottleneck has moved from finding information
to not getting lost inside an over-abundant workspace — is not addressed by comparison UIs, and no
falsifying evidence was found against it. But the proposed mechanism (run many models, synthesise a
better answer) is the wrong instrument for it, on published evidence.

---

## Running score, final

| # | Hypothesis | Verdict |
|---|---|---|
| H0a | Agentic PR risk predictable pre-review | dead — AUC 0.54–0.59 |
| H0b | Model authority derivable from usage graph | dead — recursion ≈ token count |
| H0c | Controllable agent practices separate outcomes | dead — 0/8 actionable |
| H0d | Harness choice changes real-code outcomes | abandoned — confounder not removable |
| H1 | Point-in-time evidence layer | dead — occupied (BackSearch) |
| H2 | Deterministic attribution verification | dead as product; survives as a filter |
| H3 | Entity resolution is the bottleneck | technically sound; rejected as company shape |
| H4 | Unserved recurring query in AI/markets | dead — occupied |
| H5 | Multi-model orchestration for ordinary users | dead — occupied *and* premise contested |

**Nine hypotheses, one technically sound and commercially rejected.** The failures split cleanly into
two causes, and the split is the finding:

* **Prediction ceilings** (H0a, H0b, H0c): the signal is not there.
* **Occupied space** (H1, H4, H5): the signal was there and someone reached it first.

No hypothesis failed because it was badly executed. Every one failed on evidence, in hours. That is
the method working, and it is also the reason a search of this kind cannot produce a category-defining
company: what is reachable by searching has already been reached.

---

## H6 — A free, model-agnostic layer that keeps an agent on task

Owner's specification: free, bring your own model, guides toward the solution without losing the
context or opening many directions it never closes.

### The problem is real, named, and quantified

This is the first candidate whose *problem statement* is confirmed by independent measurement rather
than merely unfalsified.

* **Context rot.** Accuracy degrades with position in the context window, with one report citing
  GPT-4 falling from 98.1% to 64.1% depending solely on where information sits — no error signal, just
  quietly worse answers ([tianpan.co](https://tianpan.co/blog/2026-02-26-context-engineering-memory-compaction-tool-clearing)).
  Degradation is described as predictable after roughly 20–30 conversation turns
  ([TechAhead](https://www.techaheadcorp.com/blog/context-rot-problem/)).
* **Losing the objective.** Error analysis of long-context web agents finds failures come primarily
  from getting stuck in loops and losing track of the original task
  ([arXiv 2512.04307](https://www.arxiv.org/pdf/2512.04307)).
* **Abandoning work mid-trajectory.** One white paper names the mode "context fatigue": agents declare
  tasks complete prematurely, substitute placeholder data, and abandon original intent
  ([MindAptiv](https://mindaptiv.com/context-fatigue)).
* **Stale state.** The memory-update gap scales with conversation length rather than compression ratio
  ([arXiv 2606.27472](https://arxiv.org/abs/2606.27472)).
* **Agent drift** in multi-agent systems over extended interactions
  ([arXiv 2601.04170](https://arxiv.org/abs/2601.04170)).

Content rephrased for compliance with licensing restrictions.

The owner's diagnosis — "you get lost inside the work the way you used to get lost in the web" — maps
onto a measured failure mode with a literature. That is a first in this log.

### The solution space is crowded, and the irony is worth recording

Spec-driven development is the established answer: the spec is the durable artefact, the code is
generated against it. Tools in market: **Kiro** (spec-driven built into the IDE), GitHub **Spec Kit**,
**Tessl**, **Zenflow**, **OpenSpec** (open-source, YC-backed, "durable context for coding agents"),
and **BMAD** (portable methodology running on tools you already use)
([InfoWorld](https://www.infoworld.com/article/4171332/4-cutting-edge-tools-for-spec-driven-development.html),
[OpenSpec on YC](https://www.ycombinator.com/companies/openspec),
[heise on OpenSpec 1.6](https://www.heise.de/en/news/Specs-first-OpenSpec-sorts-out-the-AI-chaos-during-development-11362849.html),
[Turing Post](https://www.turingpost.com/p/sdd)).

**Kiro is the environment this conversation is taking place in.** The requested product is a
description of the tool already being used to search for it. OpenSpec occupies the free,
model-agnostic, open-source position specifically.

### Verdict

**Dead as specified.** Free + bring-your-own-model + keeps the agent on task is OpenSpec's exact
position, with YC backing and an active release cadence. BMAD occupies the portable-methodology
variant. The category has a name, a literature, and at least six named entrants within a year.

### The one thing not occupied

Every tool listed enforces discipline on *building*: requirements, design, tasks, code. None found
enforces discipline on *deciding whether to continue* — which is the failure that actually consumed
this conversation. Nine directions opened; what closed them was not a spec but a threshold declared
before the test and a record of what had already been excluded.

That is the value-of-information problem under a capacity constraint, i.e. the owner's own research
subject, applied to exploration rather than to diligence. Recorded as an observation, **not** promoted
to H7: it is one step from being the tenth idea generated by the same reflex that produced the first
nine, and the search has not earned another.




