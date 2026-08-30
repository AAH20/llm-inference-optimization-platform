import json
import unittest
from pathlib import Path

from tokensre.evaluator import evaluate


ROOT = Path(__file__).parents[1]


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.intent = json.loads((ROOT / "examples/multi-cloud-model-routing/45b-tokens.json").read_text())

    def test_routes_simple_workload_to_nim(self):
        routes = {route["workload"]: route for route in evaluate(self.intent)["routes"]}
        self.assertEqual(routes["classification"]["candidate"], "self-hosted-nim")

    def test_routes_code_to_azure(self):
        routes = {route["workload"]: route for route in evaluate(self.intent)["routes"]}
        self.assertEqual(routes["code"]["candidate"], "azure-foundry-router")

    def test_keeps_frontier_reasoning(self):
        routes = {route["workload"]: route for route in evaluate(self.intent)["routes"]}
        self.assertEqual(routes["reasoning"]["candidate"], "frontier-api")

    def test_unhealthy_backend_excluded(self):
        candidates = {route["candidate"] for route in evaluate(self.intent)["routes"]}
        self.assertNotIn("self-hosted-vllm", candidates)

    def test_cost_reduction_is_measurable(self):
        score = evaluate(self.intent)["scorecard"]
        self.assertEqual(score["baseline_monthly_cost_usd"], 234000.0)
        self.assertGreater(score["modeled_monthly_savings_usd"], 0)

    def test_revenue_and_margin_are_attributed(self):
        report = evaluate(self.intent)
        self.assertEqual(report["scorecard"]["modeled_monthly_revenue_usd"], 6010000.0)
        self.assertGreater(report["scorecard"]["candidate_contribution_margin_usd"], report["scorecard"]["baseline_contribution_margin_usd"])
        self.assertTrue(all(route["contribution_margin_pct"] > 0 for route in report["routes"]))

    def test_missing_request_economics_fail_closed(self):
        del self.intent["workloads"][0]["monthly_requests"]
        with self.assertRaises(ValueError):
            evaluate(self.intent)

    def test_never_auto_executes(self):
        self.assertFalse(evaluate(self.intent)["production_control"]["auto_execute"])

    def test_receipt_is_deterministic(self):
        self.assertEqual(evaluate(self.intent)["receipt_sha256"], evaluate(self.intent)["receipt_sha256"])

    def test_duplicate_backends_rejected(self):
        self.intent["backends"].append(self.intent["backends"][0])
        with self.assertRaises(ValueError):
            evaluate(self.intent)


if __name__ == "__main__":
    unittest.main()
