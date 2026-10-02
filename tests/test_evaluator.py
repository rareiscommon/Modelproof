"""
Unit tests for evaluator metrics and thresholds.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from metrics import category_accuracy, per_category_accuracy
from evaluator import apply_thresholds, compare_to_baseline


def test_category_accuracy():
    results = [{"match": True}, {"match": False}, {"match": True}]
    assert abs(category_accuracy(results) - 2/3) < 1e-9


def test_per_category_accuracy():
    results = [
        {"expected": "billing", "match": True},
        {"expected": "billing", "match": False},
        {"expected": "technical", "match": True},
    ]
    acc = per_category_accuracy(results)
    assert abs(acc["billing"] - 0.5) < 1e-9
    assert abs(acc["technical"] - 1.0) < 1e-9


def test_thresholds():
    assert apply_thresholds(-0.09) == "CRITICAL"
    assert apply_thresholds(-0.05) == "WARNING"
    assert apply_thresholds(-0.01) == "PASS"


def test_compare_baseline():
    current = {"accuracy": 0.8, "results": [{"id": "a", "match": True}, {"id": "b", "match": False}]}
    baseline = {"accuracy": 0.9, "results": [{"id": "a", "match": True}, {"id": "b", "match": True}]}
    diff = compare_to_baseline(current, baseline)
    assert "b" in diff["regressions"]
    assert abs(diff["delta"] + 0.1) < 1e-9


if __name__ == "__main__":
    test_category_accuracy()
    test_per_category_accuracy()
    test_thresholds()
    test_compare_baseline()
    print("All tests passed")
