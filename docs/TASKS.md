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
- [x] src/run_store.py — atomic snapshot write, FIFO rotation (7 max)
- [x] src/drift.py — rolling 7-run avg vs fixed baseline
- [x] src/alerter.py — Slack webhook with color-coded payload
- [x] scripts/evaluate.py wired: drift → save → alert
- [x] 34 tests passing


## Phase 5 — CI/CD + Docker
- [x] .github/workflows/eval.yml — GitHub Actions workflow
- [x] Trigger on PRs that modify prompts/ or src/
- [x] Post pass/fail summary as PR comment
- [x] Block merge on CRITICAL regressions
- [x] Dockerfile for containerized eval
- [x] GROQ_API_KEY secret configured in repo settings
- [x] Workflow validated with real PR — green checkmark

## Phase 6 — Polish
- [x] Bump action versions (Node 20 deprecation fix)
- [x] CHANGELOG v0.5.0 entry
- [x] Update README status to Phase 5 complete
- [ ] Add architecture diagram to README
- [ ] Write blog-post section in README
- [ ] Record Loom walkthrough
- [ ] Final repository hygiene pass
- [ ] Make repository public

## Backlog
- [ ] Expand golden dataset to 60-80 cases
- [ ] Add latency and token usage metrics to report
- [ ] Per-model A/B evaluation (run same dataset against 2 models)
