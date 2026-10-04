"""
Evaluation runner with baseline diff and thresholds.
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.metrics import category_accuracy, per_category_accuracy, llm_judge_summary_score, average_judge_score
from src.schemas import PromptConfig
from src.classifier import classify_email


def load_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)


def evaluate_dataset(dataset_path: Path, prompt_config: PromptConfig) -> Dict:
    dataset = load_json(dataset_path)
    results = []
    judge_scores = []
    for case in dataset:
        text = case["text"]
        expected = case["category"]
        expected_summary = case.get("summary", "")
        classification = classify_email(text, prompt_config)
        match = classification.category == expected
        judge_score = llm_judge_summary_score(classification.summary, expected_summary)
        judge_scores.append(judge_score)
        results.append({
            "id": case["id"],
            "expected": expected,
            "got": classification.category,
            "match": match,
            "difficulty": case.get("difficulty"),
            "predicted_summary": classification.summary,
            "judge_score": judge_score
        })
    accuracy = category_accuracy(results)
    per_cat = per_category_accuracy(results)
    avg_judge = average_judge_score(judge_scores)
    return {
        "total_cases": len(results),
        "correct": sum(1 for r in results if r["match"]),
        "accuracy": accuracy,
        "per_category_accuracy": per_cat,
        "average_judge_score": avg_judge,
        "results": results
    }


def load_baseline(baseline_path: Path) -> Dict:
    return load_json(baseline_path)


def compare_to_baseline(current: Dict, baseline: Dict) -> Dict:
    baseline_map = {r["id"]: r["match"] for r in baseline.get("results", [])}
    regressions = []
    improvements = []
    for r in current["results"]:
        bid = r["id"]
        b_match = baseline_map.get(bid, None)
        if b_match is None:
            continue
        if b_match and not r["match"]:
            regressions.append(r["id"])
        elif not b_match and r["match"]:
            improvements.append(r["id"])
    current_acc = current["accuracy"]
    baseline_acc = baseline.get("accuracy", 0)
    delta = current_acc - baseline_acc
    return {
        "baseline_accuracy": baseline_acc,
        "current_accuracy": current_acc,
        "delta": delta,
        "regressions": regressions,
        "improvements": improvements
    }


def apply_thresholds(delta: float, warning_thresh: float = -0.03, critical_thresh: float = -0.08) -> str:
    if delta < critical_thresh:
        return "CRITICAL"
    if delta < warning_thresh:
        return "WARNING"
    return "PASS"
