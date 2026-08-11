# P1 Open-Source Label Plan

Status: executable plan; no proprietary database is required for the reproducible core.
Last reviewed: 2026-07-21.

## 1. What "open-only" means

P1 can be executed with public or openly reusable sources, but the evidence layers must not be
collapsed:

1. **Public point-in-time observations** reconstruct what was publicly knowable at the decision
   cutoff. They are features and provenance, not decision-quality ground truth.
2. **SEC weak outcome proxy** records a later exempt-offering notice. It is reproducible but is not
   a Series A, institutional round, fundraising success, or company-success label.
3. **Adjudicated public benchmark** uses contemporaneous public evidence reviewed under a written
   protocol. It can support stronger empirical labels, while retaining `unknown` when evidence is
   insufficient.
4. **Simulator ground truth** is known by construction and supports recovery/counterfactual tests,
   not claims that the synthetic world represents private markets.

A commercial source may later be evaluated as an optional information acquisition, never as a
prerequisite for reproducing the base experiment.

## 2. Source roles and current gates

| Source | Defensible use | Does not establish | Gate |
|---|---|---|---|
| SEC Form D | filing availability, issuer-reported offering fields, later notice | round stage, institutional participation, success | accepted core |
| Issuer press release/site | announced stage, amount, named investors, event date | unannounced events or economic health | primary gold evidence |
| Investor portfolio/announcement | claimed participation and portfolio relationship | complete terms or exact close date unless stated | primary/confirming evidence |
| SEC IAPD/Form ADV | adviser identity/status and reported business | participation in a specific issuer round | accepted corroboration |
| State business registry | legal entity identity/status where accessible | operating health, venture backing | jurisdiction audit required |
| OpenAlex | research/publication signals; CC0 snapshot | founder identity without matching review | candidate acquisition block |
| GDELT | dated news discovery/indexing | truth of an article or rights to republish it | discovery only |
| Common Crawl | historical page discovery and capture date | truth; copyright transfer | discovery/archive only |
| GitHub | public technical activity where identity and cutoff are defensible | company health; complete 2016--2020 history via current Events API | blocked pending archive audit |
| Wikidata | aliases and entity-resolution candidates | gold evidence by itself | support only |
| OpenCorporates | candidate legal-entity matching | unrestricted API access/redistribution | conditional; verify terms per run |
| OpenVC | investor discovery through its service | open licensed dataset or historical PiT evidence | excluded from core |


## 3. Gold benchmark: 200 issuer-anchors

Generate a deterministic sample from `p1_first_anchor_model_ready.csv`:

- 100 SEC weak-proxy positives and 100 weak-proxy negatives;
- stratified by anchor year, SEC industry group and amount-sold quartile;
- one issuer CIK per row; use `canonical_company_id` once reviewed;
- keep the existing temporal splits and report their realized counts;
- reviewers are blinded to the SEC weak label;
- the final strong label may be `positive`, `no_public_evidence`, or `unknown`.

The balance is a review design, not a population estimate. Performance must be reweighted to the
population prevalence or reported by class. The 100 weak negatives are search cases, not known
negative outcomes.

Run:

```powershell
python code/sample_p1_gold_labels.py
```

Local, git-ignored outputs are written under `datasets/processed/sec_form_d_v2/gold/`:
`annotation_queue.csv`, `sampling_audit.csv`, and `sampling_manifest.json`.

## 4. Annotation protocol

For each sampled issuer, search evidence dated no later than the label-window end. Prefer sources in
this order: issuer announcement, named investor announcement/portfolio page, regulator or registry,
then reputable reporting as confirmation. Search engines, GDELT, Common Crawl and Wikidata locate
sources but do not themselves prove the event.

Record the event date separately from publication/availability date. Save URL, source type, access
date, a content hash or archive locator, and a short reviewer rationale; do not copy full copyrighted
articles. A qualifying event must fall in `(decision_time, label_window_end]`. An article published
after the cutoff may audit an event but cannot become a point-in-time feature.

Two reviewers independently classify each case. Disagreement or insufficient evidence goes to
adjudication. `unknown` is mandatory when identity, timing or the requested construct cannot be
established. Never convert missing evidence into failure.

**Fixed search checklist before `no_public_evidence`:** (1) exact legal name + aliases; (2) SEC CIK
and filing history; (3) issuer site/press archive; (4) named-investor or portfolio search; (5) two
reputable-news searches bounded to the window; (6) acquisition/rename/SPV check. Stop after all six
steps are logged. `No_public_evidence` means this checklist found no qualifying event; it remains
an observation about public evidence, not a true economic negative.

## 5. Two label layers

The pilot showed that “financing” and “strong VC round” must be separate targets.

- **Layer A — `financing_event_label`:** any publicly evidenced primary financing whose event date
  falls in `(decision_time, label_window_end]`. A new non-amendment Form D with first-sale date in
  the window is sufficient for Layer A, subject to identity checks. An amendment is sufficient only
  when it supplies a sale date inside the window; a cumulative increase without sale dates is not.
- **Layer B — `strong_round_label`:** a priced equity round with at least one named institutional
  investor. It is positive only when financing, pricing and institutional participation are all
  documented. A Form D alone, an equity checkbox or a Series label alone is insufficient.

Record `event_in_window` separately from `evidence_available_by_window_end`. Evidence published after
the outcome cutoff may establish the ex-post outcome label when it explicitly dates the event, but
must have `evidence_available_by_window_end = no` and can never enter point-in-time features.

`priced_round = yes` requires documentary evidence of priced equity terms (for example class and
price/valuation terms), not merely “Series A”, a valuation headline or an equity Form D. SAFE,
convertible instruments and unspecified equity are `no` or `unknown` according to documented terms.

## 6. Strong-label semantics

The primary adjudicated event is a publicly evidenced financing in the outcome window. `priced_round`,
`institutional_investor`, and `round_stage` are separate ternary/categorical fields; one must not be
inferred from another. In particular:

- first Form D does not imply seed;
- second Form D does not imply Series A;
- amount offered is not amount raised;
- an adviser appearing in IAPD does not prove participation in a particular round;
- no announcement found does not prove no financing or company failure.

The SEC proxy remains in a separate audit table. Agreement with the adjudicated label estimates proxy
precision/coverage; it does not retroactively turn the full SEC cohort into gold data.

## 7. Evidence and release policy

Version the sampling manifest, annotation instructions, schema, source-access dates, adjudication log
and inter-reviewer agreement. Raw pages and local annotations remain git-ignored until rights and
privacy review. A public release should contain only minimally necessary structured facts, provenance
links/hashes, and permitted quotations.

Current official references:

- [SEC Form D datasets](https://www.sec.gov/about/dera_form-d)
- [SEC IAPD](https://adviserinfo.sec.gov/) and [Form ADV data](https://www.sec.gov/foia/docs/form-adv-archive-data.htm)
- [OpenAlex CC0 and API](https://docs.openalex.org/additional-help) and [snapshots](https://docs.openalex.org/download/overview)
- [GDELT data access](https://gdeltproject.org/data.html)
- [Common Crawl access](https://commoncrawl.org/get-started) and [terms](https://commoncrawl.org/terms-of-use)
- [GitHub Events API limits](https://docs.github.com/rest/activity/events)
- [OpenCorporates](https://opencorporates.com/) and [API](https://api.opencorporates.com/)
- [OpenVC legal terms](https://www.openvc.app/legal)

Source access, API limits and redistribution terms must be rechecked at every extraction. This plan is
research governance, not legal advice.