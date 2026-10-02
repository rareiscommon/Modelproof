# Project Memory

## Current State
- Phase 1 complete: classifier with prompt versioning, Groq provider, smoke test
- Phase 2 complete: golden dataset v1 with 15 hand-verified cases, baseline accuracy 86.7%
- Baseline run stored in data/baseline_run_001.json
- Missing baseline documentation set being retrofitted

## Recent Changes
- 2026-10-01: Created ROADMAP.md, CHANGELOG.md, ARCHITECTURE.md, DECISIONS.md
- Docs created: PRD.md, RULES.md, TASKS.md, MEMORY.md, TEST_PLAN.md, SECURITY.md

## Known Issues
- Classifier schemas.py model_name default is openai/gpt-oss-120b but prompt v1 specifies llama-3.3-70b-versatile in original spec. Verify alignment.
- Golden dataset difficulty distribution not perfectly balanced after human review.

## Next Steps
- Complete docs baseline set
- Proceed to Stage 6 PRD specification if required
- Stage 3 dataset expansion to 60-80 cases pending human review
