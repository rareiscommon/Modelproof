from pydantic import BaseModel, Field
from typing import List, Literal


class PromptConfig(BaseModel):
    version_id: str
    system_prompt: str
    few_shot_examples: List[dict]
    model_name: str = "openai/gpt-oss-120b"
    temperature: float = 0.1


class EmailClassification(BaseModel):
    category: Literal["billing", "technical", "account", "general"]
    summary: str


class ClassificationError(Exception):
    pass


class ConfigurationError(Exception):
    pass
