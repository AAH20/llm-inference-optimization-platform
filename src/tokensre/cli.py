from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import evaluate
from .render import markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate LLM inference routes across quality, latency, cost and capacity")
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = evaluate(json.loads(args.scenario.read_text()))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "inference-scorecard.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.output / "inference-scorecard.md").write_text(markdown(report))
    receipt = {key: report[key] for key in ("schema_version", "scenario", "evidence_level", "promotion", "receipt_sha256")}
    (args.output / "promotion-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
