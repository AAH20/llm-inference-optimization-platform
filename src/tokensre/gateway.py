from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .evaluator import evaluate


class DecisionHandler(BaseHTTPRequestHandler):
    scenario: dict[str, Any] = {}

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._json(200, {"status": "ok", "service": "tokensre-decision-api"})
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path != "/v1/route":
            self._json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length) or b"{}")
            workload = request["workload"]
            report = evaluate(self.scenario)
            route = next(item for item in report["routes"] if item["workload"] == workload)
            status = 200 if route["status"] == "eligible" else 503
            self._json(status, {"route": route, "receipt_sha256": report["receipt_sha256"], "auto_execute": False})
        except (KeyError, ValueError, StopIteration, json.JSONDecodeError) as exc:
            self._json(400, {"error": "invalid_request", "detail": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _json(self, status: int, body: dict[str, Any]) -> None:
        payload = json.dumps(body, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the TokenSRE bounded inference decision API")
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    DecisionHandler.scenario = json.loads(args.scenario.read_text())
    ThreadingHTTPServer((args.host, args.port), DecisionHandler).serve_forever()


if __name__ == "__main__":
    main()
