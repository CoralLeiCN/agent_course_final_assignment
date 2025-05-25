from pydantic import BaseModel
from smolagents import CodeAgent, WebSearchTool

from agent.prompts import system_prompt
from agent.tools import TranscribeYoutubeVideo
from utils import gemini_model_liteLLM

# --- Constants ---


class final_answer(BaseModel):
    answer: str


# --- Basic Agent Definition ---
# ----- THIS IS WERE YOU CAN BUILD WHAT YOU WANT ------
class BasicAgent:
    def __init__(self):
        self.model = gemini_model_liteLLM(
            "gemini-2.0-flash", response_format=final_answer
        )
        # Example model, replace with your own
        transcribe_youtube_video = TranscribeYoutubeVideo()
        search_tool = WebSearchTool()  # (Keep Constants as is)

        model = gemini_model_liteLLM("gemini-2.0-flash")
        self.code_agent = CodeAgent(
            tools=[transcribe_youtube_video, search_tool], model=model, max_steps=10
        )

        print("BasicAgent initialized.")

    def __call__(self, question: str) -> str:
        print(f"Agent received question (first 50 chars): {question[:50]}...")
        # Run the agent to find the best catering service
        final_answer = self.code_agent.run(f"{system_prompt} \nQuestion: {question}")
        return final_answer
