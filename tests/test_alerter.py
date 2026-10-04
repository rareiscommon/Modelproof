"""
Unit tests for src/alerter.py
"""
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from alerter import _build_payload, post_to_slack, STATUS_COLORS


def test_no_op_when_slack_webhook_url_is_unset():
    """No-op when SLACK_WEBHOOK_URL is unset - post_to_slack returns False."""
    import os
    os.environ.pop("SLACK_WEBHOOK_URL", None)

    snapshot = {"status": "PASS", "accuracy": 0.86}
    drift_block = {"drift_alerted": False}

    result = post_to_slack(snapshot, drift_block)
    assert result is False


def test_payload_has_attachments_key_with_one_attachment():
    """Payload has 'attachments' key with one attachment."""
    snapshot = {
        "status": "PASS",
        "accuracy": 0.8667,
        "baseline_accuracy": 0.8667,
        "delta": -0.0033,
        "average_judge_score": 4.5,
        "regressions": ["gd-0012"],
        "improvements": ["gd-0015"],
        "prompt_version": "v1",
        "model": "openai/gpt-oss-120b",
        "dataset_version": "v1",
    }
    drift_block = {"drift_alerted": False}

    payload = _build_payload(snapshot, drift_block)

    assert "attachments" in payload
    assert len(payload["attachments"]) == 1


def test_color_mapping_pass_warning_critical_drift():
    """Color mapping: PASS=good, WARNING=warning, CRITICAL=danger, DRIFT=#FF8800."""
    # PASS
    snapshot = {"status": "PASS", "accuracy": 0.86, "baseline_accuracy": 0.8667,
                "delta": -0.0067, "average_judge_score": 4.5, "regressions": [],
                "improvements": [], "prompt_version": "v1", "model": "test",
                "dataset_version": "v1"}
    drift_block = {"drift_alerted": False}
    payload = _build_payload(snapshot, drift_block)
    assert payload["attachments"][0]["color"] == "good"

    # WARNING
    snapshot["status"] = "WARNING"
    payload = _build_payload(snapshot, drift_block)
    assert payload["attachments"][0]["color"] == "warning"

    # CRITICAL
    snapshot["status"] = "CRITICAL"
    payload = _build_payload(snapshot, drift_block)
    assert payload["attachments"][0]["color"] == "danger"

    # DRIFT
    drift_block["drift_alerted"] = True
    snapshot["status"] = "PASS"
    payload = _build_payload(snapshot, drift_block)
    assert payload["attachments"][0]["color"] == "#FF8800"


def test_attachment_has_blocks_list():
    """Attachment has 'blocks' list."""
    snapshot = {
        "status": "PASS", "accuracy": 0.8667, "baseline_accuracy": 0.8667,
        "delta": -0.0033, "average_judge_score": 4.5,
        "regressions": ["gd-0012"], "improvements": ["gd-0015"],
        "prompt_version": "v1", "model": "openai/gpt-oss-120b", "dataset_version": "v1",
    }
    drift_block = {"drift_alerted": False}

    payload = _build_payload(snapshot, drift_block)
    attachment = payload["attachments"][0]
    assert "blocks" in attachment
    assert isinstance(attachment["blocks"], list)


def test_payload_includes_all_required_fields():
    """Payload includes status, accuracy, baseline, delta, judge score, regressions, improvements, drift."""
    snapshot = {
        "status": "PASS", "accuracy": 0.8667, "baseline_accuracy": 0.8667,
        "delta": -0.0033, "average_judge_score": 4.5,
        "regressions": ["gd-0012"], "improvements": ["gd-0015"],
        "prompt_version": "v1", "model": "openai/gpt-oss-120b", "dataset_version": "v1",
    }
    drift_block = {"drift_alerted": False}

    payload = _build_payload(snapshot, drift_block)
    attachment = payload["attachments"][0]
    blocks = attachment["blocks"]

    # Header block should contain status
    assert blocks[0]["type"] == "header"

    # Section fields should include accuracy, baseline, delta
    section = blocks[1]
    field_texts = [f["text"] for f in section["fields"]]
    assert any("*Accuracy:*" in f for f in field_texts)
    assert any("*Baseline:*" in f for f in field_texts)
    assert any("*Delta:*" in f for f in field_texts)

    # Second section should include judge score, regressions, improvements, drift
    section2 = blocks[2]
    field_texts2 = [f["text"] for f in section2["fields"]]
    assert any("*Judge Score:*" in f for f in field_texts2)
    assert any("*Regressions:*" in f for f in field_texts2)
    assert any("*Improvements:*" in f for f in field_texts2)
    assert any("*Drift:*" in f for f in field_texts2)


def test_network_error_caught_does_not_raise():
    """Network error caught, does not raise."""
    import os
    os.environ["SLACK_WEBHOOK_URL"] = "https://hooks.slack.com/services/TEST"

    with patch("alerter.urllib.request.urlopen", side_effect=Exception("network down")):
        snapshot = {"status": "PASS", "accuracy": 0.86}
        drift_block = {"drift_alerted": False}

        result = post_to_slack(snapshot, drift_block)
        assert result is False


def test_http_4xx_5xx_caught_does_not_raise():
    """HTTP 4xx/5xx caught, does not raise."""
    import os
    os.environ["SLACK_WEBHOOK_URL"] = "https://hooks.slack.com/services/TEST"

    mock_response = MagicMock()
    mock_response.status = 500

    with patch("alerter.urllib.request.urlopen", return_value=mock_response):
        snapshot = {"status": "PASS", "accuracy": 0.86}
        drift_block = {"drift_alerted": False}

        result = post_to_slack(snapshot, drift_block)
        assert result is False