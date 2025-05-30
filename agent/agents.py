import time

import litellm
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, ThinkingConfig
from pydantic import BaseModel
from smolagents import CodeAgent, VisitWebpageTool, WebSearchTool

from agent.prompts import system_prompt
from agent.tools import (
    DownloadFile,
    ReadExcelFileBytes,
    TranscribeAudioBytes,
    TranscribeYoutubeVideo,
)
from agent.utils import gemini_client, gemini_model_liteLLM

# --- Constants ---

litellm.drop_params = True


class final_answer(BaseModel):
    answer: str


# add function to sleep 10 second to avoid rate limiting issues
def delay(seconds: int = 10):
    """Delay execution for a specified number of seconds."""
    time.sleep(seconds)


# --- Basic Agent Definition ---
# ----- THIS IS WERE YOU CAN BUILD WHAT YOU WANT ------
class BasicAgent:
    def __init__(self, model="gemini-2.5-flash-preview-05-20", sleep=10):
        self.model = model
        self.client = gemini_client()
        self.sleep = sleep
        transcribe_youtube_video = TranscribeYoutubeVideo()
        transcribe_audio_bytes = TranscribeAudioBytes()
        search_tool = WebSearchTool()
        visit_web_tool = VisitWebpageTool()
        download_file_tool = DownloadFile()
        read_excel_file_tool = ReadExcelFileBytes()

        model = gemini_model_liteLLM(self.model)
        self.code_agent = CodeAgent(
            tools=[
                transcribe_youtube_video,
                transcribe_audio_bytes,
                search_tool,
                visit_web_tool,
                download_file_tool,
                read_excel_file_tool,
            ],
            model=model,
            step_callbacks=time.sleep(self.sleep),
            max_steps=15,
        )

        print("BasicAgent initialized.")

    def __call__(self, task_id, question: str) -> str:
        client = self.client
        model = self.model
        # if not support thinking features, like flash 2.0, set thinking_config to None
        if model.startswith("gemini-2.0-flash"):
            thinking_config = None
        else:
            thinking_config = ThinkingConfig(
                thinking_budget=0,  # Use `0` to turn off thinking
            )
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        # Run the agent to find the best catering service

        answer = self.code_agent.run(f"Task id: {task_id}, Question: {question}")
        response = client.models.generate_content(
            model=model,
            contents=f"Question: {question}, Answer: {str(answer)}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=final_answer,
                thinking_config=thinking_config,
            ),
        )
        print(response)

        return response.parsed.answer
