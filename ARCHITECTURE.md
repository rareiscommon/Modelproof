# Architecture

## Overview
Modelproof is a CLI-first developer tool for detecting regressions in LLM-powered features. Phase 1 implements a customer support email classifier with prompt versioning. Phase 2 adds a hand-verified golden dataset for evaluation.

## Components

### Core Library
- `src/schemas.py`
  PromptConfig: version_id, system_prompt, few_shot_examples, model_name, temperature
  EmailClassification: category Literal, summary str
  Custom exceptions ClassificationError, ConfigurationError
- `src/classifier.py`
  classify_email(email_text: str, prompt_config: PromptConfig) -> EmailClassification
  Loads GROQ_API_KEY from environment via python-dotenv
  Builds messages: system prompt + few-shot user/assistant pairs + final user message
  Calls Groq OpenAI-compatible API with response_format json_object
  Validates response with Pydantic, retries once on 429/5xx

### Prompt Versioning
- `prompts/v1.yaml`
  version_id, timestamp, system_prompt, few_shot_examples
  Classifier loads prompt from YAML, never hardcoded

### Data
- `data/golden_dataset_v1.json`
  Hand-verified test cases with id, text, category, summary, difficulty, tags, source, verified, verified_by, created, notes
- `data/manifest.json`
  version_id, created_at, verified_at, num_cases, categories_counts, difficulty_counts, changelog
- `data/baseline_run_001.json`
  Baseline evaluation results

### CLI & Scripts
- `scripts/smoke_test.py`
  Loads prompt v1, runs 3 hardcoded emails, prints JSON results

## Data Flow
User email -> classify_email -> PromptConfig loaded from YAML -> messages constructed -> Groq API -> JSON parse -> Pydantic validation -> EmailClassification returned

## Technology Choices
- Python 3.11
- Pydantic v2 for typed schemas
- PyYAML for prompt versioning
- OpenAI SDK for Groq compatibility
- python-dotenv for config

## User Surfaces
- CLI tool
- Static HTML report written to disk
- Slack alert with headline metrics + link to report
- GitHub PR comment with pass/fail summary

No web application, no user accounts, no hosted service.
