from smolagents import LiteLLMModel
from smolagents import OpenAIServerModel
import os


def gemini_model_liteLLM(model: str) -> LiteLLMModel:
    """model for example, gemini-2.0-flash"""
    return LiteLLMModel(model_id=f"gemini/{model}")


def gemini_model_OpenAIServer(model: str) -> OpenAIServerModel:
    model = OpenAIServerModel(
        model_id=model,
        api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.environ["GOOGLE_API_KEY"],
    )
    return model
