[![Eval](https://github.com/rareiscommon/Modelproof/actions/workflows/eval.yml/badge.svg)](https://github.com/rareiscommon/Modelproof/actions/workflows/eval.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

# Modelproof

Continuous evaluation harness for LLM-powered features. Baseline diffing, drift detection, and CI gating for prompts and models.

## The problem

Prompts change. Models get updated. Embeddings get swapped. And almost nobody tests whether the change made outputs worse.

A prompt that improves 90% of cases can silently break the 10% that matter. You find out when a customer complains.

Modelproof is the missing test harness. It runs your LLM feature against a hand-verified golden dataset on every change, scores the results, diffs against a baseline, and fails CI when quality regresses.

## How it works

1. **Classify** — a customer support email classifier returns structured JSON (category + one-sentence summary). Prompt loaded from versioned YAML, never hardcoded.
2. **Evaluate** — runs the golden dataset, scores category match and LLM-as-judge summary relevance.
3. **Diff** — compares against a baseline run and applies configured thresholds.
4. **Alert** — posts a color-coded Slack alert and a PR comment.
5. **Gate** — blocks merge on CRITICAL regressions (>8 pp accuracy drop).
6. **Package** — ships as a reproducible Docker image.

## What a regression looks like

    Baseline accuracy:  86.7%
    Current run:        73.3%
    Delta:             -13.4 pp
    Threshold:          CRITICAL (>8%)
    Result:             ❌ CI FAILED

Caught before merge. Would have shipped silently without it.

## Current state

- 15 hand-verified golden cases, baseline accuracy 86.7%
- Full CI/CD pipeline (GitHub Actions + Docker)
- Drift detection across a rolling window of runs
- Five security scanners run on every commit: pip-audit, gitleaks, bandit, semgrep, trivy
- 44 tests passing

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

## What's next

- Expand the golden dataset from 15 to 60–80 cases
- Add adversarial input coverage
- Multi-judge scoring to reduce LLM-as-judge variance

---

## License

MIT - see LICENSE.


