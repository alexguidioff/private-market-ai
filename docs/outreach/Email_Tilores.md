# Outreach — Tilores (Tilo Tech GmbH, Berlin)

**Drafted 2026-07-30.** Attachment: `Note_Tilores_CompanyER.md`, exported to PDF.

## Who they are, verified from their own site

Tilo Tech GmbH trading as Tilores, Fabeckstraße 62, 14195 Berlin. SOC 2 certified, on AWS Marketplace,
HRB 235279 B. Leadership: **Dr Steven Renwick (CEO), Hendrik Nehnes (CTO), Stefan Berkner (CDO)**.
Customers include Exiger, Inato, Grover, Cofinity-X. The Exiger case study is **110M+ company records
from 16 sources resolved into 60M entity clusters** for supply chain risk, so company entities are
their core hard case rather than a side use.

They publish reproducible public benchmarks and state where the competitor wins, which is why an
artefact is the right first contact and a pitch is not.

## Channel, in order

1. **GitHub issue or discussion on the benchmark repo** under [github.com/tilotech](https://github.com/tilotech).
   Best first move: it is public, technical, and it is publishing rather than networking. Link the note.
2. **LinkedIn to Stefan Berkner (CDO)**, then Steven Renwick (CEO). The CDO owns a data benchmark.
   Point at the GitHub issue rather than repeating it.
3. `privacy@tilores.io` is the only published address and it is a legal inbox. Fallback only, expect slow routing.
4. Do **not** use the "Book a 30-min demo" form. That routes to sales and frames you as a buyer.

⚠️ Do not guess an email pattern like first.last@tilores.io. Unverified.

---

## Message

**Subject:** Company-name entity resolution: your Splink benchmark extended, and a circularity in how hardness gets defined

Hello,

I read your public Splink benchmark and ran the same kind of comparison on a case it does not cover:
company names, where legal-form suffixes and corporate events break string matching in ways that person
and product records do not.

The data is SEC Form D. The regulator assigns a CIK while filers type the issuer name freely, so the
same CIK gives free positives and different CIKs give free negatives. 13,773 labelled pairs, fully
public, reproducible end to end.

Out of sample, Splink 4 reaches 77.3% balanced accuracy and ROC-AUC 0.806, against 80.7% and 0.869 for
a plain token matcher, and its blocking proposes 38.2% of the labelled pairs. A supervised classical
baseline beats both of us on average precision, 0.688, which is the metric that matters for a review
queue, so I report it rather than leading with the one where I win. None of this is comparable to your
F1 0.9949: different data, and that is the point. Company names sit far below what person and product
benchmarks produce.

The part I think is actually useful to you is a flaw I found in my own design. I had defined hard
positives as pairs with low string similarity, then evaluated string matchers on them, so the 0% there
is definitional rather than empirical. Running the same protocol on FEBRL reproduces the 0%, which
confirms it. Anyone stratifying difficulty by the score under test has the same problem.

The note is attached. Two questions. Would you want to comment before I publish it, and is this the
kind of work you would consider bringing someone in to do?

Alessandro Guidi
alexguidioff@gmail.com · github.com/alexguidioff

---

## Rules for this one

- **No em dashes.** Checked.
- Do not claim to beat their product. The non-comparability sentence is load-bearing, keep it.
- Lead with what is useful to them, disclose the own-goal, ask last. The job question is one clause at
  the end, not the purpose of the email.
- **Publish the repo first or at the same time.** The email says "before I publish", which implies
  publication is actually happening. If there is no public artefact behind it, the sentence is empty and
  they will notice.
- If they reply with a Splink configuration to try, run it and report the result even if it beats you.
  That is the entire basis of the credibility being claimed here.
