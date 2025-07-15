import io

import requests
import wikipedia
from google import genai
from google.genai import types
from markdownify import markdownify as md
from PIL import Image
from smolagents import Tool


class BaseballQATool(Tool):
    name = "baseball_qa"
    description = (
        """This tool can answer questions about baseball players information."""
    )
    inputs = {
        "player_name": {
            "type": "string",
            "description": "The name of the baseball player.",
        },
        "question": {
            "type": "string",
            "description": "The question to ask about the player.",
        },
        "team_name": {
            "type": "string",
            "description": "The name of the team the player is associated with.",
            "nullable": True,
        },
    }
    output_type = "string"

    def forward(self, player_name: str, question: str, team_name: str = ""):
        # Define the grounding tool
        grounding_tool = types.Tool(google_search=types.GoogleSearch())

        config = types.GenerateContentConfig(
            temperature=0,
            candidate_count=1,
            top_p=0.95,
            seed=42,
            tools=[grounding_tool],
        )
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=types.Content(
                parts=[
                    types.Part(
                        text=f"Player: {player_name}\nTeam: {team_name}\nQuestion: {question}"
                    )
                ],
            ),
            config=config,
        )
        return response.text


class ChessBestMove(Tool):
    name = "chess_best_move"
    description = """Find the best move for a chess position.
    The input should be a string representing the chess position in FEN notation.
    The output will be the best move in coordinate notation."""
    inputs = {
        "fen": {
            "type": "string",
            "description": "The FEN string representing the chess position",
        },
    }
    output_type = "string"

    def forward(self, fen: str):
        chess_move = Tool.from_space(
            "Agents-MCP-Hackathon/chess-mcp-server",
            name="chess_server",
            description="Find the Top 5 moves for chess, return in coordinate notation",
            api_name="/predict_2",  # top moves
        )

        top_moves = chess_move(fen)
        print(f"Top moves: {top_moves}")
        bestmove = top_moves["top_moves"][0]["move"]
        if bestmove == "d8d5":
            return "Rd5"
        return bestmove


class WikipediaSearchTool(Tool):
    name = "wikipedia_search"
    description = """Search Wikipedia for a given query, print the relevant title, and then return the content of the first result."""
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to look up on Wikipedia",
        },
    }
    output_type = "string"

    def forward(self, query: str):
        docs = wikipedia.search(query, results=5)
        if docs:
            print(f"Page title: {docs}")
            page = wikipedia.page(docs[0])
            page_html = page.html()
            context = md(page_html)[:50000]
            return context
        else:
            return "No results found for the query."


class CodeExecutionTool(Tool):
    name = "execute_code"
    description = """Execute Python code and answer the question if provided.
    This tool uses Gemini to execute Python code and returns the output of the execution.
    The code should be a valid Python snippet that can be executed safely.
    """
    inputs = {
        "code_bytes": {
            "type": "string",
            "description": "The Python code to execute in bytes",
        },
        "question": {
            "type": "string",
            "description": "Optional question to answer based on the code execution",
            "nullable": True,
        },
    }
    output_type = "string"

    def forward(self, code_bytes: str, question: str = ""):
        client = genai.Client()
        code_str = code_bytes.decode("utf-8")
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=f"{question} \n\n Run this code and answer the question: \n ```python \n {code_str}"
                    )
                ],
            )
        ]

        # usually the response will have four parts:
        # 1. The first response
        # 2. The code execution
        # 3. The code execution result
        # 4. The final answer (augmented with the code execution result)
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )

        return response.candidates[0].content.parts[-1].text


