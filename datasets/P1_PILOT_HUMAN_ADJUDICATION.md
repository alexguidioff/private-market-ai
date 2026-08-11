# P1 Pilot — Human Adjudication Packet

**Purpose:** resolve five AI-review disagreements and audit five agreements before scaling.  
**Codebook:** `P1_OPEN_SOURCE_LABEL_PLAN.md` v1.1 semantics.  
**Important:** the human decision must be recorded by the user or another named reviewer; it must not
be silently replaced by another model pass.

## Decision fields

For each case record:

- `identity_resolved`: yes/no/unknown;
- Layer A `financing_event_label`: positive/no_public_evidence/unknown;
- `event_in_window`: yes/no/unknown;
- `evidence_available_by_window_end`: yes/no/unknown;
- Layer B `strong_round_label`: positive/not_qualifying/unknown;
- `priced_round` and `institutional_investor`: yes/no/unknown;
- chosen evidence URL and one-sentence rationale.

## Five conflicts

### 1. Collision Communications — P1G-7942FC70DACB
Window: `(2018-03-01, 2019-09-01]`. A Form D/A filed in November 2018 reports cumulative proceeds
but retains first sale 2016-03-02. Decide whether any sale can be dated inside the window. Under the
revised rule, cumulative growth without dated sales should normally remain `unknown`, not positive.
Evidence: https://www.sec.gov/Archives/edgar/data/1633056/000163305618000001/primary_doc.xml

### 2. Its the Ice — P1G-83F2EB87538B
Window: `(2017-01-14, 2018-07-14]`. The queue CIK and accession-prefix CIK differ, and public identity
is weak. Resolve the issuer identity before assigning absence semantics.
Evidence: https://www.sec.gov/Archives/edgar/data/1663655/000166365416000002/primary_doc.xml

### 3. Esportz Entertainment — P1G-92460E6477B6
Window: `(2020-04-15, 2021-10-15]`. A new non-amendment Form D reports first sale 2020-12-15 and
$500,000 sold. Under v1.1 this is sufficient for Layer A, but not for Layer B without pricing and a
named institutional investor.
Evidence: https://www.sec.gov/Archives/edgar/data/1772919/000177291921000002/primary_doc.xml

### 4. Sounding Board Labs — P1G-BC4E13AE073B
Window: `(2018-09-11, 2020-03-11]`. Confirmed $1M seed reporting is one day before the window;
secondary sources suggest later financing but conflict on date/amount. Decide whether evidence is
strong enough to date an event inside the window or must remain unknown.
Evidence: https://techcrunch.com/2018/09/10/at-sounding-board-an-executive-coaching-startup-the-coaches-get-coaching-too/

### 5. Cyemptive Technologies — P1G-EDA53A35A597
Window: `(2019-08-15, 2021-02-15]`. A Form D published 2021-06-17 reports first sale 2020-12-01 and
$1.31M sold. Under v1.1 it can establish Layer A ex post with `event_in_window=yes` and
`evidence_available_by_window_end=no`; it cannot be a PiT feature or establish Layer B alone.
Evidence: https://www.sec.gov/Archives/edgar/data/1750099/000175009921000001/primary_doc.xml

## Five agreement audits

Audit at least these records against the same rules: Jellysmack (`P1G-002FDE7E3020`), Datasembly
(`P1G-89A546B1DA2D`), Dialpad (`P1G-C3470EF06FC4`), EnerConnex (`P1G-02B8166A4496`) and Six Trees
(`P1G-4C6F8E29938B`). Verify that sources support Layer A and do not overstate Layer B.

## Scale gate

Proceed to the remaining 180 only after the adjudicator signs/date-stamps this packet, identity is
usable in at least 90% of the audited pilot, unresolved cases are at most 25%, and Layer B has enough
positives to evaluate rather than merely describe coverage failure.
