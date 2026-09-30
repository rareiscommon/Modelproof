# Model Regression Detector

A CI/CD-style pipeline that continuously tests LLM-powered features against a golden dataset whenever a prompt or model changes, detects quality regressions, and alerts before bad outputs reach users.

**Status:** Phase 1 complete — customer support email classifier with versioned prompts.

## What This Does

Classifies customer support emails into one of four categories: billing, technical, account, or general. It generates a one-sentence summary, using a versioned prompt loaded from YAML and Groq's OpenAI-compatible API.

## Structure

- `prompts/` — versioned prompt configurations (YAML)
- `src/` — classifier, schemas, exceptions
- `scripts/` — runnable scripts (smoke test)

## Setup
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
export GROQ_API_KEY="gsk_your_key_here"
python scripts/smoke_test.py



## Roadmap

- Phase 1 — Classifier ✅
- Phase 2 — Golden dataset (hand-labeled test cases)
- Phase 3 — Evaluation engine (multi-dimensional scoring, regression detection)
- Phase 4 — Reporting + Slack alerts
- Phase 5 — CI/CD integration (GitHub Actions)
- Phase 6 — Polish (Loom walkthrough, blog post)
