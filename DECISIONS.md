# Decisions

## ADR-001 — Prompt Versioning via YAML
**Status:** Accepted
**Date:** 2026-09-30
**Context:** Prompts need to be changed without code deploys.
**Decision:** Store prompts as versioned YAML files under prompts/ with version_id, timestamp, system_prompt, few_shot_examples.
**Consequences:** Enables prompt A/B testing and regression tracking. Requires loader in classifier.

## ADR-002 — Groq OpenAI-compatible Provider
**Status:** Accepted
**Date:** 2026-09-30
**Context:** Need free, fast inference for development.
**Decision:** Use Groq at https://api.groq.com/openai/v1 with model llama-3.3-70b-versatile, key via GROQ_API_KEY.
**Consequences:** Low cost, but provider lock-in risk. Mitigated by OpenAI SDK abstraction.

## ADR-003 — JSON Enforcement via response_format
**Status:** Accepted
**Date:** 2026-09-30
**Context:** LLM output must be machine parseable.
**Decision:** Use response_format={"type":"json_object"} and Pydantic validation.
**Consequences:** Fewer parse failures, explicit errors on schema mismatch.

## ADR-004 — Golden Dataset Verification Gate
**Status:** Accepted
**Date:** 2026-10-01
**Context:** Need human-verified ground truth.
**Decision:** Test cases have source and verified fields. Dataset must not be committed until verified != 'pending'.
**Consequences:** Slower dataset growth but ensures quality.

## ADR-005 — No UI, CLI Only
**Status:** Accepted
**Date:** 2026-10-01
**Context:** Target audience is developers in CI.
**Decision:** CLI tool, static HTML report, Slack alert, GitHub PR comment. No web app.
**Consequences:** Simpler operations, no auth.

## ADR-006 — Pydantic v2 Schemas
**Status:** Accepted
**Date:** 2026-09-30
**Context:** Need typed interface for prompts and outputs.
**Decision:** Use Pydantic BaseModel for PromptConfig and EmailClassification.
**Consequences:** Runtime validation, clear errors.

## ADR-007 — Retry Once on 429/5xx
**Status:** Accepted
**Date:** 2026-09-30
**Context:** Transient API failures.
**Decision:** Retry once after 2s sleep on 429 or 5xx, then raise ClassificationError.
**Consequences:** Improves reliability without long waits.
