"""Tail-lift analysis: measuring information value where only the extreme matters.

Motivation
----------
EXP-001B/C/D evaluated information blocks with average metrics: ROC-AUC, log
loss, mean utility. Those are the right tools when every case matters equally.
They are the wrong tools when the decision only concerns the extreme.

An analyst screening a pipeline does not act on the median company. They act on
the top slice they have capacity to examine. A feature that separates the top 5%
sharply but carries no information through the bulk will show an unremarkable
AUC, because AUC averages over all pairs and the bulk supplies most of them.

This module measures the quantity the decision actually depends on:

    lift(q) = P(outcome = 1 | feature in top q) / P(outcome = 1)

Under independence lift(q) = 1 at every q. A feature with lift(0.05) = 2.0 is
twice as likely to be followed by the outcome in its extreme slice, whatever its
AUC says.

Relation to P1
--------------
This does not contradict EXP-001C, it complements it. EXP-001C rejected *paying*
selectively for issuer history: as a discretionary acquisition action, the block
did not clear its cost in any declared scenario. The present analysis asks a
different question: how much does that block contribute *when already present in
the baseline state*. §8.2 of the working paper draws exactly this distinction
between baseline information and acquisition actions; tail lift quantifies the
former.

Honest limits
-------------
* **Tails are data-poor by construction.** At q = 0.05 with n = 4,618 the
  estimate rests on ~230 observations. Intervals are reported, never suppressed.
* **Scanning invites false discovery.** Testing many features at many thresholds
  guarantees that the luckiest combination looks significant, so Benjamini-
  Hochberg control is applied across the whole scan.
* **The outcome remains the weak SEC proxy.** A subsequent non-amendment Form D
  notice is a regulatory event, not a priced round, not Series A, not success.
* **Association, not causation.** Nothing here identifies a causal effect.

Standard library only, matching the rest of the P1 pipeline.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Sequence

DEFAULT_QUANTILES = (0.30, 0.20, 0.10, 0.05)
DEFAULT_BOOTSTRAP = 1000
DEFAULT_SEED = 20260728


# --- average-metric reference, for the contrast ------------------------------


def average_ranks(values: Sequence[float]) -> list[float]:
    """Ranks 1..n with tied values sharing their mean rank."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        mean_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = mean_rank
        i = j + 1
    return ranks


def auc_roc(scores: Sequence[float], labels: Sequence[int]) -> float | None:
    """ROC-AUC via the rank-sum identity, with correct handling of ties.

    Included so every report can show the average metric next to the tail
    metric: the gap between them is the point of the analysis.
    """
    if len(scores) != len(labels) or not scores:
        return None
    n_pos = sum(1 for y in labels if y == 1)
    n_neg = len(labels) - n_pos
    if n_pos == 0 or n_neg == 0:
        return None
    ranks = average_ranks(scores)
    rank_sum_pos = sum(r for r, y in zip(ranks, labels) if y == 1)
    u = rank_sum_pos - n_pos * (n_pos + 1) / 2.0
    return u / (n_pos * n_neg)


# --- tail lift ----------------------------------------------------------------


@dataclass
class TailLift:
    """Lift of one feature at one threshold, with uncertainty."""

    feature: str
    q: float
    n: int
    n_extreme: int
    base_rate: float
    rate_in_tail: float | None
    lift: float | None
    lift_ci: tuple[float, float] | None
    p_value: float | None

    @property
    def significant(self) -> bool:
        """Whether the interval on the lift excludes 1.0 and the test rejects."""
        if self.lift_ci is None or self.p_value is None:
            return False
        return self.lift_ci[0] > 1.0 and self.p_value < 0.05

    def as_dict(self) -> dict:
        return {
            "feature": self.feature,
            "q": self.q,
            "n": self.n,
            "n_extreme": self.n_extreme,
            "base_rate": round(self.base_rate, 4),
            "rate_in_tail": round(self.rate_in_tail, 4) if self.rate_in_tail else None,
            "lift": round(self.lift, 3) if self.lift else None,
            "lift_ci": [round(v, 3) for v in self.lift_ci] if self.lift_ci else None,
            "p_value": round(self.p_value, 4) if self.p_value is not None else None,
            "significant": self.significant,
        }

    def line(self) -> str:
        if self.lift is None:
            return f"    q={self.q:<5.2f}  insufficient data in tail"
        ci = self.lift_ci or (float("nan"), float("nan"))
        mark = " *" if self.significant else ""
        return (
            f"    q={self.q:<5.2f}  n_ext={self.n_extreme:<5} "
            f"rate={self.rate_in_tail:.3f}  lift={self.lift:.2f}x "
            f"[{ci[0]:.2f}, {ci[1]:.2f}]  p={self.p_value:.4f}{mark}"
        )


