"""EXP-004 — Attribution on real prose documents, not structured fields.

Why this experiment was rebuilt
-------------------------------
The first attempt pointed at Form D `primary_doc.xml`, which turned out to *be*
the structured source: a few hundred words of addresses and one or two figures.
It reported one number per document and 0% attribution, which measured a mistake
in the experiment rather than a property of the world. Testing the easy case
twice is the failure mode this whole log exists to prevent.

The corpus that matters is prose with tables: annual reports, where a figure is
surrounded by dozens of similar figures, denominated in thousands, restated in a
summary, and repeated across periods. That is where a citation either resolves to
one place or does not.

What is measured
----------------
Given a figure that genuinely appears in a filing, can the deterministic route
attribute it to a *unique* location?

* **found_unique** — one occurrence at the stated precision. Attribution decided.
* **found_ambiguous** — several distinct occurrences match, so the number being
  present proves nothing about where it came from. This is exactly the case a
  "does the document contain this number?" check silently passes, and exactly
  what attribution hallucination exploits.
* **not_found** — absent at the stated precision.

The interesting quantity is the ambiguous share. If it is large, then locating a
number is not the same as verifying attribution, and the strong EXP-003 result
does not carry over to real documents. Declared before running: unique
attribution below 40% kills the deterministic-only version of the idea.

Also measured: how much the *scale-and-units* handling matters, by comparing
against a checker that matches raw digit strings. Filings denominate tables in
thousands, so a digit-string matcher should fail often — and if it does not, the
careful handling is unnecessary.

Read-only public EDGAR, throttled per SEC guidance.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from claim_verify import parse_money, tolerance_for  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "EXP-004"
CACHE = ROOT / "datasets" / ".cache_docs"
USER_AGENT = "Private-Market-AI academic research alexguidioff@gmail.com"
THROTTLE = 0.2

CONTEXT_WINDOW = 120
MIN_DOC_CHARS = 40_000  # below this it is not a prose filing


def fetch(url: str) -> str | None:
    """GET a public SEC document, cached on disk."""
    if not url.startswith("https://www.sec.gov/") and not url.startswith(
        "https://data.sec.gov/"
    ):
        raise ValueError(f"refusing non-SEC URL: {url}")

    CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^A-Za-z0-9._-]", "_", url)[-140:]
    cached = CACHE / f"{key}.txt"
    if cached.exists():
        return cached.read_text(encoding="utf-8", errors="replace")

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                body = response.read().decode("utf-8", errors="replace")
            time.sleep(THROTTLE)
            cached.write_text(body, encoding="utf-8")
            return body
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429, 503) and attempt < 2:
                time.sleep(2 ** attempt + 1)
                continue
            print(f"    fetch failed {exc}")
            return None
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < 2:
                time.sleep(2 ** attempt + 1)
                continue
            print(f"    fetch failed {exc}")
            return None
    return None


def strip_markup(html: str) -> str:
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    for entity, replacement in (
        ("&nbsp;", " "), ("&#160;", " "), ("&amp;", "&"),
        ("&lt;", "<"), ("&gt;", ">"), ("&#8217;", "'"), ("&#8212;", "-"),
    ):
        text = text.replace(entity, replacement)
    return re.sub(r"\s+", " ", text)


# --------------------------------------------------------------------------
# unit detection: filings state their denomination in the table header
# --------------------------------------------------------------------------

UNIT_PATTERNS = (
    (re.compile(r"in thousands", re.IGNORECASE), Decimal(1_000)),
    (re.compile(r"\(in 000s?\)", re.IGNORECASE), Decimal(1_000)),
    (re.compile(r"in millions", re.IGNORECASE), Decimal(1_000_000)),
    (re.compile(r"in billions", re.IGNORECASE), Decimal(1_000_000_000)),
)


def unit_multiplier_near(text: str, position: int, back: int = 3000) -> Decimal:
    """Denomination declared closest before a position.

    Financial tables say "(in thousands)" once in a header and then print 5,234
    meaning 5,234,000. Ignoring this makes every table figure look wrong by three
    orders of magnitude, which is the single largest source of error here.
    """
    window = text[max(0, position - back):position]
    best_multiplier = Decimal(1)
    best_at = -1
    for pattern, multiplier in UNIT_PATTERNS:
        for match in pattern.finditer(window):
            if match.start() > best_at:
                best_at = match.start()
                best_multiplier = multiplier
    return best_multiplier


@dataclass
class Occurrence:
    value: Decimal
    position: int
    context: str
    multiplier: Decimal

    @property
    def context_words(self) -> set[str]:
        return {
            w.lower().strip(".,:;()$%")
            for w in self.context.split()
            if len(w) > 3 and not w[0].isdigit()
        }


NUMBER_PATTERN = re.compile(
    r"\(?\$?\s?\d{1,3}(?:,\d{3})+(?:\.\d+)?\)?"
    r"|\$\s?\d+(?:\.\d+)?\s?(?:million|billion|thousand)\b"
    r"|\b\d+(?:\.\d+)?\s?(?:million|billion)\b",
    re.IGNORECASE,
)


def extract_occurrences(text: str, limit: int = 20_000) -> list[Occurrence]:
    """Every numeric value in the document, scaled by its declared denomination."""
    found: list[Occurrence] = []
    for match in NUMBER_PATTERN.finditer(text):
        if len(found) >= limit:
            break
        token = match.group(0)
        parsed = parse_money(token)
        if parsed is None:
            continue
        value, _, explicit_scale = parsed
        if value == 0:
            continue

        # A figure written with its own scale word ("$5.2 million") is already in
        # base units; only bare table numbers inherit the header denomination.
        multiplier = (
            Decimal(1) if explicit_scale > 1
            else unit_multiplier_near(text, match.start())
        )

        start = max(0, match.start() - CONTEXT_WINDOW)
        end = min(len(text), match.end() + CONTEXT_WINDOW)
        found.append(Occurrence(
            value * multiplier, match.start(), text[start:end], multiplier
        ))
    return found


def locate(
    stated: Decimal, text_written: str, occurrences: list[Occurrence]
) -> tuple[str, int]:
    """Attribute a stated figure to a unique location, or report why not."""
    tol = tolerance_for(text_written)
    matches = [o for o in occurrences if abs(o.value - stated) <= tol]

    if not matches:
        return ("not_found", 0)

    distinct: list[Occurrence] = []
    for candidate in matches:
        # The same fact restated in a summary shares much of its wording; a
        # genuinely different line item does not.
        if not any(
            len(candidate.context_words & kept.context_words) >= 6
            for kept in distinct
        ):
            distinct.append(candidate)

    if len(distinct) == 1:
        return ("found_unique", len(matches))
    return ("found_ambiguous", len(distinct))


def locate_digits_only(stated: Decimal, occurrences_raw: list[Decimal]) -> str:
    """Baseline ignoring scale and units: match the digit string as printed."""
    target = f"{stated:.0f}"
    hits = sum(1 for v in occurrences_raw if f"{v:.0f}" == target)
    if hits == 0:
        return "not_found"
    return "found_unique" if hits == 1 else "found_ambiguous"


# --------------------------------------------------------------------------
# corpus: recent annual reports
# --------------------------------------------------------------------------

def find_annual_reports(limit: int = 12) -> list[tuple[str, str]]:
    """Locate recent 10-K primary documents via EDGAR full-text search."""
    url = (
        "https://www.sec.gov/cgi-bin/srqsb?text=form-type%3D10-K"  # legacy, unused
    )
    # The reliable public route is the daily index of filings by form type.
    out: list[tuple[str, str]] = []
    listing = fetch(
        "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=10-K"
        "&dateb=&owner=include&count=40&output=atom"
    )
    if listing:
        for match in re.finditer(r"<link[^>]+href=\"([^\"]+)\"", listing):
            href = match.group(1)
            if "Archives" in href:
                out.append((href, "10-K"))
            if len(out) >= limit:
                break
    return out


def documents_from_full_text_search(query: str, limit: int) -> list[str]:
    """Use EDGAR full-text search to find annual report documents."""
    api = (
        "https://efts.sec.gov/LATEST/search-index?q=" + query
    )
    # efts search endpoint returns JSON; use the documented public path.
    body = fetch_json(
        f"https://efts.sec.gov/LATEST/search-index?q={query}&forms=10-K"
    )
    return []


def fetch_json(url: str) -> dict | None:
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            import json as _json

            return _json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:  # noqa: BLE001
        return None


def annual_report_urls(limit: int = 10) -> list[str]:
    """Recent 10-K documents, resolved through the company submissions API.

    Uses well-known large filers so the corpus is reproducible and the documents
    are guaranteed to contain prose and financial tables.
    """
    ciks = {
        "AAPL": "0000320193",
        "MSFT": "0000789019",
        "AMZN": "0001018724",
        "GOOGL": "0001652044",
        "NVDA": "0001045810",
        "META": "0001326801",
        "TSLA": "0001318605",
        "NFLX": "0001065280",
        "ADBE": "0000796343",
        "CRM": "0001108524",
        "ORCL": "0001341439",
        "INTC": "0000050863",
    }

    urls: list[str] = []
    for ticker, cik in list(ciks.items())[:limit]:
        payload = fetch_json(f"https://data.sec.gov/submissions/CIK{cik}.json")
        if not payload:
            continue
        recent = payload.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        accessions = recent.get("accessionNumber", [])
        docs = recent.get("primaryDocument", [])

        for form, accession, doc in zip(forms, accessions, docs):
            if form != "10-K" or not doc:
                continue
            clean = accession.replace("-", "")
            urls.append(
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{clean}/{doc}"
            )
            break
        time.sleep(THROTTLE)
    return urls


# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------

def sample_claims_from_document(
    occurrences: list[Occurrence], rng, n: int = 25
) -> list[tuple[Decimal, str, Occurrence]]:
    """Pick figures a memo would quote, and write them as a memo would.

    Sampling from the document guarantees the figure is genuinely present, so
    `not_found` can only mean the matcher failed — which is what needs measuring.
    """
    material = [o for o in occurrences if o.value >= 1_000_000]
    if not material:
        return []

    rng.shuffle(material)
    out = []
    for occurrence in material[:n]:
        value = occurrence.value
        if value >= 1_000_000_000:
            written = f"${value / Decimal(1_000_000_000):.1f} billion"
        else:
            written = f"${value / Decimal(1_000_000):.1f} million"
        out.append((value, written, occurrence))
    return out


def run(limit: int = 10) -> dict:
    import random

    rng = random.Random(20260728)

    urls = annual_report_urls(limit)
    print(f"  resolved {len(urls)} annual report URLs")

    verdicts = Counter()
    digits_verdicts = Counter()
    ambiguity_degrees: list[int] = []
    numbers_per_doc: list[int] = []
    docs_used = 0
    unit_scaled_share: list[float] = []

    for i, url in enumerate(urls, start=1):
        body = fetch(url)
        if not body or len(body) < MIN_DOC_CHARS:
            print(f"    [{i}] skipped (too small or unavailable)")
            continue
        text = strip_markup(body)
        occurrences = extract_occurrences(text)
        if len(occurrences) < 50:
            print(f"    [{i}] skipped ({len(occurrences)} numbers found)")
            continue

        docs_used += 1
        numbers_per_doc.append(len(occurrences))
        scaled = sum(1 for o in occurrences if o.multiplier > 1)
        unit_scaled_share.append(scaled / len(occurrences))

        raw_values = [
            o.value / o.multiplier if o.multiplier > 1 else o.value
            for o in occurrences
        ]

        for stated, written, _ in sample_claims_from_document(occurrences, rng):
            verdict, degree = locate(stated, written, occurrences)
            verdicts[verdict] += 1
            if verdict == "found_ambiguous":
                ambiguity_degrees.append(degree)
            digits_verdicts[locate_digits_only(stated, raw_values)] += 1

        print(
            f"    [{i}] {url.rsplit('/', 1)[-1][:40]:<42} "
            f"numbers={len(occurrences):<6} verdicts={dict(verdicts)}",
            flush=True,
        )

    total = sum(verdicts.values())
    return {
        "documents_used": docs_used,
        "claims_attempted": total,
        "mean_numbers_per_document": (
            sum(numbers_per_doc) / len(numbers_per_doc) if numbers_per_doc else 0
        ),
        "mean_share_needing_unit_scaling": (
            sum(unit_scaled_share) / len(unit_scaled_share) if unit_scaled_share else 0
        ),
        "verdicts": dict(verdicts),
        "digits_only_verdicts": dict(digits_verdicts),
        "unique_share": verdicts["found_unique"] / total if total else 0.0,
        "ambiguous_share": verdicts["found_ambiguous"] / total if total else 0.0,
        "not_found_share": verdicts["not_found"] / total if total else 0.0,
        "digits_only_unique_share": (
            digits_verdicts["found_unique"] / total if total else 0.0
        ),
        "mean_ambiguity_degree": (
            sum(ambiguity_degrees) / len(ambiguity_degrees) if ambiguity_degrees else 0
        ),
    }


def report(results: dict) -> str:
    total = results["claims_attempted"]
    if not total:
        return "  no claims evaluated; corpus unavailable"

    lines = [
        "",
        "  EXP-004 — attribution on real annual reports (prose + tables)",
        "  " + "=" * 68,
        f"  documents used: {results['documents_used']}",
        f"  mean numbers per document: {results['mean_numbers_per_document']:.0f}",
        f"  share of figures inheriting a table denomination: "
        f"{results['mean_share_needing_unit_scaling']:.1%}",
        f"  claims attempted: {total}",
        "",
        "  scale-aware attribution:",
        f"    uniquely attributable   {results['unique_share']:.1%}",
        f"    ambiguous               {results['ambiguous_share']:.1%}",
        f"    not found               {results['not_found_share']:.1%}",
        "",
        "  digit-string baseline (ignores scale and units):",
        f"    uniquely attributable   {results['digits_only_unique_share']:.1%}",
        f"    verdicts {results['digits_only_verdicts']}",
    ]
    if results.get("mean_ambiguity_degree"):
        lines.append(
            f"\n  when ambiguous, mean distinct candidate locations: "
            f"{results['mean_ambiguity_degree']:.1f}"
        )

    ok = results["unique_share"] >= 0.40
    lines += [
        "",
        "  " + "-" * 68,
        f"  unique attribution >= 40%: {'PASS' if ok else 'FAIL'}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    results = run(n)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(report(results))
