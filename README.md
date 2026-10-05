# Modelproof

**Model regression detection for LLM-powered features.**

A CI/CD pipeline that detects quality regressions whenever prompts or models change, before bad outputs reach users.

**Status:** Phase 5 of 6 complete.

---

## The Problem

Every team that ships AI features changes prompts. Almost none of them test whether the change made things worse.

A prompt that improves 90% of cases can silently break 10% of edge cases. You only find out when a customer complains, or when the wrong output hits production.

Modelproof is the missing test harness. It runs your LLM feature against a hand-verified golden dataset on every change, scores the results, diffs against the previous run, and alerts you when quality regresses.

---

## What This Does Today

**Phase 1 - Classifier.** A customer support email classifier that returns structured JSON with a category and one-sentence summary. Prompt loaded from versioned YAML, never hardcoded.

**Phase 2 - Golden Dataset.** 15 hand-verified test cases. Baseline accuracy: 86.7%.

**Phase 3 - Evaluation Engine.** Runs the dataset, scores category match and LLM-as-judge summary relevance, diffs against baseline, applies thresholds, generates HTML report.

---

## Prerequisites

- Python 3.11+
- uv
- Groq API key (free tier)

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

