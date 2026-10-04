"""
Drift detection for Modelproof evaluation.

Compares rolling average accuracy against fixed baseline reference.
"""
from typing import List, Dict
from src.run_store import load_recent_runs, load_baseline_accuracy


DEFAULT_DRIFT_THRESHOLD = 0.03  # 3 percentage points


def compute_rolling_average(runs: List[Dict]) -> float:
    """
    Compute mean accuracy across runs.

    Args:
        runs: List of run snapshot dicts (newest first).

    Returns:
        Mean accuracy as float, or 0.0 if no runs.
    """
    if not runs:
        return 0.0
    accuracies = [r.get("accuracy", 0.0) for r in runs if "accuracy" in r]
    return sum(accuracies) / len(accuracies) if accuracies else 0.0


def check_drift(
    current_run: Dict,
    recent_runs: List[Dict],
    drift_threshold: float = DEFAULT_DRIFT_THRESHOLD
) -> Dict:
    """
    Check for drift and return drift block for snapshot.

    Args:
        current_run: The current run snapshot (must include 'accuracy').
        recent_runs: List of recent runs including current (newest first).
        drift_threshold: Threshold in percentage points (default 0.03).

    Returns:
        Drift dict with rolling_7_avg, baseline_reference, drift_threshold, drift_alerted.
    """
    current_accuracy = current_run.get("accuracy", 0.0)

    # Include current run in rolling average calculation
    all_runs = [current_run] + recent_runs
    rolling_avg = compute_rolling_average(all_runs)

    # Fixed baseline reference from baseline_run_001.json
    baseline_reference = load_baseline_accuracy()

    # Drift condition: rolling average below baseline_reference - threshold
    drift_alerted = rolling_avg < (baseline_reference - drift_threshold)

    return {
        "rolling_7_avg": round(rolling_avg, 4),
        "baseline_reference": round(baseline_reference, 4),
        "drift_threshold": drift_threshold,
        "drift_alerted": drift_alerted
    }


def get_drift_status(drift_block: Dict) -> str:
    """
    Get human-readable drift status string.

    Args:
        drift_block: Dict from check_drift().

    Returns:
        "OK" or "DRIFT".
    """
    return "DRIFT" if drift_block.get("drift_alerted") else "OK"