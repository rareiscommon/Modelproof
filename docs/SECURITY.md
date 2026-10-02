# Security

## Threat Model Summary
Assets: API keys, golden dataset, prompt files, classifier code
Actors: developers, CI systems, LLM provider
Trust boundaries: local dev machine -> Groq API, repo -> public

## Secrets Policy
- GROQ_API_KEY stored in .env, gitignored
- .env.example committed with placeholder only
- Never log API keys or include in error messages
- Secret scanning on repository

## Authentication Model
- No user authentication; CLI tool for developers
- API access controlled by Groq API key only

## Input Validation
- Email text passed to LLM without execution
- LLM output validated with Pydantic EmailClassification
- Category restricted to Literal set
- JSON output enforced via response_format

## Trust Boundaries
- LLM output is untrusted until validated
- Prompt files are trusted configuration, subject to version control
- Dataset is trusted ground truth after human verification

## Residual Risks
- Prompt injection via email text could influence classification
- Mitigation: classification is limited scope, no tool use
- Provider data retention per Groq policy
- API key leakage via logs or commits

## Security Assumptions
- Developers protect .env files
- Groq API is trusted for inference
- Golden dataset contains no PII

## Compliance
- No PII in code or public dataset
- Dataset cases are synthetic or anonymized
