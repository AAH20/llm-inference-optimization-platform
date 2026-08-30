# Continuous inference-evaluation loop

1. Capture sanitized production workload categories and SLOs.
2. Replay representative requests against baseline and candidates.
3. Score deterministic correctness, task metrics and judge-based quality separately.
4. Measure time to first token, p50, p95, p99, throughput and failures.
5. Calculate provider cost, GPU-seconds, cost per successful request and gross margin.
6. Inject provider outage, quota exhaustion, rate limiting and capacity saturation.
7. Reject any candidate outside quality, latency, residency or capacity constraints.
8. Produce a bounded canary and rollback plan.
9. Require deterministic policy and human approval.
10. Store the experiment as a regression test with an evidence hash.

Agents may propose experiments and diagnose failures. They never hold unilateral production authority.
