from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import Backend, RouteDecision


def evaluate(intent: dict[str, Any]) -> dict[str, Any]:
    _validate(intent)
    backends = {item.name: item for item in map(Backend.from_dict, intent["backends"])}
    routes: list[RouteDecision] = []
    baseline_cost = 0.0
    candidate_cost = 0.0
    weighted_quality = 0.0
    weighted_latency = 0.0
    total_tokens = 0

    for workload in intent["workloads"]:
        kind = workload["name"]
        tokens = workload["monthly_tokens"]
        baseline = backends[workload["baseline_backend"]]
        baseline_cost += tokens / 1_000_000 * baseline.cost_per_million_tokens
        candidates = []
        for backend in backends.values():
            if not backend.healthy:
                continue
            if workload["residency"] not in backend.data_residency:
                continue
            if backend.quality[kind] < workload["min_quality"]:
                continue
            if backend.p95_ms[kind] > workload["max_p95_ms"]:
                continue
            if backend.capacity_rps < workload["peak_rps"]:
                continue
            candidates.append(backend)
        selected = min(candidates, key=lambda item: item.cost_per_million_tokens) if candidates else None
        if selected:
            routes.append(RouteDecision(kind, baseline.name, selected.name, "eligible", "lowest cost inside quality, latency, capacity and residency envelope", tokens))
            candidate_cost += tokens / 1_000_000 * selected.cost_per_million_tokens
            weighted_quality += selected.quality[kind] * tokens
            weighted_latency += selected.p95_ms[kind] * tokens
        else:
            routes.append(RouteDecision(kind, baseline.name, None, "blocked", "no backend satisfies the production envelope", tokens))
            candidate_cost += tokens / 1_000_000 * baseline.cost_per_million_tokens
            weighted_quality += baseline.quality[kind] * tokens
            weighted_latency += baseline.p95_ms[kind] * tokens
        total_tokens += tokens

    blocked = [route for route in routes if route.status == "blocked"]
    savings = baseline_cost - candidate_cost
    gpu = intent["self_hosted_gpu_economics"]
    gpu_monthly_cost = gpu["gpu_count"] * gpu["gpu_hour_rate_usd"] * 720
    current_useful_cost = gpu_monthly_cost / gpu["current_utilization"]
    target_useful_cost = gpu_monthly_cost / gpu["target_utilization"]
    report: dict[str, Any] = {
        "schema_version": "tokensre/v1",
        "scenario": intent["scenario"],
        "evidence_level": "synthetic-evaluation",
        "promotion": "blocked" if blocked else "eligible-for-canary",
        "routes": [route.as_dict() for route in routes],
        "scorecard": {
            "monthly_tokens": total_tokens,
            "baseline_monthly_cost_usd": round(baseline_cost, 2),
            "candidate_monthly_cost_usd": round(candidate_cost, 2),
            "modeled_monthly_savings_usd": round(savings, 2),
            "modeled_savings_pct": round(savings / baseline_cost * 100, 2),
            "candidate_weighted_quality": round(weighted_quality / total_tokens, 4),
            "candidate_weighted_p95_ms": round(weighted_latency / total_tokens, 2),
            "blocked_workloads": len(blocked),
        },
        "gpu_finops": {
            "monthly_gpu_capacity_cost_usd": round(gpu_monthly_cost, 2),
            "current_cost_per_fully_useful_capacity_unit_usd": round(current_useful_cost, 2),
            "target_cost_per_fully_useful_capacity_unit_usd": round(target_useful_cost, 2),
            "modeled_capacity_efficiency_delta_usd": round(current_useful_cost - target_useful_cost, 2),
        },
        "production_control": {
            "auto_execute": False,
            "next_step": "replay evaluation and bounded canary" if not blocked else "retain baseline and resolve blocked workloads",
            "required_gates": ["representative replay", "quality non-regression", "p95 and p99 SLO", "cost verification", "rollback", "human approval"],
        },
        "claim_boundary": [
            "No live Azure Foundry, OpenRouter, NVIDIA NIM, vLLM, SGLang or TensorRT-LLM endpoint was called",
            "No physical GPU performance is claimed",
            "Prices, quality, latency and capacity are configurable synthetic inputs",
            "Savings are modeled exposure, not guaranteed cash savings",
        ],
        "search_evidence": intent["search_evidence"],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["receipt_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def _validate(intent: dict[str, Any]) -> None:
    required = {"scenario", "backends", "workloads", "self_hosted_gpu_economics", "search_evidence"}
    missing = sorted(required - intent.keys())
    if missing:
        raise ValueError(f"missing keys: {', '.join(missing)}")
    names = [item["name"] for item in intent["backends"]]
    if len(names) != len(set(names)):
        raise ValueError("backend names must be unique")
    if not intent["workloads"]:
        raise ValueError("at least one workload is required")
    for value in intent["self_hosted_gpu_economics"].values():
        if value <= 0:
            raise ValueError("GPU economic inputs must be positive")
