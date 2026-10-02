# Test Plan

## What "Working" Means
Classifier returns valid EmailClassification for any input email text using a valid PromptConfig, with category in allowed set and summary as one sentence.

## Acceptance Criteria per Feature

### Prompt Loading
- PromptConfig loads from YAML without error
- Missing fields raise ValidationError

### Classification
- Output has category in billing/technical/account/general
- Summary is non-empty string
- JSON output enforced via response_format
- Pydantic validation rejects malformed responses

### Error Handling
- Missing GROQ_API_KEY raises ConfigurationError
- API 429/5xx triggers one retry after 2s
- Parse failure raises ClassificationError with raw response

### Golden Dataset
- Dataset cases have required fields: id, text, category, summary, difficulty, source, verified, verified_by, created
- Manifest counts match dataset length
- No case committed with verified='pending'

## Edge Cases
- Very short email
- Typos and broken grammar
- Ambiguous mixed-topic emails
- Angry tone
- Ticket references
- Empty input
- Very long email

## Test Scenarios
1. Smoke test with 3 sample emails prints JSON
2. Load prompt v1 and classify sample from few-shot
3. Simulate missing API key
4. Simulate parse error
5. Validate dataset schema for all cases

## Manual Test Steps
1. cp .env.example .env and set GROQ_API_KEY
2. python scripts/smoke_test.py
3. Verify output JSON schema matches EmailClassification
4. Compare classifier output to golden dataset expected category
