import os
import re
import wave
import struct
import math
import asyncio
from config.config import settings

# Persona-based Neural Voice mappings (Microsoft Edge Neural Voices)
VOICE_MAP = {
    "manager": "en-US-AvaNeural",
    "triage": "en-US-AvaNeural",
    "greeting": "en-US-AvaNeural",
    "faq": "en-US-EmmaNeural",
    "knowledge": "en-US-EmmaNeural",
    "order_booking": "en-US-AndrewNeural",
    "orders": "en-US-AndrewNeural",
    "booking": "en-US-AndrewNeural",
    "complaints": "en-US-BrianNeural",
    "support": "en-US-BrianNeural",
    "recommendation": "en-US-AnaNeural",
    "default": "en-US-AvaNeural"
}


class TextToSpeechService:
    """
    Multi-provider Text-to-Speech (TTS) service supporting ElevenLabs API,
    Edge Neural TTS (edge-tts), Google TTS (gTTS), and synthetic WAV fallback.
    """
    def __init__(self):
        self.provider = settings.TTS_PROVIDER

    def _clean_text_for_speech(self, text: str) -> str:
        """
        Strip markdown syntax, emojis, URLs, and bullet points for clear spoken output.
        """
        if not text:
            return ""
        # Remove URLs
        cleaned = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove markdown markers (*, _, #, `, ~)
        cleaned = re.sub(r'[*_#`~]', '', cleaned)
        # Remove bullet point hyphens at start of lines or sentences
        cleaned = re.sub(r'^\s*[-•]\s+', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'\.\s*[-•]\s+', '. ', cleaned)
        # Remove non-ASCII characters & emojis
        cleaned = re.sub(r'[^\x00-\x7F]+', ' ', cleaned)
        # Replace multiple spaces / newlines with single space
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def synthesize_speech(self, text: str, output_path: str, agent_type: str = "default") -> str:
        """
        Synthesize text into spoken audio output.
        
        Args:
            text (str): Input text to synthesize into speech.
            output_path (str): File path where generated audio will be saved.
            agent_type (str): Voice persona selection identifier.
            
        Returns:
            str: Path to the generated audio file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        clean_text = self._clean_text_for_speech(text)

        # 1. ElevenLabs API Integration
        if self.provider == "elevenlabs" and settings.ELEVENLABS_API_KEY:
            try:
                import requests
                url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
                headers = {
                    "xi-api-key": settings.ELEVENLABS_API_KEY,
                    "Content-Type": "application/json"
                }
                body = {
                    "text": clean_text or text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
                }
                res = requests.post(url, json=body, headers=headers)
                if res.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(res.content)
                    return output_path
            except Exception as e:
                print(f"[TTS Error] ElevenLabs API error: {e}")

        # 2. Microsoft Edge Neural Text-to-Speech (edge-tts)
        if clean_text:
            try:
                import edge_tts
                voice = VOICE_MAP.get(agent_type.lower() if agent_type else "default", VOICE_MAP["default"])
                
                async def _run_edge_tts():
                    communicate = edge_tts.Communicate(clean_text, voice)
                    await communicate.save(output_path)

                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as pool:
                            pool.submit(lambda: asyncio.run(_run_edge_tts())).result()
                    else:
                        loop.run_until_complete(_run_edge_tts())
                except RuntimeError:
                    asyncio.run(_run_edge_tts())

                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return output_path
            except Exception as e:
                print(f"[TTS Warning] edge-tts synthesis failed: {e}. Falling back to gTTS.")

        # 3. Google Text-to-Speech (gTTS) Fallback
        if clean_text:
            try:
                from gtts import gTTS
                tts = gTTS(text=clean_text, lang='en', slow=False)
                tts.save(output_path)
                return output_path
            except Exception as e:
                print(f"[TTS Warning] gTTS voice synthesis failed: {e}. Falling back to synthetic chime.")

        # 4. Local Synthetic WAV Audio Chime Generator Fallback
        self._generate_synthetic_beep_wav(output_path)
        return output_path

    def _generate_synthetic_beep_wav(self, output_path: str, duration_sec: float = 2.0, sample_rate: int = 44100):
        """Generate a valid 16-bit PCM WAV notification chime locally without external network dependencies."""
        num_samples = int(duration_sec * sample_rate)
        
        with wave.open(output_path, "w") as wav_file:
            wav_file.setnchannels(1)        # Mono
            wav_file.setsampwidth(2)       # 16-bit PCM
            wav_file.setframerate(sample_rate)

            # Generate pleasant dual-tone AI notification chime
            for i in range(num_samples):
                t = i / sample_rate
                freq = 523.25 if t < 0.7 else (659.25 if t < 1.4 else 783.99)
                envelope = math.exp(-2.5 * (t % 0.7))
                sample_val = int(12000 * envelope * math.sin(2 * math.pi * freq * t))
                sample_val = max(-32767, min(32767, sample_val))
                wav_file.writeframes(struct.pack("<h", sample_val))


tts_service = TextToSpeechService()
