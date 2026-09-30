"""
Classifier for customer support emails using Groq OpenAI compatible API.
"""
import os
import time
import json
from typing import Any

import openai
from dotenv import load_dotenv

load_dotenv()

from schemas import PromptConfig, EmailClassification, ClassificationError, ConfigurationError


def classify_email(email_text: str, prompt_config: PromptConfig) -> EmailClassification:
    """
    Classify an email using a versioned prompt config.

    Few-shot injection mechanism:
    - system prompt first
    - each few-shot example as a user/assistant message pair
    - actual email as final user message

    The function enforces JSON output via response_format and validates with Pydantic.
    Retries once on 429 or 5xx.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ConfigurationError("GROQ_API_KEY environment variable is not set")

    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": prompt_config.system_prompt}
    ]

    for ex in prompt_config.few_shot_examples:
        user_msg = ex.get("input", "")
        # Build output string from example output dict
        out = ex.get("output", {})
        if isinstance(out, dict):
            assistant_content = f"category: {out.get('category')}\nsummary: {out.get('summary')}"
        else:
            assistant_content = str(out)
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_content})

    messages.append({"role": "user", "content": email_text})

    attempt = 0
    last_error: Exception | None = None
    while attempt < 2:
        try:
            resp = client.chat.completions.create(
                model=prompt_config.model_name,
                messages=messages,
                temperature=prompt_config.temperature,
                response_format={"type": "json_object"},
            )
            content = resp.choices[0].message.content
            try:
                data = json.loads(content)
                classification = EmailClassification(**data)
                return classification
            except Exception as e:
                raise ClassificationError(f"Failed to parse classification: {e}. Raw response: {content}")
        except (openai.APIStatusError, openai.APIConnectionError) as e:
            status = getattr(e, "status_code", None)
            if status in (429, 500, 502, 503, 504):
                attempt += 1
                if attempt < 2:
                    time.sleep(2)
                    last_error = e
                    continue
            raise ClassificationError(f"Groq API error {status}: {e}")
        except Exception as e:
            raise ClassificationError(f"Classification failed: {e}")

    raise ClassificationError(f"Groq API failed after retry: {last_error}")
