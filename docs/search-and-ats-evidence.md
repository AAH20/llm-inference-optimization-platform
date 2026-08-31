# Search-volume and ATS evidence map

Exact Google or LinkedIn search-volume figures require proprietary keyword/recruitment datasets and are not claimed. The public surface prioritizes broadly searched category language, current platform terminology and recurring senior-role vocabulary. Every term maps to implementation or an explicit boundary so SEO never outruns engineering evidence.

| Search or hiring term | Repository evidence | Claim status |
|---|---|---|
| AI infrastructure / Generative AI | Production gateway, Kubernetes runtime and Azure deployment plane | Implemented reference platform |
| LLM inference | Workload evaluation, live upstream adapters and backend profiles | Implemented; benchmark inputs remain synthetic |
| AI gateway / OpenAI-compatible API | Authenticated `/v1/chat/completions`, SSE streaming and `/v1/route` | Implemented |
| model routing | Quality, latency, cost, capacity and residency selector | Implemented |
| inference optimization | Baseline/candidate scorecard | Implemented |
| NVIDIA NIM | Self-hosted NIM backend contract | Synthetic profile; no endpoint called |
| vLLM | Health-aware vLLM backend contract | Synthetic profile; no endpoint called |
| TensorRT-LLM / SGLang / NVIDIA Dynamo | Adapter roadmap | Not implemented |
| Azure OpenAI / Azure AI Foundry | OpenAI-compatible adapter contract and Azure evidence plane | Adapter implemented; no model deployed by this repository |
| OpenRouter | OpenAI-compatible adapter | Implemented; requires customer credentials |
| Kubernetes / AKS / GPU autoscaling | HA deployment, probes, PDB, topology spread, security context and HPA | Gateway deployable; physical GPU results not claimed |
| AI observability / OpenTelemetry | Prometheus request, latency and failover telemetry plus Azure monitoring IaC | Implemented baseline |
| LLMOps | CI evaluation and controlled promotion | Implemented baseline |
| AI FinOps / cost per token / unit economics | Per-workload revenue, inference cost and contribution margin | Implemented with modeled inputs |
| multi-cloud AI / hybrid cloud | Provider-neutral live upstream abstraction | Implemented |
| sovereign AI / on-prem LLM | Residency-aware routing | Implemented contract |

## Current terminology sources

- NVIDIA describes Dynamo as an open-source inference framework spanning vLLM, SGLang and TensorRT-LLM, with Kubernetes deployment, KV-aware routing, cache management and autoscaling: <https://docs.nvidia.com/dynamo/dev>
- NVIDIA's NIM Operator documentation recommends inference-specific rather than CPU/memory metrics for autoscaling: <https://docs.nvidia.com/nim/large-language-models/latest/deployment/kubernetes-deployment/nim-operator-deployment.html>
- Microsoft Foundry documents model/agent tracing, evaluation, OpenTelemetry and production monitoring: <https://learn.microsoft.com/azure/ai-foundry/concepts/observability>
- The FinOps Foundation identifies workload optimization, AI cost management and unit economics as active practice priorities: <https://data.finops.org/2025-report/>

Validated on 2026-08-31. These sources establish terminology and market relevance, not numerical search volume.

## Target international roles

- Principal AI Platform Architect
- Senior Inference Infrastructure Engineer
- NVIDIA NIM Platform Engineer
- AI Infrastructure SRE
- GPU Cloud Infrastructure Engineer
- Distributed Systems Engineer
- Forward-Deployed AI Engineer
- Generative AI Solutions Architect
- Kubernetes GPU Platform Engineer
- Multi-Cloud AI Architect
