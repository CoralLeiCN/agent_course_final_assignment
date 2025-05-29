from google import genai
from google.genai import types
from smolagents import Tool
import requests

from google.genai import types


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
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=[
                f"{prompt} And also try to answer the question: {question}",
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type="audio/mp3",
                ),
            ],
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
        )
        transcript = response.text

        return transcript


class DownloadFile(Tool):
    name = "download_file"
    description = """Download a specific file associated with a given task ID from an API endpoint.
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
    output_type = "string"

    def forward(self, excel_bytes: str):
        import pandas as pd
        from io import BytesIO

        df = pd.read_excel(BytesIO(excel_bytes))
        return df.to_string()
