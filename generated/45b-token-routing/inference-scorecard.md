# 45-billion-token multi-cloud LLM inference routing evaluation

**Promotion:** `eligible-for-canary`
**Evidence:** `synthetic-evaluation`
**Receipt:** `bf5e5bb9a5cac29768ad403b48553c736f01476defa65895a279693e4e075c4a`

## Model-routing decisions

| Workload | Baseline | Candidate | Status | Revenue | Cost | Margin |
|---|---|---|---|---:|---:|---:|
| classification | frontier-api | self-hosted-nim | eligible | $2,160,000.00 | $37,800.00 | 98.25% |
| rag | frontier-api | self-hosted-nim | eligible | $1,400,000.00 | $25,200.00 | 98.20% |
| code | frontier-api | azure-foundry-router | eligible | $1,350,000.00 | $32,400.00 | 97.60% |
| reasoning | frontier-api | frontier-api | eligible | $1,100,000.00 | $31,200.00 | 97.16% |

## Quality, latency and cost scorecard

- `monthly_tokens`: `45000000000`
- `monthly_requests`: `240000000`
- `modeled_monthly_revenue_usd`: `6010000.0`
- `baseline_monthly_cost_usd`: `234000.0`
- `candidate_monthly_cost_usd`: `126600.0`
- `modeled_monthly_savings_usd`: `107400.0`
- `modeled_savings_pct`: `45.9`
- `baseline_contribution_margin_usd`: `5776000.0`
- `candidate_contribution_margin_usd`: `5883400.0`
- `candidate_contribution_margin_pct`: `97.89`
- `modeled_margin_improvement_usd`: `107400.0`
- `candidate_weighted_quality`: `0.9313`
- `candidate_weighted_p95_ms`: `1505.33`
- `blocked_workloads`: `0`

## Kubernetes GPU and AI FinOps model

- `monthly_gpu_capacity_cost_usd`: `$20,160.00`
- `current_cost_per_fully_useful_capacity_unit_usd`: `$57,600.00`
- `target_cost_per_fully_useful_capacity_unit_usd`: `$31,015.38`
- `modeled_capacity_efficiency_delta_usd`: `$26,584.62`

## Production control

- Auto-execute: `False`
- Next step: replay evaluation and bounded canary

## Claim boundary

- No live Azure Foundry, OpenRouter, NVIDIA NIM, vLLM, SGLang or TensorRT-LLM endpoint was called
- No physical GPU performance is claimed
- Prices, quality, latency and capacity are configurable synthetic inputs
- Savings are modeled exposure, not guaranteed cash savings
