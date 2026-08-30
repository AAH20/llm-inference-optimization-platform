from __future__ import annotations

from typing import Any


def markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['scenario']}",
        "",
        f"**Promotion:** `{report['promotion']}`",
        f"**Evidence:** `{report['evidence_level']}`",
        f"**Receipt:** `{report['receipt_sha256']}`",
        "",
        "## Model-routing decisions",
        "",
        "| Workload | Baseline | Candidate | Status | Revenue | Cost | Margin |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for route in report["routes"]:
        lines.append(f"| {route['workload']} | {route['baseline']} | {route['candidate'] or 'none'} | {route['status']} | ${route['candidate_revenue_usd']:,.2f} | ${route['candidate_cost_usd']:,.2f} | {route['contribution_margin_pct']:.2f}% |")
    lines.extend(["", "## Quality, latency and cost scorecard", ""])
    for key, value in report["scorecard"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Kubernetes GPU and AI FinOps model", ""])
    for key, value in report["gpu_finops"].items():
        lines.append(f"- `{key}`: `${value:,.2f}`")
    lines.extend(["", "## Production control", "", f"- Auto-execute: `{report['production_control']['auto_execute']}`", f"- Next step: {report['production_control']['next_step']}", "", "## Claim boundary", ""])
    for boundary in report["claim_boundary"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines) + "\n"