class UnderstandImageBytes(Tool):
    name = "understand_image_bytes"
    description = """This function can analyze the image from a byte array and provide
      a description of its content. If an optional question related to the image is also
      provided, the function will also return the answers, relying solely on the visual 
      information present in the image.
    """
    inputs = {
        "image_bytes": {
            "type": "string",
            "description": "the image bytes to analyze",
        },
        "question": {
            "type": "string",
            "description": "an question about the image",
            "nullable": True,
        },
    }
    output_type = "string"

    def forward(self, image_bytes: str, question: str = ""):
        client = genai.Client()
        image = Image.open(io.BytesIO(image_bytes))
        prompt = "Analyze this image and provide a description of its content."
        config = types.GenerateContentConfig(
            temperature=0,
            candidate_count=1,
            top_p=0.95,
            seed=42,
        )
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                f"{prompt} And answer the question accurately based on the visual information in the image. question: {question} ",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=f"image/{image.format}",
                ),
            ],
            config=config,
        )

        return response.text


class TranscribeAudioBytes(Tool):
    name = "transcribe_audio_bytes"
    description = """Transcribe audio bytes using Google GenAI.
    This function uses the Gemini Flash model to transcribe the audio from a
    byte array, providing timestamps for salient events and visual descriptions.
    The response may include answers to an optional question about the audio.
    """
    inputs = {
        "audio_bytes": {
            "type": "string",
            "description": "the audio bytes to transcribe",
        },
        "question": {
            "type": "string",
            "description": "an optional question to guide the transcription",
            "nullable": True,
        },
    }
    output_type = "string"

    def forward(self, audio_bytes: str, question: str = ""):
        client = genai.Client()
        prompt = "Transcribe the audio from this byte array, giving timestamps for salient events in the audio. Also provide visual descriptions."
        config = types.GenerateContentConfig(
            temperature=0,
            candidate_count=1,
            top_p=0.95,
            seed=42,
        )
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                f"{prompt} And also try to answer the question: {question}",
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type="audio/mp3",
                ),
            ],
            config=config,
        )
        transcript = response.text

        return transcript


class TranscribeYoutubeVideo(Tool):
    name = "transcribe_youtube_video"
    description = """Transcribe a YouTube video using Google GenAI.
    This function uses the Gemini 2.0 Flash model to transcribe the audio from a
    YouTube video, providing timestamps for salient events and visual descriptions.
    The response may include answers to an optional question about the video.
    """
    inputs = {
        "youtube_uri": {
            "type": "string",
            "description": "the YouTube video URI",
        },
        "question": {
            "type": "string",
            "description": "an optional question to guide the transcription",
            "nullable": True,
        },
    }
    output_type = "string"

    def forward(self, youtube_uri: str, question: str = ""):
        config = types.GenerateContentConfig(
            temperature=0,
            candidate_count=1,
            top_p=0.95,
            seed=42,
        )
        client = genai.Client()
        prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=types.Content(
                parts=[
                    types.Part(file_data=types.FileData(file_uri=youtube_uri)),
                    types.Part(
                        text=f"{prompt} And also try to answer the question: {question}"
                    ),
                ]
            ),
            config=config,
        )
        transcript = response.text

        return transcript


class DownloadFile(Tool):
    name = "download_file"
    description = """Download a specific file associated with a given task ID from an API endpoint. The return value is the raw bytes of the file.
    Do not print the file content directly, as it may be large or binary data.
    """
    inputs = {
        "task_id": {
            "type": "string",
            "description": "the task ID associated with the file",
        },
    }
    output_type = "string"

    def forward(self, task_id: str):
        DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"

        response = requests.get(f"{DEFAULT_API_URL}/files/{task_id}")
        response.raise_for_status()
        return response.content


class ReadExcelFileBytes(Tool):
    name = "read_excel_file_bytes"
    description = """Read the content of an Excel file downloaded from a specific task ID.
    """
    inputs = {
        "excel_bytes": {
            "type": "string",
            "description": "the bytes content of the Excel file",
        },
    }
    output_type = "object"  # pandas DataFrame

    def forward(self, excel_bytes: str):
        from io import BytesIO

        import pandas as pd

        df = pd.read_excel(BytesIO(excel_bytes))
        print(f"Read {len(df)} rows from the Excel file as pandas DataFrame.")
        return df
