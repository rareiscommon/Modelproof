"""
Static HTML report generator.
"""
from pathlib import Path
from typing import Dict


def generate_html_report(eval_result: Dict, baseline_diff: Dict, output_path: Path):
    status = baseline_diff.get("status", "PASS")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Modelproof Evaluation Report</title></head>
<body>
<h1>Modelproof Evaluation Report</h1>
<p>Status: <strong>{status}</strong></p>
<p>Baseline accuracy: {baseline_diff.get('baseline_accuracy',0):.2%}</p>
<p>Current accuracy: {eval_result.get('accuracy',0):.2%}</p>
<p>Delta: {baseline_diff.get('delta',0):+.2%}</p>
<h2>Per Category Accuracy</h2>
<ul>
"""
    for cat, acc in eval_result.get("per_category_accuracy", {}).items():
        html += f"<li>{cat}: {acc:.2%}</li>"
    html += "</ul>"
    html += "<h2>Regressions</h2><ul>"
    for rid in baseline_diff.get("regressions", []):
        html += f"<li>{rid}</li>"
    html += "</ul>"
    html += "<h2>Improvements</h2><ul>"
    for rid in baseline_diff.get("improvements", []):
        html += f"<li>{rid}</li>"
    html += "</ul></body></html>"
    output_path.write_text(html)
