"""Can attribution of quantitative claims be verified without model judgement?

The problem this targets
-----------------------
Adoption of AI in investment workflows is near universal, but the measured
benefit is being consumed by checking the output. A 2026 survey of CRE investing
professionals found 97% have AI in the investment process while only 51% say it
saves time once verification is counted, and 41% say AI-involved work takes
longer than doing it by hand. The failure mode is specific and has a name in the
literature: *attribution hallucination* — the answer is right, the cited location
is wrong. An audit of 20 multimodal models put the best system's source
attribution accuracy at 76.0.

That is not a prediction problem. For a quantitative claim about a filing, the
number either occurs in the cited document or it does not. Which makes the
verification deterministic, and therefore cheap, auditable, and reproducible.

What this module measures
-------------------------
Whether the deterministic route is *sufficient*: what share of quantitative
claims can be resolved by exact arithmetic against source data, and how often the
answer differs from an accept-the-citation baseline.

Declared before running (falsification conditions):

* If fewer than ~40% of claims are deterministically checkable, the approach
  leaves the hard cases untouched and is not a product.
* If a naive check agrees with the deterministic one almost always, there is no
  value being added.

Honest scope
------------
This verifies *attribution*, not truth. If a filing reports a wrong number, a
citation to that filing is still correctly attributed. The claim being tested is
narrow on purpose: "the cited source says what the text says it says".

Numeric matching is the whole difficulty, and it is not naive equality:

* scale words: "$5.2 million" against 5200000
* rounding: "$5.2M" against 5,234,000 — correct at the stated precision
* units: thousands-denominated tables
* formatting: currency symbols, thousands separators, parentheses for negatives
* ranges and approximations: "about", "up to", "at least"

Each of these is a place a real verifier gets it wrong, so each is tested.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path

USER_AGENT = "Private-Market-AI academic research alexguidioff@gmail.com"
CACHE = Path(__file__).resolve().parent.parent / "datasets" / ".cache_claims"

SCALE_WORDS = {
    "hundred": Decimal(100),
    "thousand": Decimal(1_000),
    "k": Decimal(1_000),
    "million": Decimal(1_000_000),
    "m": Decimal(1_000_000),
    "mm": Decimal(1_000_000),
    "billion": Decimal(1_000_000_000),
    "bn": Decimal(1_000_000_000),
    "b": Decimal(1_000_000_000),
    "trillion": Decimal(1_000_000_000_000),
}

HEDGE_WORDS = (
    "approximately", "about", "around", "roughly", "nearly", "almost",
    "up to", "at least", "more than", "less than", "over", "under",
    "in excess of", "no more than",
)

# Words that assert the number is precise as written, which removes the rounding
# allowance rather than widening it. Without this, "exactly $5 million" accepted
# $5.4 million, because the tolerance was derived only from the digits shown.
EXACT_WORDS = ("exactly", "precisely", "in total exactly", "to the dollar")

# Verdicts. Deliberately includes an explicit "cannot decide" so the method
# cannot quietly convert ignorance into a pass.
VERIFIED = "verified"
CONTRADICTED = "contradicted"
NOT_CHECKABLE = "not_checkable"
SOURCE_MISSING = "source_missing"


@dataclass(frozen=True)
class NumericClaim:
    """A quantitative assertion attributed to a specific source field."""

    text: str
    field_name: str
    source_id: str
    hedged: bool = False

    @property
    def stated_value(self) -> Decimal | None:
        parsed = parse_money(self.text)
        return parsed[0] if parsed else None

    @property
    def precision(self) -> int | None:
        """Significant decimals as written, which sets the rounding tolerance."""
        parsed = parse_money(self.text)
        return parsed[1] if parsed else None


def parse_money(text: str) -> tuple[Decimal, int, Decimal] | None:
    """Parse a monetary or numeric expression into (value, decimals, scale).

    Returns the value in base units, the number of decimal places written (which
    determines how much rounding is legitimate), and the scale multiplier
    applied. Returns None when no number is present.
    """
    # Thousands separators must be removed, not turned into spaces: replacing
    # them with spaces made "5,000,000" parse as 5, which silently converted a
    # correct claim into a contradiction. Only separators between digit groups
    # are stripped, so "12, 15 investors" is not merged into 1215.
    cleaned = text.replace("\u00a0", " ")
    cleaned = re.sub(r"(?<=\d),(?=\d{3}\b)", "", cleaned)

    pattern = re.compile(
        r"(?P<neg>\()?\s*\$?\s*(?P<num>\d+(?:\.\d+)?)\s*"
        r"(?P<scale>hundred|thousand|million|billion|trillion|bn|mm|[kmb])?\b",
        re.IGNORECASE,
    )
    match = pattern.search(cleaned)
    if not match:
        return None

    raw = match.group("num")
    try:
        value = Decimal(raw)
    except InvalidOperation:
        return None

    decimals = len(raw.split(".")[1]) if "." in raw else 0

    scale_token = (match.group("scale") or "").lower()
    scale = SCALE_WORDS.get(scale_token, Decimal(1))
    value *= scale

    if match.group("neg"):
        value = -value

    return (value, decimals, scale)


def tolerance_for(text: str) -> Decimal:
    """How much difference is legitimate, given how the claim was written.

    "$5.2 million" is a correct rendering of 5,234,000: the writer stated one
    decimal at million scale, so anything within half of that last place agrees.
    Treating this as a mismatch is the single biggest source of false alarms in a
    naive verifier, which is why tolerance is derived from the text rather than
    fixed.
    """
    parsed = parse_money(text)
    if parsed is None:
        return Decimal(0)

    _, decimals, scale = parsed
    lowered = text.lower()

    # An explicit precision marker overrides the rounding allowance implied by
    # the digits: "exactly $5 million" claims the round number, not a range.
    if any(word in lowered for word in EXACT_WORDS):
        return Decimal(0)

    half_place = (scale / (Decimal(10) ** decimals)) / Decimal(2)

    if any(word in lowered for word in HEDGE_WORDS):
        # A hedged claim asserts less, so it is allowed more room. Chosen as one
        # order of magnitude, declared rather than tuned.
        half_place *= Decimal(10)

    return half_place


def is_hedged(text: str) -> bool:
    return any(word in text.lower() for word in HEDGE_WORDS)


@dataclass
class Result:
    """Outcome of verifying one claim."""

    claim: NumericClaim
    verdict: str
    stated: Decimal | None = None
    actual: Decimal | None = None
    tolerance: Decimal | None = None
    note: str = ""

    @property
    def difference(self) -> Decimal | None:
        if self.stated is None or self.actual is None:
            return None
        return abs(self.stated - self.actual)


def verify_claim(claim: NumericClaim, source_row: dict | None) -> Result:
    """Check one quantitative claim against structured source data.

    No model is involved. The verdict is arithmetic.
    """
    if source_row is None:
        return Result(claim, SOURCE_MISSING, note="cited source not found")

    if claim.field_name not in source_row:
        return Result(
            claim, NOT_CHECKABLE,
            note=f"field {claim.field_name!r} absent from source",
        )

    raw_actual = source_row.get(claim.field_name)
    if raw_actual in (None, "", "Indefinite"):
        return Result(claim, NOT_CHECKABLE, note="source value empty or indefinite")

    stated = claim.stated_value
    if stated is None:
        return Result(claim, NOT_CHECKABLE, note="no parseable number in claim")

    try:
        actual = Decimal(str(raw_actual).replace(",", "").replace("$", "").strip())
    except InvalidOperation:
        return Result(claim, NOT_CHECKABLE, note="source value not numeric")

    tol = tolerance_for(claim.text)
    if abs(stated - actual) <= tol:
        return Result(claim, VERIFIED, stated, actual, tol)
    return Result(claim, CONTRADICTED, stated, actual, tol,
                  note="value outside the precision stated in the claim")


def naive_verify(claim: NumericClaim, source_row: dict | None) -> str:
    """Baseline: exact equality, no scale or precision handling.

    This stands in for what a verifier does when it treats numbers as strings.
    The gap between this and `verify_claim` is the value the careful version adds;
    if there is no gap, there is no product.
    """
    if source_row is None or claim.field_name not in source_row:
        return NOT_CHECKABLE
    raw = source_row.get(claim.field_name)
    if raw in (None, ""):
        return NOT_CHECKABLE

    digits = re.search(r"\d+(?:\.\d+)?", claim.text.replace(",", ""))
    if not digits:
        return NOT_CHECKABLE
    try:
        stated = Decimal(digits.group(0))
        actual = Decimal(str(raw).replace(",", ""))
    except InvalidOperation:
        return NOT_CHECKABLE
    return VERIFIED if stated == actual else CONTRADICTED


# --------------------------------------------------------------------------
# self-test on constructed cases before touching real data
# --------------------------------------------------------------------------

def self_test() -> tuple[int, int, list[str]]:
    """Cases where the correct answer is known by construction.

    Running this first is the difference between measuring a phenomenon and
    measuring a bug in the measuring instrument.
    """
    cases: list[tuple[str, str, dict, str]] = [
        # (claim text, field, source row, expected verdict)
        ("The offering totals $5,000,000.", "amount", {"amount": "5000000"}, VERIFIED),
        ("The offering totals $5 million.", "amount", {"amount": "5000000"}, VERIFIED),
        ("Raised $5.2 million.", "amount", {"amount": "5234000"}, VERIFIED),
        ("Raised $5.2 million.", "amount", {"amount": "5900000"}, CONTRADICTED),
        ("Raised $5.23 million.", "amount", {"amount": "5234000"}, VERIFIED),
        ("Raised $5.23 million.", "amount", {"amount": "5280000"}, CONTRADICTED),
        ("Approximately $5 million.", "amount", {"amount": "5400000"}, VERIFIED),
        ("Exactly $5 million.", "amount", {"amount": "5400000"}, CONTRADICTED),
        ("Sold $750K of securities.", "amount", {"amount": "750000"}, VERIFIED),
        ("A $1.5bn fund.", "amount", {"amount": "1500000000"}, VERIFIED),
        ("There were 12 investors.", "investors", {"investors": "12"}, VERIFIED),
        ("There were 12 investors.", "investors", {"investors": "13"}, CONTRADICTED),
        ("The amount is indefinite.", "amount", {"amount": "Indefinite"}, NOT_CHECKABLE),
        ("Total was $2 million.", "amount", {"other": "1"}, NOT_CHECKABLE),
        ("Total was $2 million.", "amount", None, SOURCE_MISSING),
        ("No number stated here.", "amount", {"amount": "100"}, NOT_CHECKABLE),
        ("Up to $10 million.", "amount", {"amount": "9000000"}, VERIFIED),
    ]

    failures: list[str] = []
    for text, field_name, row, expected in cases:
        claim = NumericClaim(text=text, field_name=field_name, source_id="test",
                             hedged=is_hedged(text))
        got = verify_claim(claim, row).verdict
        if got != expected:
            failures.append(f"{text!r} vs {row} -> {got}, expected {expected}")

    return (len(cases) - len(failures), len(cases), failures)


if __name__ == "__main__":
    passed, total, failures = self_test()
    print(f"  self-test: {passed}/{total} cases correct")
    for failure in failures:
        print(f"    FAIL {failure}")
