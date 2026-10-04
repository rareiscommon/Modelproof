"""
Slack alerter for Modelproof evaluation.

Posts evaluation results to Slack via incoming webhook.
Uses attachment format with color coding and blocks.
"""
import os
import json
import logging
from typing import Dict, Optional
import urllib.request
import urllib.error

from src.drift import get_drift_status

logger = logging.getLogger(__name__)


STATUS_COLORS = {
    "PASS": "good",
    "WARNING": "warning",
    "CRITICAL": "danger",
    "DRIFT": "#FF8800",
}


def _build_payload(snapshot: Dict, drift_block: Dict) -> Dict:
    """
    Build Slack attachment payload from snapshot and drift block.

    Args:
        snapshot: Run snapshot dict.
        drift_block: Drift dict from drift.check_drift().

    Returns:
        Dict suitable for JSON serialization to Slack webhook.
    """
    status = snapshot.get("status", "PASS")
    drift_status = get_drift_status(drift_block)

    # Determine effective color: DRIFT overrides if alerted, else status color
    if drift_alerted := drift_block.get("drift_alerted", False):
        color = STATUS_COLORS["DRIFT"]
        effective_status = "DRIFT"
    else:
        color = STATUS_COLORS.get(status, "good")
        effective_status = status

    accuracy = snapshot.get("accuracy", 0.0)
    baseline = snapshot.get("baseline_accuracy", 0.0)
    delta = snapshot.get("delta", 0.0)
    judge_score = snapshot.get("average_judge_score", 0.0)
    regressions = len(snapshot.get("regressions", []))
    improvements = len(snapshot.get("improvements", []))

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Modelproof Evaluation — {effective_status}"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Status:* {effective_status}"},
                {"type": "mrkdwn", "text": f"*Accuracy:* {accuracy:.2%}"},
                {"type": "mrkdwn", "text": f"*Baseline:* {baseline:.2%}"},
                {"type": "mrkdwn", "text": f"*Delta:* {delta:+.2%}"}
            ]
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Judge Score:* {judge_score:.1f}/5"},
                {"type": "mrkdwn", "text": f"*Regressions:* {regressions}"},
                {"type": "mrkdwn", "text": f"*Improvements:* {improvements}"},
                {"type": "mrkdwn", "text": f"*Drift:* {drift_status}"}
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        f"Prompt {snapshot.get('prompt_version', '?')} • "
                        f"Model {snapshot.get('model', '?')} • "
                        f"Dataset {snapshot.get('dataset_version', '?')}"
                    )
                }
            ]
        }
    ]

    return {
        "attachments": [
            {
                "color": color,
                "blocks": blocks
            }
        ]
    }


def post_to_slack(snapshot: Dict, drift_block: Dict) -> bool:
    """
    Post evaluation result to Slack webhook.

    Args:
        snapshot: Run snapshot dict.
        drift_block: Drift dict from drift.check_drift().

    Returns:
        True if posted successfully, False otherwise (including missing webhook).
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logger.debug("SLACK_WEBHOOK_URL not set; skipping Slack notification")
        return False

    payload = _build_payload(snapshot, drift_block)

    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                logger.info("Slack notification sent successfully")
                return True
            else:
                logger.warning(f"Slack webhook returned status {response.status}")
                return False
    except urllib.error.URLError as e:
        logger.warning(f"Slack notification failed: {e}")
        return False
    except Exception as e:
        logger.warning(f"Slack notification error: {e}")
        return False