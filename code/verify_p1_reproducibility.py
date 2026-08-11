"""Verify that the P1 diagnostic experiments reproduce byte-identically.

The working paper states that EXP-005 through EXP-010 are deterministic given their
seeds. That was written as an assertion. This script turns it into a check: hash each
result artefact, re-run the experiment, hash again, and compare.

A mismatch is not a cosmetic problem. Every number quoted in §§4.5–4.9 and §8.6 rests
on these files, and an experiment that does not reproduce cannot support a claim in a
thesis. The recorded hashes also let a reader confirm that the artefact they are
reading is the one the paper describes.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (experiment folder, script) pairs, in dependency order.
TARGETS = [
    ("EXP-005", "exp005_why_voi_fails.py"),
    ("EXP-005-ER", "exp005_entity_resolution.py"),
    ("EXP-006", "exp006_stronger_baseline.py"),
    ("EXP-007", "exp007_topk_transfer.py"),
    ("EXP-008", "exp008_where_gain_lives.py"),
    ("EXP-009", "exp009_change_targeting.py"),
    ("EXP-010", "exp010_condition_sweep.py"),
]


def digest(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    records = []
    failures = 0

    for folder, script in TARGETS:
        artefact = ROOT / "experiments" / folder / "results.json"
        before = digest(artefact)
        if before is None:
            print(f"  {folder:<12} no results.json; skipped")
            continue

        print(f"  {folder:<12} re-running {script} ...", flush=True)
        completed = subprocess.run(
            [sys.executable, str(ROOT / "code" / script)],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        if completed.returncode != 0:
            tail = (completed.stderr or "").strip().splitlines()[-1:]
            print(f"  {folder:<12} SCRIPT FAILED  {tail}")
            failures += 1
            records.append(
                {"experiment": folder, "script": script, "status": "script_failed"}
            )
            continue

        after = digest(artefact)
        identical = before == after
        if not identical:
            failures += 1
        print(
            f"  {folder:<12} {'identical' if identical else 'DIFFERS'}  "
            f"sha256 {after[:16]}"
        )
        records.append(
            {
                "experiment": folder,
                "script": script,
                "status": "identical" if identical else "differs",
                "sha256": after,
                "sha256_before_rerun": before,
            }
        )

    manifest = {
        "checked": len(records),
        "failures": failures,
        "reproducible": failures == 0,
        "note": "sha256 of experiments/<id>/results.json after a fresh run; "
        "compared against the hash before the run",
        "results": records,
    }
    out = ROOT / "experiments" / "P1_REPRODUCIBILITY.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print()
    print(f"  checked {len(records)}, failures {failures}")
    print(f"  manifest written to {out.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