def _extreme_indices(values: Sequence[float], q: float, upper: bool) -> list[int]:
    """Indices of the extreme q share, by rank rather than by value.

    Rank-based selection keeps the slice size stable even when the feature is
    heavily skewed or has mass points, which financial count variables usually do.
    """
    n = len(values)
    if n == 0:
        return []
    k = max(1, int(round(q * n)))
    order = sorted(range(n), key=lambda i: values[i], reverse=upper)
    return order[:k]


def tail_rate(
    feature: Sequence[float], outcome: Sequence[int], q: float, upper: bool = True
) -> tuple[float | None, int]:
    """Outcome rate inside the extreme q share of the feature."""
    if len(feature) != len(outcome) or not feature:
        return (None, 0)
    idx = _extreme_indices(feature, q, upper)
    if len(idx) < 20:
        return (None, len(idx))
    return (sum(outcome[i] for i in idx) / len(idx), len(idx))


def tail_lift(
    feature: Sequence[float],
    outcome: Sequence[int],
    q: float,
    name: str = "feature",
    upper: bool = True,
    n_boot: int = DEFAULT_BOOTSTRAP,
    seed: int = DEFAULT_SEED,
    alpha: float = 0.05,
) -> TailLift:
    """Lift in the extreme q share, with bootstrap interval and permutation test.

    The p-value comes from permuting the outcome while holding the feature fixed,
    which gives the null distribution without assuming a functional form.
    """
    n = len(feature)
    base = sum(outcome) / n if n else 0.0
    rate, n_ext = tail_rate(feature, outcome, q, upper)

    if rate is None or base == 0.0:
        return TailLift(name, q, n, n_ext, base, None, None, None, None)

    point = rate / base

    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        f = [feature[i] for i in idx]
        y = [outcome[i] for i in idx]
        b = sum(y) / n
        r, _ = tail_rate(f, y, q, upper)
        if r is not None and b > 0:
            draws.append(r / b)

    ci: tuple[float, float] | None = None
    if draws:
        draws.sort()
        lo = draws[max(0, int((alpha / 2) * len(draws)) - 1)]
        hi = draws[min(len(draws) - 1, int((1 - alpha / 2) * len(draws)))]
        ci = (lo, hi)

    perm_rng = random.Random(seed + 1)
    labels = list(outcome)
    null: list[float] = []
    for _ in range(n_boot):
        perm_rng.shuffle(labels)
        r, _ = tail_rate(feature, labels, q, upper)
        if r is not None:
            null.append(r / base)

    p_value = None
    if null:
        p_value = (sum(1 for v in null if v >= point) + 1) / (len(null) + 1)

    return TailLift(name, q, n, n_ext, base, rate, point, ci, p_value)


@dataclass
class FeatureProfile:
    """A feature's behaviour from bulk to extreme, next to its average metric."""

    feature: str
    auc: float | None
    base_rate: float
    lifts: list[TailLift]

    @property
    def best(self) -> TailLift | None:
        usable = [x for x in self.lifts if x.lift is not None]
        return max(usable, key=lambda x: x.lift or 0.0) if usable else None

    @property
    def monotone_in_tail(self) -> bool:
        """Whether lift increases as the slice narrows.

        Monotonicity is the credible pattern: a genuine tail effect should
        strengthen as the threshold tightens. A single significant threshold with
        no trend is more likely to be a lucky slice.
        """
        values = [x.lift for x in self.lifts if x.lift is not None]
        if len(values) < 3:
            return False
        return all(a <= b + 1e-9 for a, b in zip(values, values[1:]))

    @property
    def tail_only(self) -> bool:
        """Weak on average, strong at the extreme: the case average metrics hide."""
        if self.auc is None or self.best is None or self.best.lift is None:
            return False
        return abs(self.auc - 0.5) < 0.10 and self.best.lift >= 1.25 and self.best.significant

    def report(self) -> str:
        auc = f"{self.auc:.3f}" if self.auc is not None else "n/a"
        lines = [f"  {self.feature}   (AUC {auc}, base rate {self.base_rate:.1%})"]
        lines += [x.line() for x in self.lifts]
        flags = []
        if self.monotone_in_tail:
            flags.append("monotone lift")
        if self.tail_only:
            flags.append("TAIL-ONLY signal")
        if flags:
            lines.append("    -> " + ", ".join(flags))
        return "\n".join(lines)

    def as_dict(self) -> dict:
        return {
            "feature": self.feature,
            "auc": round(self.auc, 4) if self.auc is not None else None,
            "base_rate": round(self.base_rate, 4),
            "monotone_in_tail": self.monotone_in_tail,
            "tail_only": self.tail_only,
            "lifts": [x.as_dict() for x in self.lifts],
        }


