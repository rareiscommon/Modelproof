"""
Run snapshot storage for Modelproof evaluation.

Provides atomic write, sorted reads, and FIFO rotation (max 7 snapshots).
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict


RUNS_DIR = Path(__file__).resolve().parents[1] / "data" / "runs"
MAX_RUNS = 7


def _ensure_dir():
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp_for_filename() -> str:
    """Return UTC timestamp in Windows-safe format with microseconds: YYYY-MM-DDTHHMMSS.ffffffZ."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%S.%fZ")


def save_run(snapshot: Dict) -> Path:
    """
    Save a run snapshot atomically.

    Args:
        snapshot: Dict containing the run data. Must include 'run_id' key
                  or it will be generated from current timestamp.

    Returns:
        Path to the saved file.
    """
    _ensure_dir()

    run_id = snapshot.get("run_id") or _timestamp_for_filename()
    snapshot["run_id"] = run_id

    filename = f"{run_id}.json"
    target_path = RUNS_DIR / filename
    temp_path = RUNS_DIR / f".{filename}.tmp"

    # Atomic write: write to temp, then replace
    with open(temp_path, "w") as f:
        json.dump(snapshot, f, indent=2)
    os.replace(temp_path, target_path)

    # Rotate: keep only MAX_RUNS most recent
    _rotate()

    return target_path


def load_recent_runs(limit: int = MAX_RUNS) -> List[Dict]:
    """
    Load the most recent run snapshots, sorted by run_id descending (newest first).

    Args:
        limit: Maximum number of runs to return.

    Returns:
        List of run snapshot dicts, newest first.
    """
    _ensure_dir()

    runs = []
    for path in RUNS_DIR.glob("*.json"):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            runs.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    # Sort by run_id descending (newest first)
    runs.sort(key=lambda r: r.get("run_id", ""), reverse=True)

    return runs[:limit]


def _rotate():
    """Delete oldest snapshots if count exceeds MAX_RUNS."""
    files = sorted(RUNS_DIR.glob("*.json"))
    if len(files) > MAX_RUNS:
        for old in files[:-MAX_RUNS]:
            try:
                old.unlink()
            except OSError:
                pass


def load_baseline_accuracy() -> float:
    """
    Load the fixed baseline accuracy from data/baseline_run_001.json.

    Returns:
        Baseline accuracy as float, or 0.0 if not found.
    """
    baseline_path = Path(__file__).resolve().parents[1] / "data" / "baseline_run_001.json"
    try:
        with open(baseline_path, "r") as f:
            data = json.load(f)
        return float(data.get("accuracy", 0.0))
    except (OSError, json.JSONDecodeError, KeyError):
        return 0.0