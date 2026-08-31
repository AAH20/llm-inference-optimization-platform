# Production acceptance, not a marketing label

TokenSRE contains a production-oriented gateway and deployment contracts. A specific installation becomes production-ready only after the operator supplies and verifies its own upstreams, identity, networking, capacity and incident response.

## Mandatory release gates

- Replace synthetic quality, latency, capacity and price inputs with signed replay, load-test and billing evidence.
- Store gateway and provider credentials in Azure Key Vault or another external secret manager; never commit `.env` values.
- Terminate TLS at a controlled ingress or API gateway and replace the reference bearer token with enterprise workload identity where required.
- Pin the container by digest, generate an SBOM, sign it and verify the signature at admission.
- Exercise streaming and buffered traffic under representative concurrency.
- Prove rate-limit, timeout, 5xx, quota-exhaustion and total-provider-outage failover.
- Validate multi-zone disruption, rollback and disaster recovery against documented RTO/RPO.
- Connect Prometheus/OpenTelemetry to owned alerts and an on-call rotation.
- Review residency, content logging and retention for every workload jurisdiction.
- Run canary promotion with a human approval boundary and a tested rollback.

The CI build, unit tests, Bicep compilation and Kubernetes schema parsing prove repository integrity. They do not replace workload acceptance testing.
