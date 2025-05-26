from google import genai
from google.genai import types
from smolagents import Tool


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
