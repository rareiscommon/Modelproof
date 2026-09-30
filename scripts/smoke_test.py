"""
Smoke test for the email classifier.
"""
import json
import yaml
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from schemas import PromptConfig
from classifier import classify_email

def load_prompt(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return PromptConfig(**data)

def main():
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "v1.yaml"
    config = load_prompt(prompt_path)

    emails = [
        "Hello, I was billed twice for invoice #12345 last week. Please remove the duplicate charge.",
        "The website is showing a 500 error whenever I try to submit a payment.",
        "I want to update my billing address and also find out why my login is slow sometimes.",
    ]

    for i, email in enumerate(emails, 1):
        try:
            result = classify_email(email, config)
            print(json.dumps(result.model_dump(), indent=2))
        except Exception as e:
            print(f"Error classifying email {i}: {e}")

if __name__ == "__main__":
    main()
