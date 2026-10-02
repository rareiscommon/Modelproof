# Evaluation Specification

## Metrics
- Category accuracy: proportion of cases where predicted category matches expected
- Per-category accuracy: breakdown by billing, technical, account, general
- Summary scoring: LLM-as-judge rating 1-5 for relevance and factual consistency
- Baseline delta: current accuracy minus baseline accuracy

## Thresholds
- WARNING if overall accuracy delta < -3%
- CRITICAL if overall accuracy delta < -8%
- Status labels: PASS, WARNING, CRITICAL

## Baseline Comparison
Baseline file: data/baseline_run_001.json
Compare per-case pass/fail, report regressions and improvements

## Report
Static HTML report with status label, accuracy numbers, delta, per-category breakdown, regressions and improvements list

## Judge Model
Default judge model same as classifier model. Can be overridden via config.

## Reproducibility
Evaluation run records prompt_version, model, run timestamp, dataset version
