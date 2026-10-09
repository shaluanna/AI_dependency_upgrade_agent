import os

from google import genai


def generate_analysis(prompt: str):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash"
    )

    try:
        client = genai.Client(api_key=api_key)

        chat = client.chats.create(
            model=model_name
        )

        response = chat.send_message(prompt)

        return response.text

    except Exception as exc:
        return f"Gemini analysis could not be generated: {exc}"