import os

from google import genai
from smolagents import LiteLLMModel


def gemini_model_liteLLM(
    model: str,
    response_format=None,
) -> LiteLLMModel:
    """model for example, gemini-2.0-flash"""
    return LiteLLMModel(
        model_id=f"gemini/{model}",
        response_format=response_format,
        thinking={"type": "enabled", "budget_tokens": 0},
    )


def gemini_client():
    client = genai.Client()
    return client
