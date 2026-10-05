# Changelog

All notable changes to Modelproof will be documented in this file.

## [0.5.0] — 2026-10-05

### Added
- LLM-as-judge scoring for summary relevance (1-5 rating)
- Baseline comparison with regression/improvement diffing
- Statistical thresholds (WARNING at 3% drop, CRITICAL at 8%)
- Static HTML evaluation report
- Slack alerting with structured payload and color-coded status
- Drift detection (7-run rolling average vs fixed baseline)
- Run snapshot storage with FIFO rotation
- GitHub Actions CI workflow — runs eval on every PR
- Dockerfile for containerized evaluation
- 34 new tests (44 total passing)

### Changed
- JSON output is now single-line for CI parsing
- All GitHub Action versions bumped to fix Node 20 deprecation

### Fixed
- `meta.migrations.utilityModelSeparation` marker causing startup failures
- `.env.example` placeholder values

## [0.1.0] - 2026-10-01
### Added
- Phase 1: Customer support email classifier with prompt versioning.
- PromptConfig Pydantic model and EmailClassification schema.
- Groq OpenAI-compatible provider integration with JSON enforcement and retry.
- Prompt v1.yaml with system prompt and few-shot examples.
- Smoke test script with 3 sample emails.
- requirements.txt with pinned dependencies.
- Phase 2: Golden dataset v1 with 15 hand-verified test cases.
- data/manifest.json for dataset versioning.
- Baseline run baseline_run_001.json with 86.7% accuracy.

### Changed
- N/A

### Removed
- N/A
