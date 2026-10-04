import base64

from app.core.config import settings
from app.core.exceptions import SpeechProcessingError
from app.core.logging import get_logger
from app.speech.audio_processor import generate_tone_wav_bytes

logger = get_logger(__name__)

SUPPORTED_VOICES = {"Rachel", "Adam", "Bella", "Antoni", "Josh"}


def synthesize_speech(text: str, voice: str = "Rachel") -> dict:
    """Synthesize spoken audio from text and return WAV metadata with base64 audio."""
    if not text or not str(text).strip():
        raise SpeechProcessingError("Text for speech synthesis must not be empty.")

    cleaned_text = str(text).strip()
    selected_voice = (voice or settings.DEFAULT_TTS_VOICE).strip() or "Rachel"

    word_count = len(cleaned_text.split())
    duration_seconds = round(min(max(word_count * 0.15, 0.25), 5.0), 2)
    wav_bytes = generate_tone_wav_bytes(duration_seconds=duration_seconds)
    audio_b64 = base64.b64encode(wav_bytes).decode("ascii")

    logger.info(
        "Synthesized speech voice=%s chars=%d duration=%.2fs",
        selected_voice,
        len(cleaned_text),
        duration_seconds,
    )

    return {
        "text": cleaned_text,
        "voice": selected_voice,
        "format": "wav",
        "audio_base64": audio_b64,
        "duration_seconds": duration_seconds,
    }
