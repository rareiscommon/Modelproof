# Project Rules

## Coding Standards
- Python 3.11 syntax only
- Type hints on public functions
- Pydantic models for all data contracts
- No secrets in code; use os.getenv
- Load .env via python-dotenv at module import

## File Layout
- src/ for library code
- prompts/ for versioned YAML prompts
- data/ for golden datasets and manifests
- scripts/ for CLI and smoke tests
- docs/ for documentation

## Prompt Changes
- Never hardcode prompts in classifier.py
- Always store prompts in prompts/*.yaml
- Increment version_id on change
- Update manifest when dataset changes

## Dataset Verification Gate
- Test cases must have source and verified fields
- verified values: pending, edited, authored
- source values: ai-drafted, ai-drafted-human-edited, human-authored
- Do not commit dataset with any verified='pending'

## Agent Behavior
- Read RULES.md before modifying repository
- Read DESIGN.md before modifying user-facing code [N/A for CLI]
- Update MEMORY.md at end of each session
- Update TASKS.md as work completes
- Report files changed, tests executed, remaining issues

## Testing
- Smoke test must pass before any change
- New features require test cases in golden dataset

## Security
- Never commit .env
- Never log API keys
- Validate all LLM outputs with Pydantic
