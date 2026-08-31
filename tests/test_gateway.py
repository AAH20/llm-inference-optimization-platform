import json
from pathlib import Path

from fastapi.testclient import TestClient

from tokensre.gateway import CircuitBreaker, create_app

ROOT = Path(__file__).parents[1]


def scenario() -> dict:
    value = json.loads((ROOT / "examples/multi-cloud-model-routing/45b-tokens.json").read_text())
    for backend in value["backends"]:
        backend["base_url"] = "https://inference.invalid"
        backend["api_key_env"] = "TEST_UPSTREAM_KEY"
    return value


def test_health_and_readiness():
    with TestClient(create_app(scenario())) as client:
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200


def test_route_returns_receipted_decision():
    with TestClient(create_app(scenario())) as client:
        response = client.post("/v1/route", json={"workload": "rag"})
        assert response.status_code == 200
        assert response.json()["backend"] == "self-hosted-nim"
        assert len(response.json()["receipt_sha256"]) == 64


def test_unknown_workload_is_rejected():
    with TestClient(create_app(scenario())) as client:
        assert client.post("/v1/route", json={"workload": "unknown"}).status_code == 503


def test_production_requires_gateway_authentication(monkeypatch):
    monkeypatch.setenv("TOKENSRE_ENV", "production")
    monkeypatch.delenv("TOKENSRE_GATEWAY_TOKEN", raising=False)
    with TestClient(create_app(scenario())) as client:
        assert client.post("/v1/route", json={"workload": "rag"}).status_code == 503


def test_circuit_breaker_opens_and_recovers(monkeypatch):
    breaker = CircuitBreaker(threshold=2, recovery_seconds=1)
    breaker.failure("nim")
    assert breaker.available("nim")
    breaker.failure("nim")
    assert not breaker.available("nim")
    opened = breaker.opened_at["nim"]
    monkeypatch.setattr("tokensre.gateway.time.monotonic", lambda: opened + 2)
    assert breaker.available("nim")
