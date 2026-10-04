"""
Unit tests for src/drift.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from drift import compute_rolling_average, check_drift, get_drift_status, DEFAULT_DRIFT_THRESHOLD
from run_store import RUNS_DIR, load_recent_runs, save_run


@pytest.fixture
def clean_runs_dir(tmp_path, monkeypatch):
    """Isolate RUNS_DIR to a temporary directory for each test."""
    test_runs_dir = tmp_path / "runs"
    test_runs_dir.mkdir()
    monkeypatch.setattr("run_store.RUNS_DIR", test_runs_dir)
    return test_runs_dir


def test_compute_rolling_average_empty():
    """compute_rolling_average should return 0.0 for empty list."""
    assert compute_rolling_average([]) == 0.0


def test_compute_rolling_average_single():
    """compute_rolling_average should return the single accuracy."""
    runs = [{"accuracy": 0.85}]
    assert compute_rolling_average(runs) == 0.85


def test_compute_rolling_average_multiple():
    """compute_rolling_average should compute mean correctly."""
    runs = [{"accuracy": 0.8}, {"accuracy": 0.9}, {"accuracy": 0.7}]
    assert abs(compute_rolling_average(runs) - 0.8) < 1e-9


def test_compute_rolling_average_skips_missing_accuracy():
    """Runs without 'accuracy' key should be ignored."""
    runs = [{"accuracy": 0.8}, {"other": "data"}, {"accuracy": 1.0}]
    assert abs(compute_rolling_average(runs) - 0.9) < 1e-9


def test_check_drift_no_alert_when_above_threshold(clean_runs_dir):
    """Drift should NOT be alerted when rolling avg >= baseline - threshold."""
    current = {"accuracy": 0.8667}
    recent = [{"accuracy": 0.86}, {"accuracy": 0.87}]

    drift = check_drift(current, recent)

    assert drift["rolling_7_avg"] == pytest.approx(0.8656, abs=0.001)
    assert drift["baseline_reference"] == 0.8667
    assert drift["drift_threshold"] == DEFAULT_DRIFT_THRESHOLD
    assert drift["drift_alerted"] is False


def test_check_drift_alerts_when_below_threshold(clean_runs_dir):
    """Drift SHOULD be alerted when rolling avg < baseline - threshold."""
    # baseline = 0.8667, threshold = 0.03 -> alert if < 0.8367
    current = {"accuracy": 0.80}
    recent = [{"accuracy": 0.80}, {"accuracy": 0.80}]

    drift = check_drift(current, recent)

    # rolling avg = (0.80 + 0.80 + 0.80) / 3 = 0.80
    assert drift["rolling_7_avg"] == 0.80
    assert drift["drift_alerted"] is True


def test_check_drift_boundary_condition(clean_runs_dir):
    """Drift should alert exactly at the boundary (baseline - threshold)."""
    # baseline = 0.8667, threshold = 0.03 -> boundary = 0.8367
    # rolling avg = 0.8367 should NOT alert (strictly less than)
    current = {"accuracy": 0.8367}
    recent = [{"accuracy": 0.8367}]

    drift = check_drift(current, recent)
    assert drift["drift_alerted"] is False  # equal to boundary, not below

    # Slightly below should alert
    current2 = {"accuracy": 0.8366}
    drift2 = check_drift(current2, recent)
    assert drift2["drift_alerted"] is True


def test_get_drift_status_ok():
    """get_drift_status returns 'OK' when drift_alerted is False."""
    drift_block = {"drift_alerted": False}
    assert get_drift_status(drift_block) == "OK"


def test_get_drift_status_drift():
    """get_drift_status returns 'DRIFT' when drift_alerted is True."""
    drift_block = {"drift_alerted": True}
    assert get_drift_status(drift_block) == "DRIFT"


def test_check_drift_includes_current_run_in_average(clean_runs_dir):
    """check_drift should include the current run in the rolling average."""
    current = {"accuracy": 0.9}
    recent = [{"accuracy": 0.8}, {"accuracy": 0.8}]

    drift = check_drift(current, recent)

    # (0.9 + 0.8 + 0.8) / 3 = 0.8333...
    assert drift["rolling_7_avg"] == pytest.approx(0.8333, abs=0.001)


def test_check_drift_custom_threshold(clean_runs_dir):
    """check_drift should respect custom drift_threshold parameter."""
    current = {"accuracy": 0.85}
    recent = [{"accuracy": 0.85}]

    # Tighter threshold: 0.01
    drift = check_drift(current, recent, drift_threshold=0.01)
    # baseline 0.8667 - 0.01 = 0.8567, rolling = 0.85 -> alerts
    assert drift["drift_threshold"] == 0.01
    assert drift["drift_alerted"] is True

    # Looser threshold: 0.05
    drift2 = check_drift(current, recent, drift_threshold=0.05)
    # baseline 0.8667 - 0.05 = 0.8167, rolling = 0.85 -> no alert
    assert drift2["drift_alerted"] is False


def test_drift_block_structure(clean_runs_dir):
    """check_drift should return dict with all expected keys."""
    current = {"accuracy": 0.8}
    recent = []

    drift = check_drift(current, recent)

    assert "rolling_7_avg" in drift
    assert "baseline_reference" in drift
    assert "drift_threshold" in drift
    assert "drift_alerted" in drift
    assert isinstance(drift["drift_alerted"], bool)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))