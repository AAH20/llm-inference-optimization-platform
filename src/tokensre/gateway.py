from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from .evaluator import evaluate

REQUESTS = Counter("tokensre_requests_total", "Gateway requests", ["backend", "status"])
LATENCY = Histogram("tokensre_upstream_seconds", "Upstream latency", ["backend"])
FAILOVERS = Counter("tokensre_failovers_total", "Backend failovers", ["from_backend", "to_backend"])


class CircuitBreaker:
    def __init__(self, threshold: int = 3, recovery_seconds: int = 30) -> None:
        self.threshold = threshold
        self.recovery_seconds = recovery_seconds
        self.failures: dict[str, int] = defaultdict(int)
        self.opened_at: dict[str, float] = {}

    def available(self, backend: str) -> bool:
        opened = self.opened_at.get(backend)
        if opened is None:
            return True
        if time.monotonic() - opened >= self.recovery_seconds:
            self.failures[backend] = 0
            self.opened_at.pop(backend, None)
            return True
        return False

    def success(self, backend: str) -> None:
        self.failures[backend] = 0
        self.opened_at.pop(backend, None)

    def failure(self, backend: str) -> None:
        self.failures[backend] += 1
        if self.failures[backend] >= self.threshold:
            self.opened_at[backend] = time.monotonic()


class GatewayRuntime:
    def __init__(self, scenario: dict[str, Any]) -> None:
        self.scenario = scenario
        self.report = evaluate(scenario)
        self.backends = {}
        for source in scenario["backends"]:
            item = source.copy()
            prefix = "TOKENSRE_BACKEND_" + item["name"].upper().replace("-", "_")
            item["base_url"] = os.getenv(f"{prefix}_BASE_URL", item.get("base_url"))
            item["api_key_env"] = os.getenv(f"{prefix}_API_KEY_ENV", item.get("api_key_env"))
            self.backends[item["name"]] = item
        self.breaker = CircuitBreaker(
            int(os.getenv("TOKENSRE_CIRCUIT_FAILURES", "3")),
            int(os.getenv("TOKENSRE_CIRCUIT_RECOVERY_SECONDS", "30")),
        )
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(float(os.getenv("TOKENSRE_UPSTREAM_TIMEOUT", "60"))),
            limits=httpx.Limits(max_connections=200, max_keepalive_connections=50),
        )

    async def close(self) -> None:
        await self.client.aclose()

    def candidates(self, workload: str) -> list[dict[str, Any]]:
        route = next((r for r in self.report["routes"] if r["workload"] == workload), None)
        if route is None or route["candidate"] is None:
            return []
        ordered = [route["candidate"], route["baseline"]]
        return [self.backends[name] for name in dict.fromkeys(ordered) if self.breaker.available(name)]


def create_app(scenario: dict[str, Any]) -> FastAPI:
    runtime = GatewayRuntime(scenario)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        await runtime.close()

    app = FastAPI(title="TokenSRE AI Gateway", version="1.0.0", lifespan=lifespan)
    app.state.runtime = runtime

    def authorize(authorization: str | None = Header(default=None)) -> str:
        expected = os.getenv("TOKENSRE_GATEWAY_TOKEN")
        if not expected and os.getenv("TOKENSRE_ENV", "development") == "production":
            raise HTTPException(503, "gateway authentication is not configured")
        if expected and authorization != f"Bearer {expected}":
            raise HTTPException(401, "invalid bearer token", headers={"WWW-Authenticate": "Bearer"})
        return "authenticated" if expected else "development"

    @app.get("/health/live")
    async def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    async def ready() -> dict[str, Any]:
        configured = [b["name"] for b in runtime.backends.values() if b.get("base_url")]
        if not configured:
            raise HTTPException(503, "no live upstream is configured")
        return {"status": "ready", "configured_backends": configured}

    @app.get("/metrics")
    async def metrics(_: str = Depends(authorize)) -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.post("/v1/route")
    async def route(payload: dict[str, Any], _: str = Depends(authorize)) -> dict[str, Any]:
        choices = runtime.candidates(str(payload.get("workload", "")))
        if not choices:
            raise HTTPException(503, "no backend satisfies the production envelope")
        return {"backend": choices[0]["name"], "fallbacks": [item["name"] for item in choices[1:]], "receipt_sha256": runtime.report["receipt_sha256"]}

    @app.post("/v1/chat/completions")
    async def completions(request: Request, _: str = Depends(authorize)) -> Response:
        payload = await request.json()
        workload = request.headers.get("x-tokensre-workload", payload.pop("workload", "rag"))
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        choices = runtime.candidates(str(workload))
        if not choices:
            raise HTTPException(503, "no eligible or available backend")
        previous = choices[0]["name"]
        errors: list[str] = []
        for backend in choices:
            name = backend["name"]
            base_url = backend.get("base_url")
            token_env = backend.get("api_key_env")
            if not base_url or not token_env or not os.getenv(token_env):
                errors.append(f"{name}: live adapter not configured")
                continue
            if name != previous:
                FAILOVERS.labels(previous, name).inc()
            headers = {"authorization": f"Bearer {os.environ[token_env]}", "content-type": "application/json", "x-request-id": request_id}
            started = time.monotonic()
            try:
                upstream = await runtime.client.send(runtime.client.build_request("POST", f"{base_url.rstrip('/')}/v1/chat/completions", json=payload, headers=headers), stream=bool(payload.get("stream")))
                LATENCY.labels(name).observe(time.monotonic() - started)
                if upstream.status_code >= 500 or upstream.status_code == 429:
                    runtime.breaker.failure(name)
                    REQUESTS.labels(name, str(upstream.status_code)).inc()
                    await upstream.aclose()
                    errors.append(f"{name}: upstream {upstream.status_code}")
                    previous = name
                    continue
                runtime.breaker.success(name)
                REQUESTS.labels(name, str(upstream.status_code)).inc()
                response_headers = {"x-request-id": request_id, "x-tokensre-backend": name, "x-tokensre-receipt": runtime.report["receipt_sha256"]}
                if payload.get("stream"):
                    async def body() -> AsyncIterator[bytes]:
                        try:
                            async for chunk in upstream.aiter_raw():
                                yield chunk
                        finally:
                            await upstream.aclose()
                    return StreamingResponse(body(), status_code=upstream.status_code, media_type="text/event-stream", headers=response_headers)
                content = await upstream.aread()
                await upstream.aclose()
                return Response(content, status_code=upstream.status_code, media_type=upstream.headers.get("content-type", "application/json"), headers=response_headers)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                runtime.breaker.failure(name)
                REQUESTS.labels(name, "transport_error").inc()
                errors.append(f"{name}: {type(exc).__name__}")
                previous = name
        incident = hashlib.sha256("|".join(errors).encode()).hexdigest()[:16]
        return JSONResponse(503, {"error": "all_backends_unavailable", "incident": incident, "request_id": request_id})

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the TokenSRE production AI gateway")
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    uvicorn.run(create_app(json.loads(args.scenario.read_text())), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
