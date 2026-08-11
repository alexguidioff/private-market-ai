"""P0 smoke test: exact VoI oracle over synthetic worlds (standard library only)."""
from __future__ import annotations

import json
import random
from statistics import mean

SEED = 20260721
WORLDS = 500


def make_world(rng: random.Random) -> list[dict[str, float | str]]:
    return [
        {"name": f"signal_{i}", "accuracy": rng.uniform(0.52, 0.92), "cost": rng.uniform(0.01, 0.30)}
        for i in range(5)
    ]


def ndv(action: dict[str, float | str] | None) -> float:
    return 0.5 if action is None else float(action["accuracy"]) - float(action["cost"])


def select(actions: list[dict[str, float | str]], policy: str, rng: random.Random):
    if policy == "none":
        return None
    if policy == "random":
        return rng.choice(actions)
    if policy == "cheapest":
        return min(actions, key=lambda x: float(x["cost"]))
    if policy == "most_predictive":
        return max(actions, key=lambda x: float(x["accuracy"]))
    if policy == "cost_aware_oracle":
        return max([None, *actions], key=ndv)
    raise ValueError(f"Unknown policy: {policy}")


def run() -> dict[str, object]:
    rng = random.Random(SEED)
    policies = ["none", "random", "cheapest", "most_predictive", "cost_aware_oracle"]
    scores = {policy: [] for policy in policies}
    for _ in range(WORLDS):
        actions = make_world(rng)
        world_scores = {policy: ndv(select(actions, policy, rng)) for policy in policies}
        assert world_scores["cost_aware_oracle"] >= max(v for k, v in world_scores.items() if k != "cost_aware_oracle")
        for policy, value in world_scores.items():
            scores[policy].append(value)
    summary = {policy: round(mean(values), 6) for policy, values in scores.items()}
    return {"seed": SEED, "worlds": WORLDS, "metric": "expected_net_decision_value", "means": summary}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
