# 45-billion-token multi-cloud LLM inference routing evaluation

**Promotion:** `eligible-for-canary`
**Evidence:** `synthetic-evaluation`
**Receipt:** `36ecb87b3e63cfde990e3988078b14b117cddf253f4ffe25efad8b9ba601b442`

## Model-routing decisions

| Workload | Baseline | Candidate | Status | Reason |
|---|---|---|---|---|
| classification | frontier-api | self-hosted-nim | eligible | lowest cost inside quality, latency, capacity and residency envelope |
| rag | frontier-api | self-hosted-nim | eligible | lowest cost inside quality, latency, capacity and residency envelope |
| code | frontier-api | azure-foundry-router | eligible | lowest cost inside quality, latency, capacity and residency envelope |
| reasoning | frontier-api | frontier-api | eligible | lowest cost inside quality, latency, capacity and residency envelope |

## Quality, latency and cost scorecard

- `monthly_tokens`: `45000000000`
- `baseline_monthly_cost_usd`: `234000.0`
- `candidate_monthly_cost_usd`: `126600.0`
- `modeled_monthly_savings_usd`: `107400.0`
- `modeled_savings_pct`: `45.9`
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
