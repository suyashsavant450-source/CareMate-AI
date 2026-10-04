import io
import requests
from gtts import gTTS


LANGUAGE_CODES = {
    "English": "en",
    "Marathi": "mr",
    "Hindi": "hi",
    "Kannada": "kn",
}


def generate_speech(text, language="English"):

    if not text or not text.strip():
        raise ValueError("No text available for speech.")

    language_code = LANGUAGE_CODES.get(
        language,
        "en"
    )

    audio_buffer = io.BytesIO()

    try:

        tts = gTTS(
            text=text.strip(),
            lang=language_code,
            slow=False
        )

        # gTTS uses Google's online TTS service
        tts.write_to_fp(audio_buffer)

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Voice generation timed out. "
            "Please check your internet connection and try again."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to the voice service. "
            "Please check your internet connection."
        )

    except Exception as error:
        raise RuntimeError(
            f"Voice generation failed: {error}"
        )

    audio_buffer.seek(0)

    audio_bytes = audio_buffer.read()

    if not audio_bytes:
        raise RuntimeError(
            "Generated audio is empty."
        )

    return audio_bytes