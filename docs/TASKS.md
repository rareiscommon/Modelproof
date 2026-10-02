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
- [ ] Implement evaluation runner
- [ ] Compute category accuracy and summary similarity
- [ ] Generate static HTML report
- [ ] Add CLI entry point

## Phase 4 — Regression Detection
- [ ] Baseline storage and comparison
- [ ] Configurable thresholds
- [ ] Pass/fail determination

## Phase 5 — Notifications
- [ ] Slack alert formatting
- [ ] GitHub PR comment generation

## Phase 6 — CI Integration
- [ ] GitHub Actions example workflow
- [ ] Documentation for CI usage

## Documentation Retrofit
- [x] ROADMAP.md
- [x] CHANGELOG.md
- [x] ARCHITECTURE.md
- [x] DECISIONS.md
- [x] docs/PRD.md
- [x] docs/RULES.md
- [x] docs/MEMORY.md
- [ ] docs/TEST_PLAN.md
- [ ] docs/SECURITY.md
- [ ] docs/DESIGN.md classification
