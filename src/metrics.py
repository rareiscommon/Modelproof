"""
Metric calculations for Modelproof evaluation.
"""
from typing import List, Dict
from collections import defaultdict


def category_accuracy(results: List[Dict]) -> float:
    correct = sum(1 for r in results if r.get("match"))
    total = len(results)
    return correct / total if total else 0.0


def per_category_accuracy(results: List[Dict]) -> Dict[str, float]:
    counts = defaultdict(lambda: [0, 0])
    for r in results:
        cat = r.get("expected")
        counts[cat][0] += 1
        if r.get("match"):
            counts[cat][1] += 1
    return {cat: (correct / total if total else 0.0) for cat, (total, correct) in counts.items()}


def llm_judge_summary_score(predicted_summary: str, expected_summary: str, judge_fn=None) -> float:
    """
    Score summary relevance 1-5 using LLM-as-judge.
    If judge_fn is None, returns placeholder 3.0.
    """
    if judge_fn is None:
        return 3.0
    return float(judge_fn(predicted_summary, expected_summary))


def average_judge_score(scores: List[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0
