import time

import litellm
from google.genai import types
from google.genai.types import ThinkingConfig
from pydantic import BaseModel
from smolagents import CodeAgent, VisitWebpageTool, WebSearchTool

from agent.prompts import formatter_system_prompt, system_prompt
from agent.tools import (
    ChessBestMove,
    CodeExecutionTool,
    DownloadFile,
    ReadExcelFileBytes,
    TranscribeAudioBytes,
    TranscribeYoutubeVideo,
    UnderstandImageBytes,
    WikipediaSearchTool,
)
from agent.utils import gemini_client, gemini_model_liteLLM

# --- Constants ---

litellm.drop_params = True


class final_answer(BaseModel):
    answer: str


def lowercase_if_comma(s):
    if s.count(",") > 2:
        return s.lower()
    return s


def delay_8_seconds(
    agent: CodeAgent,
) -> bool:
    """
    Delay execution for 8 seconds.
    """
    time.sleep(8)
    return True


STEP_CALLBACKS = [delay_8_seconds]


# --- Basic Agent Definition ---
# ----- THIS IS WERE YOU CAN BUILD WHAT YOU WANT ------
class BasicAgent:
    def __init__(self, model="gemini-2.5-flash-preview-05-20", if_sleep=True):
        self.model = model
        self.client = gemini_client()
        transcribe_youtube_video = TranscribeYoutubeVideo()
        transcribe_audio_bytes = TranscribeAudioBytes()
        search_tool = WebSearchTool()
        visit_web_tool = VisitWebpageTool()
        download_file_tool = DownloadFile()
        read_excel_file_tool = ReadExcelFileBytes()
        understand_image_bytes = UnderstandImageBytes()
        code_execution_tool = CodeExecutionTool()
        wiki_retriever = WikipediaSearchTool()
        chess_best_move = ChessBestMove()
        model = gemini_model_liteLLM(self.model)

        if if_sleep:
            STEP_CALLBACKS = [delay_8_seconds]
        else:
            STEP_CALLBACKS = None
        self.code_agent = CodeAgent(
            tools=[
                transcribe_youtube_video,
                transcribe_audio_bytes,
                search_tool,
                visit_web_tool,
                download_file_tool,
                read_excel_file_tool,
                understand_image_bytes,
                code_execution_tool,
                wiki_retriever,
                chess_best_move,
            ],
            model=model,
            additional_authorized_imports=["pandas"],
            step_callbacks=STEP_CALLBACKS,
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
            # let model decide the budget
            thinking_config = ThinkingConfig()
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        # Run the agent to find the best catering service

        answer = self.code_agent.run(
            f"{system_prompt}\nTask id: {task_id}, Question: {question}"
        )
        print(f"Agent found answer: {answer}")
        response = client.models.generate_content(
            model=model,
            contents=f"Here is the provided question: {question}, infomation or answer: {str(answer)} \n Now, resposne with the answer that followed the rules.",
            config=types.GenerateContentConfig(
                system_instruction=formatter_system_prompt,
                response_mime_type="application/json",
                temperature=0.0,
                response_schema=final_answer,
                thinking_config=thinking_config,
                top_p=0.95,
                seed=42,
            ),
        )
        print(f"Final answer after formatter by model: {response.parsed.answer}")
        result = lowercase_if_comma(response.parsed.answer)

        return result
