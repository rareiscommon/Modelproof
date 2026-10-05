[![Eval](https://github.com/rareiscommon/Modelproof/actions/workflows/eval.yml/badge.svg)](https://github.com/rareiscommon/Modelproof/actions/workflows/eval.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

# Modelproof

**Continuous regression testing for LLM-powered applications.**

Modelproof evaluates LLM features against versioned golden datasets and detects quality regressions when prompts, models, or evaluation logic change — before bad outputs reach users.

Status: **Phase 6 — Polish**
---

## The Problem

Every team that ships AI features changes prompts. Almost none of them test whether the change made things worse.

A prompt that improves 90% of cases can silently break 10% of edge cases. You only find out when a customer complains, or when the wrong output hits production.

Modelproof is the missing test harness. It runs your LLM feature against a hand-verified golden dataset on every change, scores the results, diffs against the previous run, and alerts you when quality regresses.

---
## What This Does Today

**Phase 1 — Classifier.** A customer support email classifier that returns structured JSON with a category and one-sentence summary. Prompt loaded from versioned YAML, never hardcoded.

**Phase 2 — Golden Dataset.** 15 hand-verified test cases. Baseline accuracy: 86.7%.

**Phase 3 — Evaluation Engine.** Runs the dataset, scores category match and LLM-as-judge summary relevance, diffs against baseline, applies statistical thresholds, generates an HTML report.

**Phase 4 — Alerts + Drift Detection.** Detects evaluation drift across a rolling window of runs and sends color-coded regression alerts via Slack.

**Phase 5 — CI/CD + Docker.** Runs the regression evaluation on every PR, posts results as a PR comment, blocks merge on CRITICAL regressions, and packages the system in a reproducible container.

## Example regression

    Baseline accuracy:  86.7%
    Current run:        73.3%
    Delta:             -13.4 pp
    Threshold:          CRITICAL (>8%)
    Result:             ❌ CI FAILED

Modelproof caught this before merge. Without it, the regression would have shipped silently.
---

## Prerequisites

- Python 3.11+
- uv
- Groq API key

---

## Setup

```bash
git clone git@github.com:rareiscommon/Modelproof.git
cd Modelproof
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
```

---

## Usage

Smoke test:

```bash
python scripts/smoke_test.py
```

Full evaluation:

```bash
python scripts/evaluate.py \
  --dataset data/golden_dataset_v1.json \
  --prompt prompts/v1.yaml \
  --baseline data/baseline_run_001.json \
  --output report.html
```

Tests:

```bash
pytest tests/ -v
```

---

## Architecture

```
prompts/v1.yaml --> src/classifier --> Groq API
                          |
                          v
                  EmailClassification
                          |
                          v
                src/evaluator + metrics
                          |
                          v
                  src/reporter (HTML)
```

---

## Security

Five scanners run on every commit: pip-audit, gitleaks, bandit, semgrep, trivy.

---

## Roadmap

| Phase | Deliverable | Status |
|---|---|---|
| 1 | Classifier | Complete |
| 2 | Golden dataset + baseline | Complete |
| 3 | Evaluation engine | Complete |
| 4 | Slack alerts + drift detection | Complete |
| 5 | CI/CD + Docker | Complete |
| 6 | Polish | In progress |

---

## License

MIT - see LICENSE.

