# Tasks

## Phase 1 — Classifier
- [x] Define PromptConfig Pydantic model
- [x] Define EmailClassification schema
- [x] Implement classify_email with Groq provider
- [x] Add JSON enforcement and Pydantic validation
- [x] Add retry logic for 429/5xx
- [x] Load prompts from YAML
- [x] Create prompts/v1.yaml
- [x] Create smoke test script
- [x] Pin requirements

## Phase 2 — Golden Dataset
- [x] Design dataset schema with verified/source fields
- [x] Create data/ directory structure
- [x] Draft 15 sample cases
- [x] Human review and verification
- [x] Create manifest.json
- [x] Run baseline evaluation, record 86.7% accuracy

## Phase 3 — Evaluation Engine
- [x] Implement evaluation runner (src/evaluator.py)
- [x] Compute category accuracy and LLM-as-judge summary scoring (src/metrics.py)
- [x] Add baseline comparison with regression/improvement diff
- [x] Add statistical thresholds (--warning-threshold, --critical-threshold)
- [x] Generate static HTML report (src/reporter.py)
- [x] Add CLI entry point (scripts/evaluate.py)
- [x] Write evaluation spec (docs/evaluation_spec.md)
- [x] Write unit tests (tests/test_evaluator.py — 4 passing)
- [x] First real run: 86.67% accuracy, delta 0.00%, PASS

## Phase 4 — Slack Alerts + Drift Detection
- [ ] Wire Slack incoming webhook
- [ ] Send structured alert with PASS/WARNING/CRITICAL status
- [ ] Include headline metrics and link to HTML report
- [ ] Implement 7-run rolling average for drift detection
- [ ] Fire slow-drift warning when rolling average drops below threshold
- [ ] Add tests for alert formatting and drift logic

## Phase 5 — CI/CD + Docker
- [ ] Create .github/workflows/eval.yml
- [ ] Trigger eval on PRs that modify /prompts
- [ ] Post pass/fail summary as PR comment
- [ ] Block merge on CRITICAL regressions
- [ ] Write Dockerfile for eval runner
- [ ] Test container locally

## Phase 6 — Polish
- [ ] Write blog post or README section explaining the problem
- [ ] Record 3-minute Loom walkthrough
- [ ] Add architecture diagram to README
- [ ] Final repository hygiene pass
- [ ] Make repo public

## Backlog
- [ ] Expand golden dataset to 60-80 cases
- [ ] Add latency and token usage metrics to report
- [ ] Per-model A/B evaluation (run same dataset against 2 models)
