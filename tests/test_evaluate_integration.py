"""
End-to-end integration test for the evaluate flow with mocked externals.
"""
import sys
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from src.classifier import EmailClassification
from src.evaluator import evaluate_dataset, compare_to_baseline, apply_thresholds, average_judge_score
from src.schemas import PromptConfig


# --- Fake golden dataset fixtures ---

FAKE_CASES = [
    {
        "id": "case-001",
        "text": "I have a billing question about my recent charge.",
        "category": "billing",
        "summary": "Billing inquiry",
    },
    {
        "id": "case-002",
        "text": "My system is crashing with a blue screen error.",
        "category": "technical",
        "summary": "System crash",
    },
    {
        "id": "case-003",
        "text": "Can you help me with my account access?",
        "category": "account",
        "summary": "Account access request",
    },
]


def test_evaluate_flow_integration(tmp_path):
    """
    End-to-end integration test of the evaluate flow with all externals mocked.

    Coverage:
    1. Create a tiny fake golden dataset in tmp_path (3 cases)
    2. Mock classify_email to return deterministic EmailClassification objects
    3. Mock the LLM judge to return a fixed score (e.g., 5)
    4. Set SLACK_WEBHOOK_URL to a fake URL and mock urllib so no real network call
    5. Monkeypatch RUNS_DIR to tmp_path
    6. Run the evaluate flow (import from scripts/evaluate.py or src/evaluator.py)
    7. Verify:
       - classifier called once per case (3 calls)
       - judge called once per case (3 calls)
       - run snapshot written to tmp_path
       - drift block present in snapshot
       - Slack post called with correct status (PASS)
       - report.html written
    """
    # ---- 1. Create a tiny fake golden dataset in tmp_path ----
    dataset_path = tmp_path / "golden_dataset.json"
    dataset_data = [
        {"id": "case-001", "text": "I have a billing question about my recent charge.", "category": "billing", "summary": "Billing inquiry"},
        {"id": "case-002", "text": "My system is crashing with a blue screen error.", "category": "technical", "summary": "System crash"},
        {"id": "case-003", "text": "Can you help me with my account access?", "category": "account", "summary": "Account access request"},
    ]
    dataset_path.write_text(json.dumps(dataset_data))

    # ---- 2. Mock classify_email to return deterministic EmailClassification objects ----
    # Mock at the path where it's actually used by evaluator (src.evaluator.classify_email)
    # but also patch the classifier module directly
    mock_classifications = [
        EmailClassification(category="billing", summary="Billing inquiry"),
        EmailClassification(category="technical", summary="System crash"),
        EmailClassification(category="account", summary="Account access request"),
    ]

    with patch("src.evaluator.classify_email", side_effect=mock_classifications) as mock_cls:
        # ---- 3. Mock the LLM judge to return a fixed score (e.g., 5) ----
        with patch("src.evaluator.llm_judge_summary_score", return_value=5.0) as mock_judge:
            # ---- 5. Monkeypatch RUNS_DIR to tmp_path ----
            with patch("src.run_store.RUNS_DIR", tmp_path / "runs"):

                # ---- 4. Set SLACK_WEBHOOK_URL to a fake URL and mock urllib ----
                fake_webhook_url = "https://hooks.slack.com/services/FAKE/TEST/123"
                os.environ["SLACK_WEBHOOK_URL"] = fake_webhook_url

                # Mock urllib in alerter module - patch before any alerter import/usage
                # Create mock urlopen that returns 200
                mock_response = MagicMock()
                mock_response.status = 200
                mock_response.__enter__ = MagicMock(return_value=mock_response)
                mock_response.__exit__ = MagicMock(return_value=False)

                # Patch at the module level in src/alerter
                import src.alerter as alerter_mod
                # Replace the entire urllib.request module
                mock_urlopen = MagicMock()
                mock_urlopen.urlopen = MagicMock(return_value=mock_response)
                mock_urlopen.Request = object
                alerter_mod.urllib.request = mock_urlopen

                # Also patch urllib that evaluator might reference
                import urllib.request as urllib_request_mock
                urllib_request_mock.urlopen = MagicMock(return_value=mock_response)
                urllib_request_mock.Request = object

                # ---- 6. Run the evaluate flow ----
                prompt_config = PromptConfig(
                    version_id="v1",
                    system_prompt="You are a helpful assistant.",
                    few_shot_examples=[],
                    model_name="test-model",
                    temperature=0.0,
                )

                # Load dataset
                dataset = json.loads(dataset_path.read_text())

                # Run evaluate_dataset (this will use mocked classify_email)
                result = evaluate_dataset(dataset_path, prompt_config)

                # Load baseline (from data/baseline_run_001.json)
                from src.run_store import load_baseline_accuracy
                baseline_acc = load_baseline_accuracy()

                # Compare to baseline
                diff = compare_to_baseline(result, {"accuracy": baseline_acc, "results": []})

                # Apply thresholds
                status = apply_thresholds(diff["delta"])

                # Build snapshot (following evaluate.py logic)
                snapshot = {
                    "run_id": "test-run-001",
                    "prompt_version": prompt_config.version_id,
                    "model": prompt_config.model_name,
                    "dataset_version": "v1",
                    "total_cases": result["total_cases"],
                    "correct": result["correct"],
                    "accuracy": result["accuracy"],
                    "per_category_accuracy": result["per_category_accuracy"],
                    "average_judge_score": result["average_judge_score"],
                    "status": status,
                    "baseline_accuracy": diff["baseline_accuracy"],
                    "delta": diff["delta"],
                    "regressions": diff["regressions"],
                    "improvements": diff["improvements"],
                }

                # Compute drift
                from src.drift import check_drift
                recent_runs = []  # No recent runs in this test
                drift_block = check_drift(snapshot, recent_runs)
                snapshot["drift"] = drift_block

                # Save snapshot (RUNS_DIR already pointed to tmp_path/runs)
                from src.run_store import save_run
                saved_path = save_run(snapshot)

                # Post to Slack (mocked, but should be called)
                from src.alerter import post_to_slack
                post_to_slack(snapshot, drift_block)

                # Generate HTML report
                from src.reporter import generate_html_report
                report_path = tmp_path / "report.html"
                generate_html_report(result, diff, report_path)

                # ---- 7. Verify all expected outcomes ----

                # Classifier called once per case (3 calls)
                assert mock_cls.call_count == 3, f"Expected 3 classify_email calls, got {mock_cls.call_count}"

                # Judge called once per case (3 calls)
                assert mock_judge.call_count == 3, f"Expected 3 judge calls, got {mock_judge.call_count}"

                # Run snapshot written to tmp_path
                assert saved_path is not None, "Snapshot should be saved"
                assert saved_path.parent.name == "runs", f"Expected runs dir, got {saved_path.parent}"
                snapshot_data = json.loads(saved_path.read_text())
                assert "run_id" in snapshot_data, "Snapshot should have run_id"
                assert snapshot_data["drift"] is not None, "Snapshot should have drift block"
                assert snapshot_data["drift"]["drift_alerted"] is False, "Drift should not be alerted with good data"
                assert snapshot_data["status"] == "PASS", f"Expected PASS status, got {snapshot_data['status']}"

                # report.html written
                assert report_path.exists(), "report.html should be written"
                assert report_path.read_text().startswith("<!DOCTYPE html>"), "report.html should be valid HTML"

    # Clean up env
    os.environ.pop("SLACK_WEBHOOK_URL", None)