from smolagents import LiteLLMModel
from smolagents import OpenAIServerModel
import os


def gemini_model_liteLLM(model: str, response_format=None) -> LiteLLMModel:
    """model for example, gemini-2.0-flash"""
    return LiteLLMModel(model_id=f"gemini/{model}", response_format=response_format)
