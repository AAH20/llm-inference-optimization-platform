import io
import json
import unittest
from pathlib import Path

from tokensre.gateway import DecisionHandler


ROOT = Path(__file__).parents[1]


def invoke(method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    handler = object.__new__(DecisionHandler)
    payload = json.dumps(body or {}).encode()
    handler.path = path
    handler.headers = {"Content-Length": str(len(payload))}
    handler.rfile = io.BytesIO(payload)
    handler.wfile = io.BytesIO()
    captured: dict[str, int] = {}
    handler.send_response = lambda status: captured.update(status=status)
    handler.send_header = lambda *_: None
    handler.end_headers = lambda: None
    getattr(handler, method)()
    return captured["status"], json.loads(handler.wfile.getvalue())


class GatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DecisionHandler.scenario = json.loads((ROOT / "examples/multi-cloud-model-routing/45b-tokens.json").read_text())

    def test_health(self):
        status, payload = invoke("do_GET", "/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")

    def test_route_returns_bounded_decision(self):
        status, payload = invoke("do_POST", "/v1/route", {"workload": "rag"})
        self.assertEqual(status, 200)
        self.assertEqual(payload["route"]["candidate"], "self-hosted-nim")
        self.assertFalse(payload["auto_execute"])
        self.assertEqual(len(payload["receipt_sha256"]), 64)

    def test_unknown_workload_is_rejected(self):
        status, payload = invoke("do_POST", "/v1/route", {"workload": "unknown"})
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "invalid_request")


if __name__ == "__main__":
    unittest.main()
