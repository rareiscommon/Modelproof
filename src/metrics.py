"""
Metric calculations for Modelproof evaluation.
"""
import os
import json
from typing import List, Dict
from collections import defaultdict

import openai
from dotenv import load_dotenv

from src.schemas import ClassificationError

load_dotenv()


def category_accuracy(results: List[Dict]) -> float:
    correct = sum(1 for r in results if r.get("match"))
    total = len(results)
    return correct / total if total else 0.0


def per_category_accuracy(results: List[Dict]) -> Dict[str, float]:
    counts = defaultdict(lambda: [0, 0])
    for r in results:
        cat = r.get("expected")
        counts[cat][0] += 1
        if r.get("match"):
            counts[cat][1] += 1
    return {cat: (correct / total if total else 0.0) for cat, (total, correct) in counts.items()}


def _make_judge_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ClassificationError("GROQ_API_KEY environment variable is not set")
    return openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )


def llm_judge_summary_score(predicted_summary: str, expected_summary: str, model_name: str = "openai/gpt-oss-120b") -> int:
    """
    Score summary relevance 1-5 using LLM-as-judge via Groq API.
    Returns integer 1-5.
    Raises ClassificationError on parse failure.
    """
    client = _make_judge_client()
    prompt = (
        "You are evaluating summary quality. "
        "Rate 1-5 how well the PREDICTED summary captures the same information as the EXPECTED summary. "
        "Return JSON with key 'score' containing the integer."
    )
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"EXPECTED: {expected_summary}\nPREDICTED: {predicted_summary}"}
    ]
    resp = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    try:
        data = json.loads(content)
        # Expect {"score": N} or just N
        score = data.get("score") if isinstance(data, dict) else data
        score = int(score)
        if not 1 <= score <= 5:
            raise ValueError
        return score
    except Exception as e:
        raise ClassificationError(f"Failed to parse judge score: {e}. Raw: {content}")


def average_judge_score(scores: List[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0