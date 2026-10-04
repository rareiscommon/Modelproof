"""
Unit tests for src/run_store.py
"""
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from run_store import save_run, load_recent_runs, load_baseline_accuracy, RUNS_DIR, MAX_RUNS


@pytest.fixture
def isolated_runs_dir(tmp_path, monkeypatch):
    """Isolate RUNS_DIR to a temporary directory for each test."""
    test_runs_dir = tmp_path / "runs"
    test_runs_dir.mkdir()
    monkeypatch.setattr("run_store.RUNS_DIR", test_runs_dir)
    monkeypatch.setattr("run_store.MAX_RUNS", 7)
    return test_runs_dir


def test_save_run_writes_valid_json(isolated_runs_dir):
    """save_run() writes a valid JSON file to RUNS_DIR."""
    snapshot = {"accuracy": 0.85, "status": "PASS", "total_cases": 15}
    path = save_run(snapshot)

    assert path.exists()
    assert path.suffix == ".json"
    assert path.parent == isolated_runs_dir

    with open(path, "r") as f:
        data = json.load(f)
    assert data["accuracy"] == 0.85
    assert data["status"] == "PASS"


def test_save_run_filename_format(isolated_runs_dir):
    """save_run() filename matches YYYY-MM-DDTHHMMSS.ffffffZ.json format."""
    snapshot = {"accuracy": 0.5}
    path = save_run(snapshot)

    import re
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{6}\.\d{6}Z\.json$", path.name)


def test_save_run_returns_path(isolated_runs_dir):
    """save_run() returns a Path object pointing to the written file."""
    snapshot = {"accuracy": 0.5}
    path = save_run(snapshot)

    assert isinstance(path, Path)
    assert path == isolated_runs_dir / path.name


def test_load_recent_runs_sorted_descending(isolated_runs_dir):
    """load_recent_runs() returns a list sorted newest first."""
    for i in range(3):
        save_run({"accuracy": 0.5 + i * 0.1, "seq": i})
        time.sleep(0.01)

    runs = load_recent_runs(5)
    assert len(runs) == 3
    assert runs[0]["seq"] == 2
    assert runs[1]["seq"] == 1
    assert runs[2]["seq"] == 0


def test_load_recent_runs_respects_limit(isolated_runs_dir):
    """load_recent_runs(limit=N) respects the limit."""
    for i in range(5):
        save_run({"accuracy": float(i), "seq": i})
        time.sleep(0.01)

    runs = load_recent_runs(3)
    assert len(runs) == 3
    assert runs[0]["seq"] == 4
    assert runs[2]["seq"] == 2


def test_fifo_rotation_max_7(isolated_runs_dir):
    """FIFO rotation: saving 10 runs leaves only the 7 newest on disk."""
    for i in range(9):
        save_run({"accuracy": float(i), "seq": i})
        time.sleep(0.01)

    runs = load_recent_runs(20)
    assert len(runs) == 7
    assert runs[-1]["seq"] == 2
    assert runs[0]["seq"] == 8

    # Also verify on disk
    files = list(isolated_runs_dir.glob("*.json"))
    assert len(files) == 7


def test_load_recent_runs_empty_directory(isolated_runs_dir):
    """load_recent_runs() returns [] when directory is empty."""
    runs = load_recent_runs(5)
    assert runs == []


def test_file_content_round_trips(isolated_runs_dir):
    """File content is valid JSON that round-trips (read == written)."""
    original = {"accuracy": 0.9, "custom_field": "test", "nested": {"a": 1}}
    path = save_run(original)

    with open(path, "r") as f:
        loaded = json.load(f)

    assert loaded == original


def test_load_baseline_accuracy():
    """load_baseline_accuracy should read from baseline_run_001.json."""
    baseline = load_baseline_accuracy()
    assert abs(baseline - 0.8667) < 0.001


def test_run_id_generated_if_missing(isolated_runs_dir):
    """If snapshot lacks run_id, one should be generated from timestamp."""
    snapshot = {"accuracy": 0.5}
    path = save_run(snapshot)

    assert "run_id" in snapshot
    assert snapshot["run_id"] == path.stem
    import re
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{6}\.\d{6}Z", snapshot["run_id"])


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))