# Roadmap

## Current Status

All six phases complete. Modelproof runs end-to-end: change a prompt, trigger
evaluation, detect regression, block merge.

- Classifier with versioned prompts, typed interface, Groq provider, smoke test
- Golden dataset v1 — 15 hand-verified cases, baseline accuracy 86.7%
- Evaluation engine — category accuracy + LLM-as-judge scoring, baseline diff,
  configured thresholds (3% WARNING, 8% CRITICAL), HTML report
- Regression detection — 7-run rolling average, drift tracking vs baseline
- Alerts — Slack webhook with color-coded payload, no-op if unconfigured
- CI integration — GitHub Actions workflow, PR comment, merge block on CRITICAL

## Phase 1 — Classifier

- Customer support email classifier returning structured JSON (category + summary)
- Prompt loaded from versioned YAML, never hardcoded
- Pydantic-typed interface, JSON-mode enforcement
- Groq provider, smoke test CLI

## Phase 2 — Golden Dataset

- 15 hand-verified test cases across the classifier's label space
- Dataset manifest with version metadata
- Baseline run locked at 86.7% accuracy

## Phase 3 — Evaluation Engine

- Loads dataset + prompt config, runs classifier, compares category and summary
- Metrics: category accuracy + LLM-as-judge summary scoring
- Baseline diff with configured thresholds (3% WARNING, 8% CRITICAL)
- Static HTML report written to disk
- Reproducible from CLI — same inputs, same outputs

## Phase 4 — Regression Detection

- Snapshot storage with 7-run FIFO rotation
- Rolling average compared against fixed baseline
- Drift detection across runs
- Configurable thresholds

## Phase 5 — Notifications

- Slack alert with headline metrics and color-coded pass/warn/fail payload
- GitHub PR comment with pass/fail summary
- No-op when webhook is unconfigured

## Phase 6 — CI Integration

- GitHub Actions workflow running on PRs that touch prompts/, src/, data/
- CLI entry point (scripts/evaluate.py) for CI usage
- Dockerfile for reproducible execution
- Merge blocked on CRITICAL regressions

## Out of Scope

- Web application, Streamlit dashboard, user accounts, hosted service
- Real-time production monitoring — this is a pre-merge gate, not an APM
- Dataset generation without human verification — every case stays hand-approved
