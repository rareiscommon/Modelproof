# Project Memory

## Current State
- Phase 1 complete: classifier with prompt versioning, Groq provider, smoke test
- Phase 2 complete: golden dataset v1 with 15 hand-verified cases, baseline accuracy 86.7%
- Phase 3 complete: evaluation engine with metrics, baseline diff, thresholds, HTML report
- Phase 4 complete: Slack alerts, drift detection, 7-run rolling window, 34 tests passing
- Phase 5 complete: CI/CD workflow, Dockerfile, GitHub Actions validated with a real merged PR (green checkmark)
- Baseline documentation set complete (README, ROADMAP, CHANGELOG, ARCHITECTURE, DECISIONS, PRD, RULES, TASKS, MEMORY, TEST_PLAN, SECURITY)
- Security scan complete: pip-audit, gitleaks, bandit, semgrep, trivy — all clean
- Dependency lock file added: requirements.lock.txt

## Recent Changes
- 2026-10-01: Retrofit baseline docs created (11 files)
- 2026-10-02: Security stack installed and initial scan committed
- 2026-10-02: Phase 3 evaluation engine built and tested
  - src/metrics.py, src/evaluator.py, src/reporter.py
  - scripts/evaluate.py with --dataset, --prompt, --baseline, --warning-threshold, --critical-threshold, --output
  - tests/test_evaluator.py — 4 tests, all passing
  - First real run: 86.67% accuracy, delta 0.00%, status PASS
  - HTML report at report.html

## Known Issues
- Golden dataset difficulty distribution is 7 easy / 4 medium / 4 hard (deliberately not forced to 5/5/5)
- Two hard cases (gd-0012, gd-0014) mis-classify, expected given difficulty tag
- Rate-limit failover can trigger session-manager bug on long agent turns; workaround is single-model pinning and small turns

## Next Steps
- Phase 4: Slack alerts + drift detection (7-run rolling average)
- Phase 5: CI/CD integration (GitHub Actions) + Dockerfile
- Phase 6: Polish (Loom walkthrough, blog post)

