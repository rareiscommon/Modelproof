# Roadmap

## Current Status
Phase 1 and Phase 2 complete.
- Phase 1: Customer support email classifier with prompt versioning, typed interface, Groq provider, smoke test.
- Phase 2: Golden dataset v1 with 15 hand-verified test cases. Baseline accuracy 86.7% on golden set.

## Phase 3 — Evaluation Engine
- Implement evaluation runner that loads golden dataset and PromptConfig, runs classifier, compares category and summary.
- Compute metrics: category accuracy, summary similarity, regression delta vs baseline.
- Output static HTML report written to disk.
- Acceptance: Reproducible metric run from CLI with same inputs producing same outputs.

## Phase 4 — Regression Detection
- Baseline storage and comparison.
- Detect regressions when prompt or model changes.
- Fail criteria configurable thresholds.

## Phase 5 — Notifications
- Slack alert with headline metrics + link to report.
- GitHub PR comment with pass/fail summary.

## Phase 6 — CI Integration
- GitHub Actions workflow example.
- CLI entry point for CI usage.

## Out of Scope
- Web application, Streamlit dashboard, user accounts, hosted service.