def profile(
    name: str,
    feature: Sequence[float],
    outcome: Sequence[int],
    quantiles: Sequence[float] = DEFAULT_QUANTILES,
    upper: bool = True,
    n_boot: int = DEFAULT_BOOTSTRAP,
    seed: int = DEFAULT_SEED,
) -> FeatureProfile:
    """Profile one feature across thresholds."""
    lifts = [
        tail_lift(feature, outcome, q, name, upper, n_boot, seed) for q in quantiles
    ]
    base = sum(outcome) / len(outcome) if outcome else 0.0
    return FeatureProfile(name, auc_roc(list(feature), list(outcome)), base, lifts)


def benjamini_hochberg(p_values: Sequence[float], alpha: float = 0.05) -> list[bool]:
    """Step-up FDR control.

    Mandatory here: a scan over features times thresholds will always produce an
    apparently significant cell by chance alone.
    """
    n = len(p_values)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: p_values[i])
    max_k = 0
    for k, idx in enumerate(order, start=1):
        if p_values[idx] <= (k / n) * alpha:
            max_k = k
    rejected = [False] * n
    for k, idx in enumerate(order, start=1):
        if k <= max_k:
            rejected[idx] = True
    return rejected


def screen(
    features: dict[str, Sequence[float]],
    outcome: Sequence[int],
    quantiles: Sequence[float] = DEFAULT_QUANTILES,
    n_boot: int = 500,
    alpha: float = 0.05,
    seed: int = DEFAULT_SEED,
) -> tuple[list[FeatureProfile], dict]:
    """Screen features for tail lift, with FDR control across the whole scan."""
    profiles = [
        profile(name, values, outcome, quantiles, n_boot=n_boot, seed=seed)
        for name, values in features.items()
    ]

    p_values: list[float] = []
    coords: list[tuple[int, int]] = []
    for pi, prof in enumerate(profiles):
        for li, lift in enumerate(prof.lifts):
            if lift.p_value is not None:
                p_values.append(lift.p_value)
                coords.append((pi, li))

    keep = benjamini_hochberg(p_values, alpha)
    survivors = sorted({profiles[coords[i][0]].feature for i, k in enumerate(keep) if k})

    summary = {
        "n": len(outcome),
        "base_rate": round(sum(outcome) / len(outcome), 4) if outcome else None,
        "n_tests": len(p_values),
        "fdr_alpha": alpha,
        "bootstrap": n_boot,
        "seed": seed,
        "quantiles": list(quantiles),
        "survivors_fdr": survivors,
        "tail_only": [p.feature for p in profiles if p.tail_only],
        "monotone": [p.feature for p in profiles if p.monotone_in_tail],
    }
    return profiles, summary


def transport_check(
    features: dict[str, tuple[Sequence[float], Sequence[float]]],
    outcome_dev: Sequence[int],
    outcome_test: Sequence[int],
    q: float = 0.05,
    n_boot: int = 500,
    seed: int = DEFAULT_SEED,
) -> list[dict]:
    """Does the lift found on development transport to a disjoint test cohort?

    This is the only result worth reporting. A lift measured on the cohort used to
    find it is a description; a lift that survives on a company-disjoint later
    cohort is evidence.
    """
    rows: list[dict] = []
    for name, (dev_values, test_values) in features.items():
        dev = tail_lift(dev_values, outcome_dev, q, name, n_boot=n_boot, seed=seed)
        test = tail_lift(test_values, outcome_test, q, name, n_boot=n_boot, seed=seed)
        rows.append(
            {
                "feature": name,
                "q": q,
                "dev_lift": round(dev.lift, 3) if dev.lift else None,
                "test_lift": round(test.lift, 3) if test.lift else None,
                "test_ci": [round(v, 3) for v in test.lift_ci] if test.lift_ci else None,
                "test_p": round(test.p_value, 4) if test.p_value is not None else None,
                "transports": bool(
                    test.significant and test.lift and dev.lift and test.lift > 1.2
                ),
            }
        )
    return sorted(rows, key=lambda r: -(r["test_lift"] or 0))
