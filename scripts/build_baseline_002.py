"""One-shot: run evaluator on golden_dataset_v2 and write baseline_run_002.json
in the same schema as baseline_run_001.json."""
import json
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from schemas import PromptConfig
from evaluator import evaluate_dataset

DATA = Path("data")
DATASET = DATA / "golden_dataset_v2.json"
PROMPT = Path("prompts/v1.yaml")
OUT = DATA / "baseline_run_002.json"


def main():
    prompt_data = yaml.safe_load(open(PROMPT))
    config = PromptConfig(**prompt_data)

    result = evaluate_dataset(DATASET, config)

    # Match baseline_run_001.json schema exactly:
    # run_at, prompt_version, model, total_cases, correct, accuracy, results
    # results rows: id, expected, got, match, difficulty
    trimmed = [
        {
            "id": r["id"],
            "expected": r["expected"],
            "got": r["got"],
            "match": r["match"],
            "difficulty": r["difficulty"],
        }
        for r in result["results"]
    ]

    out = {
        "run_at": str(date.today()),
        "prompt_version": config.version_id,
        "model": config.model_name,
        "total_cases": result["total_cases"],
        "correct": result["correct"],
        "accuracy": round(result["accuracy"], 4),
        "results": trimmed,
    }

    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {OUT}")
    print(f"total={out['total_cases']} correct={out['correct']} accuracy={out['accuracy']}")


if __name__ == "__main__":
    main()
