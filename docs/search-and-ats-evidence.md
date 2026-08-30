# Search-volume and ATS evidence map

Exact Google or LinkedIn search-volume figures require proprietary keyword/recruitment datasets and are not claimed. The public surface prioritizes broadly searched category language, current platform terminology and recurring senior-role vocabulary. Every term maps to implementation or an explicit boundary so SEO never outruns engineering evidence.

| Search or hiring term | Repository evidence | Claim status |
|---|---|---|
| LLM inference | Workload evaluation and backend profiles | Implemented simulation |
| AI gateway / OpenAI-compatible API | `/v1/route` decision API and request contract | Decision API implemented; streaming proxy not claimed |
| model routing | Quality, latency, cost, capacity and residency selector | Implemented |
| inference optimization | Baseline/candidate scorecard | Implemented |
| NVIDIA NIM | Self-hosted NIM backend contract | Synthetic profile; no endpoint called |
| vLLM | Health-aware vLLM backend contract | Synthetic profile; no endpoint called |
| TensorRT-LLM / SGLang / NVIDIA Dynamo | Adapter roadmap | Not implemented |
| Azure AI Foundry | Foundry router contract and Azure evidence plane | Synthetic profile; no model deployed |
| OpenRouter | Provider-adapter roadmap | Not implemented |
| Kubernetes / GPU autoscaling | Deployment, probes, security context and HPA example | Control plane deployable; GPU metrics remain synthetic |
| AI observability / LLM observability | Evaluation receipts and Azure monitoring IaC | Baseline implemented |
| LLMOps | CI evaluation and controlled promotion | Implemented baseline |
| AI FinOps / cost per token / unit economics | Per-workload revenue, inference cost and contribution margin | Implemented with modeled inputs |
| multi-cloud AI | Provider-neutral backend abstraction | Implemented contract |
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
