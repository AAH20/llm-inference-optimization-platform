from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Backend:
    name: str
    engine: str
    deployment: str
    healthy: bool
    quality: dict[str, float]
    p95_ms: dict[str, int]
    cost_per_million_tokens: float
    capacity_rps: int
    data_residency: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Backend":
        value = value.copy()
        value["data_residency"] = tuple(value["data_residency"])
        return cls(**value)


@dataclass(frozen=True)
class RouteDecision:
    workload: str
    baseline: str
    candidate: str | None
    status: str
    reason: str
    monthly_tokens: int
    monthly_requests: int
    revenue_per_request_usd: float
    candidate_cost_usd: float
    candidate_revenue_usd: float
    contribution_margin_usd: float
    contribution_margin_pct: float

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
