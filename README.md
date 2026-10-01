# Modelproof

**Model regression detection for LLM-powered features.**

A CI/CD pipeline that detects quality regressions whenever prompts or models change, before bad outputs reach users.

> **Status:** Phase 1 of 6 complete. The classifier works. Regression detection, evaluation engine, Slack alerts, and CI integration are on the roadmap — not yet implemented.

## What This Does Today

A customer support email classifier that:
- Takes raw email text as input
- Returns structured JSON with a `category` (`billing`, `technical`, `account`, `general`) and a one-sentence `summary`
- Loads its prompt from a versioned YAML file (not hardcoded)
- Calls Groq's OpenAI-compatible API

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) for dependency management
- A free [Groq API key](https://console.groq.com/keys) (starts with `gsk_`)

## Setup

```bash
# 1. Create and activate a virtual environment
uv venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\activate           # Windows

# 2. Install dependencies
uv pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env
# Edit .env and paste your Groq key
