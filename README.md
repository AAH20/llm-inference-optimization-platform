# LLM Inference Optimization Platform

## AI Gateway, Model Routing, NVIDIA NIM, vLLM, TensorRT-LLM, Kubernetes GPU Autoscaling, Observability and AI FinOps

**TokenSRE** is an open-source, provider-neutral evaluation and control-plane foundation for production LLM inference. It determines whether an inference route satisfies quality, latency, cost, capacity, availability and data-residency requirements before producing a bounded canary recommendation and reproducible promotion receipt.

[![LLM inference optimization CI](https://github.com/AAH20/llm-inference-optimization-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AAH20/llm-inference-optimization-platform/actions/workflows/ci.yml)

> **Claim boundary:** the reference scenario is a deterministic synthetic evaluation. It does not call Azure Foundry, OpenRouter, NVIDIA NIM, vLLM, SGLang or TensorRT-LLM and does not claim physical GPU performance.

## Why production LLM inference is painful, urgent and frequent

Every AI request creates a live quality, latency, availability and margin decision. Teams routinely overpay for simple workloads, under-provision difficult workloads, react slowly to provider failures, waste GPU capacity, lose KV cache during rollouts and reduce cost at the expense of answer quality.

TokenSRE makes every routing change an evaluated, reversible experiment instead of an unmeasured configuration edit.

## Executable multi-cloud model-routing case study

The first vertical slice evaluates **45 billion monthly tokens** across classification, RAG, code and reasoning workloads. It compares four configurable contracts:

- commercial frontier API;
- Azure Foundry model router;
- self-hosted NVIDIA NIM on Kubernetes GPU infrastructure;
- self-hosted vLLM experiencing a simulated health failure.

```bash
PYTHONPATH=src python3 -m tokensre.cli \
  examples/multi-cloud-model-routing/45b-tokens.json \
  --output generated/45b-token-routing

PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The evaluator:

1. Rejects unhealthy providers.
2. Enforces workload quality thresholds.
3. Enforces p95 latency and peak-capacity targets.
4. Enforces data residency.
5. Selects the lowest-cost eligible backend.
6. Calculates token and self-hosted GPU economics.
7. Blocks autonomous production execution.
8. Emits a deterministic SHA-256 receipt.

## OpenAI-compatible AI gateway

The repository defines an OpenAI-compatible routing envelope for chat, RAG, code, reasoning, tool-calling and agent workloads. The network server, streaming lifecycle and authentication layers are roadmap work rather than completed claims.

## NVIDIA NIM, vLLM, TensorRT-LLM and SGLang

The current model includes health-aware NVIDIA NIM and vLLM backend contracts. Live adapters for NIM, vLLM, TensorRT-LLM, SGLang, NVIDIA Dynamo and Triton Inference Server will preserve engine version, model profile, GPU type and raw benchmark receipts.

## Azure AI Foundry and multi-cloud model routing

The Azure Foundry profile participates in the same production envelope as self-hosted and commercial APIs. Future adapters will add Azure Foundry, OpenRouter and direct-provider evaluation without coupling policy to a single vendor.

## Kubernetes GPU autoscaling

The included Kubernetes HPA demonstrates bounded autoscaling structure with stabilization. Its container is deliberately a CPU-only placeholder. Queue depth, tokens per second, KV-cache pressure, MIG placement and GPU telemetry adapters remain explicit roadmap items.

## LLM observability and LLMOps

Evaluation receipts capture routes, health, quality, latency, cost, capacity, residency, promotion status and evidence hashes. The Azure Bicep module creates a low-cost observability and receipt-storage plane using Log Analytics, Application Insights and private Blob Storage.

## AI FinOps and inference unit economics

The 45-billion-token scenario compares a baseline blended cost against the eligible candidate routes. It separately models eight self-hosted GPUs at `$3.50/GPU-hour`, moving from 35% to 65% useful utilization.

All figures are configurable scenario inputs—not Azure, NVIDIA or provider quotations and not guaranteed cash savings. Capacity-efficiency improvement may create deferred purchases or additional sellable capacity rather than immediate cash reduction.

## Infrastructure as Code and policy-controlled promotion

The repository includes:

- compilable Azure Bicep;
- Kubernetes autoscaling example;
- OpenAI-compatible request contract;
- deterministic promotion policy;
- GitHub Actions regression evaluation;
- generated scorecards and promotion receipts.

## Repository map

```text
src/tokensre/                         deterministic routing evaluator
examples/multi-cloud-model-routing/  45B-token synthetic workload
contracts/                            OpenAI-compatible routing schema
kubernetes/                           inference autoscaling example
infra/azure/                          observability and evidence plane
policy/                               production-promotion gates
generated/                            scorecards and receipts
docs/                                 search evidence and evaluation loop
tests/                                behavioral guarantees
```

See the [search and ATS evidence map](docs/search-and-ats-evidence.md) and [continuous evaluation loop](docs/evaluation-loop.md).

## Roadmap

- OpenAI-compatible streaming gateway
- Live Azure Foundry and OpenRouter adapters
- NVIDIA NIM, vLLM, TensorRT-LLM, SGLang and Dynamo adapters
- OpenTelemetry semantic conventions and Prometheus dashboards
- KEDA token-queue and KV-cache autoscaling
- Model-download and cache-placement optimization
- Provider outage and quota-exhaustion fault injection
- RAG, code, agent and tool-call evaluation datasets
- Multi-region, multi-cloud and sovereign failover
- Gross-margin and customer-SLA ledger

## Work with A2Z SOC

Operating or designing production GenAI? **[Request an LLM Inference Cost, Reliability and Performance Assessment](https://a2zsoc.com)** covering model routing, NVIDIA NIM/vLLM, Azure, Kubernetes GPU capacity, observability, quality evaluation and AI unit economics.
