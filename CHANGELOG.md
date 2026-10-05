# Changelog

All notable changes to Modelproof will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] — 2026-10-05

### Added
- LLM-as-judge scoring for summary relevance (1–5 rating)
- Baseline comparison with regression/improvement diffing
- Statistical thresholds: WARNING at 3% drop, CRITICAL at 8%
- Static HTML evaluation report
- Slack alerting with structured payload and color-coded status
- Drift detection: 7-run rolling average compared against fixed baseline
- Run snapshot storage with FIFO rotation
- GitHub Actions CI workflow that runs evaluation on every PR
- Dockerfile for containerized evaluation
- 34 new tests (44 total passing)

### Changed
- JSON output is now single-line for CI parsing
- All GitHub Action versions bumped to fix Node 20 deprecation

### Fixed
- `.env.example` placeholder values

## [0.1.0] — 2026-10-01

### Added
- Customer support email classifier with versioned prompts
- `PromptConfig` Pydantic model and `EmailClassification` schema
- Groq OpenAI-compatible provider integration with JSON-mode enforcement and retry
- Prompt `v1.yaml` with system prompt and few-shot examples
- Smoke test script with 3 sample emails
- `requirements.txt` with pinned dependencies
- Golden dataset v1 with 15 hand-verified test cases
- `data/manifest.json` for dataset versioning
- Baseline run `baseline_run_001.json` at 86.7% accuracy

