"""
CLI evaluation runner.
"""
import argparse
import json
from pathlib import Path
import yaml
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from schemas import PromptConfig
from evaluator import evaluate_dataset, load_baseline, compare_to_baseline, apply_thresholds
from reporter import generate_html_report
from run_store import save_run, load_recent_runs
from drift import check_drift
from alerter import post_to_slack


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--baseline", default="data/baseline_run_001.json")
    parser.add_argument("--warning-threshold", type=float, default=-0.03)
    parser.add_argument("--critical-threshold", type=float, default=-0.08)
    parser.add_argument("--output", default="report.html")
    args = parser.parse_args()

    prompt_data = yaml.safe_load(open(args.prompt))
    config = PromptConfig(**prompt_data)

    eval_result = evaluate_dataset(Path(args.dataset), config)
    baseline = load_baseline(Path(args.baseline))
    diff = compare_to_baseline(eval_result, baseline)
    diff["status"] = apply_thresholds(diff["delta"], args.warning_threshold, args.critical_threshold)

    # Build snapshot for storage and alerting
    snapshot = {
        "run_id": None,
        "prompt_version": config.version_id,
        "model": config.model_name,
        "dataset_version": "v1",
        "total_cases": eval_result["total_cases"],
        "correct": eval_result["correct"],
        "accuracy": eval_result["accuracy"],
        "per_category_accuracy": eval_result["per_category_accuracy"],
        "average_judge_score": eval_result.get("average_judge_score", 0.0),
        "status": diff["status"],
        "baseline_accuracy": diff["baseline_accuracy"],
        "delta": diff["delta"],
        "regressions": diff["regressions"],
        "improvements": diff["improvements"],
    }

    # 1. Compute drift (needs current + recent runs + fixed baseline)
    recent_runs = load_recent_runs(6)
    drift_block = check_drift(snapshot, recent_runs)
    snapshot["drift"] = drift_block

    # 2. Save snapshot WITH drift block populated
    save_run(snapshot)

    # 3. Post Slack alert (reads from saved snapshot)
    post_to_slack(snapshot, drift_block)

    generate_html_report(eval_result, diff, Path(args.output))
    print(json.dumps({
        "accuracy": eval_result["accuracy"],
        "baseline_accuracy": diff["baseline_accuracy"],
        "delta": diff["delta"],
        "status": diff["status"],
        "average_judge_score": eval_result.get("average_judge_score"),
        "drift": drift_block
    }, indent=2))


if __name__ == "__main__":
    main()
