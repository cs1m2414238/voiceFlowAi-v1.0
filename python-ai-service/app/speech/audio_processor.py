import io
import math
import struct
import wave
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.exceptions import SpeechProcessingError

ALLOWED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".webm", ".ogg"}


def get_audio_extension(filename: str) -> str:
    """Return the lowercase file extension (including dot) for an audio filename."""
    if not filename:
        return ""
    return Path(filename).suffix.lower()


def estimate_audio_duration(audio_bytes: bytes, extension: str = ".wav") -> float:
    """Estimate the duration of audio bytes in seconds."""
    if not audio_bytes:
        return 0.0

    if extension == ".wav" and len(audio_bytes) >= 44 and audio_bytes[:4] == b"RIFF":
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                if rate > 0:
                    return round(frames / float(rate), 2)
        except Exception:
            pass

    # Fallback heuristic (~16 KB/s average compressed/uncompressed stream)
    estimated = len(audio_bytes) / 16000.0
    return round(max(estimated, 0.1), 2)


def validate_audio_file(
    filename: str,
    audio_bytes: bytes,
    max_size_mb: Optional[int] = None,
) -> dict:
    """Validate audio file extension, non-empty payload, and size limit."""
    ext = get_audio_extension(filename)
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_AUDIO_EXTENSIONS))
        raise SpeechProcessingError(
            f"Unsupported audio format '{ext or 'unknown'}'. Allowed formats: {allowed}."
        )

    if not audio_bytes:
        raise SpeechProcessingError("The uploaded audio file is empty.")

    limit_mb = max_size_mb if max_size_mb is not None else settings.MAX_AUDIO_SIZE_MB
    max_bytes = limit_mb * 1024 * 1024
    if len(audio_bytes) > max_bytes:
        raise SpeechProcessingError(
            f"Audio file exceeds the maximum allowed size of {limit_mb} MB."
        )

    duration = estimate_audio_duration(audio_bytes, ext)
    return {
        "filename": filename,
        "extension": ext,
        "size_bytes": len(audio_bytes),
        "duration_seconds": duration,
    }


def generate_tone_wav_bytes(
    duration_seconds: float = 0.25,
    sample_rate: int = 16000,
    frequency_hz: float = 440.0,
) -> bytes:
    """Generate a valid mono 16-bit PCM WAV byte payload."""
    num_samples = max(int(duration_seconds * sample_rate), 1)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            sample = int(4000.0 * math.sin(2.0 * math.pi * frequency_hz * (i / sample_rate)))
            frames.extend(struct.pack("<h", sample))
        wav_file.writeframes(bytes(frames))
    return buf.getvalue()
