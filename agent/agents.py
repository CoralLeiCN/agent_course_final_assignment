from google import genai
from google.genai import types
from pydantic import BaseModel
from smolagents import CodeAgent, WebSearchTool, VisitWebpageTool

import time
from agent.prompts import system_prompt
from agent.tools import TranscribeYoutubeVideo, DownloadFile, ReadExcelFileBytes
from agent.utils import gemini_client, gemini_model_liteLLM
from google.genai.types import GenerateContentConfig, ThinkingConfig

# --- Constants ---


class final_answer(BaseModel):
    answer: str


# --- Basic Agent Definition ---
# ----- THIS IS WERE YOU CAN BUILD WHAT YOU WANT ------
class BasicAgent:
    def __init__(self, sleep=60):
        self.client = gemini_client()
        self.sleep = sleep
        transcribe_youtube_video = TranscribeYoutubeVideo()
        search_tool = WebSearchTool()
        visit_web_tool = VisitWebpageTool()
        download_file_tool = DownloadFile()
        read_excel_file_tool = ReadExcelFileBytes()
        model = gemini_model_liteLLM("gemini-2.5-flash-preview-05-20")
        self.code_agent = CodeAgent(
            tools=[
                transcribe_youtube_video,
                search_tool,
                visit_web_tool,
                download_file_tool,
                read_excel_file_tool,
            ],
            model=model,
            max_steps=15,
        )

        print("BasicAgent initialized.")

    def __call__(self, task_id, question: str) -> str:
        client = self.client
        time.sleep(self.sleep)  # Avoid rate limiting issues
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        # Run the agent to find the best catering service
        answer = self.code_agent.run(f"Task id: {task_id}, Question: {question}")
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=f"Question: {question}, Answer: {str(answer)}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=final_answer,
                thinking_config=ThinkingConfig(
                    thinking_budget=0,  # Use `0` to turn off thinking
                ),
            ),
        )
        print(response)

        return response.parsed.answer
