# Product Requirements Document — Modelproof

## Product Objective
Detect quality regressions in LLM-powered features before bad outputs reach users, via a CLI-first regression detection system with prompt versioning and golden datasets.

## Problem Statement
LLM features degrade silently when prompts or models change. Teams lack cheap, repeatable regression tests for LLM outputs.

## Users
- Developers integrating LLM features
- ML engineers managing prompts
- CI/CD maintainers

## Scope
### In Scope
- Prompt versioning via YAML
- Customer support email classifier as reference implementation
- Golden dataset creation workflow with human verification gate
- CLI tool for evaluation
- Static HTML report generation
- Slack alert with headline metrics
- GitHub PR comment pass/fail summary

### Out of Scope
- Web application
- Streamlit dashboard
- User accounts
- Hosted service
- Evaluation engine, scoring, CI integration are Phase 3+

## Functional Requirements
1. PromptConfig loads from YAML with version_id, system_prompt, few_shot_examples, model_name, temperature.
2. classify_email(email_text, prompt_config) returns EmailClassification with category and summary.
3. JSON output enforced via API response_format and Pydantic validation.
4. Golden dataset stored as JSON with verification fields.
5. Manifest tracks version metadata and counts.
6. Smoke test script runs end-to-end classification.

## Non-Functional Requirements
- Python 3.11 compatible
- API key via environment variable, never hardcoded
- Retry once on transient errors
- Deterministic evaluation given same dataset and prompt

## Acceptance Criteria
- Classifier returns valid JSON for all sample emails
- Prompt can be changed by editing YAML only
- Golden dataset cases have verified field enforced
- Smoke test prints JSON for 3 samples without error

## Success Metrics
- Category accuracy baseline established
- Time to detect regression < CI run time

## Constraints
- Use Groq OpenAI-compatible API
- No UI, CLI only
- Developer tool, no auth

## Assumptions
- Golden dataset will be human-verified
- Prompts are small enough for YAML storage

## Risks
- Provider rate limits
- Prompt drift without dataset coverage
