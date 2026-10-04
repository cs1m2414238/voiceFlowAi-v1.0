import os
import uuid
import shutil
from typing import Callable, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse

from config.config import settings
from stt.speechToText import stt_service
from tts.textToSpeech import tts_service

router = APIRouter(prefix="/voice", tags=["Voice AI Module"])

AUDIO_DIR = settings.AUDIO_DIR
os.makedirs(AUDIO_DIR, exist_ok=True)


def process_voice_pipeline(
    audio_file_path: str,
    ai_handler: Callable[[str], str],
    agent_type: str = "default",
    output_directory: str = AUDIO_DIR
) -> dict:
    """
    Core Voice AI Pipeline Integration Function.
    
    Flow:
    1. Audio File -> STT Service -> Transcript Text
    2. Transcript Text -> AI Handler Callback -> Response Text
    3. Response Text -> TTS Service -> Audio File Output
    
    Args:
        audio_file_path (str): Path to input speech audio file.
        ai_handler (Callable[[str], str]): Callback function (LLM/Agent) that accepts user text and returns AI text.
        agent_type (str): Persona type for TTS voice selection.
        output_directory (str): Directory where generated response audio will be written.
        
    Returns:
        dict: Object containing user_transcript, agent_response, and audio_path.
    """
    # 1. Speech-to-Text (STT)
    user_transcript = stt_service.transcribe_audio(audio_file_path)

    # 2. AI Application Logic Callback
    agent_response_text = ai_handler(user_transcript)

    # 3. Text-to-Speech (TTS)
    output_filename = f"output_{uuid.uuid4().hex}.mp3"
    output_audio_path = os.path.join(output_directory, output_filename)
    tts_service.synthesize_speech(agent_response_text, output_audio_path, agent_type=agent_type)

    return {
        "user_transcript": user_transcript,
        "agent_response": agent_response_text,
        "output_audio_path": output_audio_path,
        "audio_filename": output_filename
    }


# Standalone FastAPI Router Endpoints for Voice AI Integration

@router.post("/transcribe")
def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """API Endpoint: Upload audio file and receive recognized text transcript."""
    temp_filename = f"stt_{uuid.uuid4().hex}.wav"
    temp_path = os.path.join(AUDIO_DIR, temp_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = stt_service.transcribe_audio(temp_path)
    return {"transcript": transcript}


@router.post("/synthesize")
def synthesize_audio_endpoint(
    text: str = Form(...),
    agent_type: str = Form("default")
):
    """API Endpoint: Send text and generate spoken audio output file."""
    audio_filename = f"tts_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    tts_service.synthesize_speech(text, audio_path, agent_type=agent_type)

    return {
        "audio_filename": audio_filename,
        "audio_url": f"/voice/audio/play/{audio_filename}"
    }


@router.get("/audio/play/{audio_filename}")
def play_audio_file(audio_filename: str):
    """API Endpoint: Stream audio file to browser/client with automatic MIME detection."""
    file_path = os.path.join(AUDIO_DIR, audio_filename)
    if not os.path.exists(file_path):
        alt_path = file_path.rsplit('.', 1)[0] + (".mp3" if audio_filename.endswith(".wav") else ".wav")
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            raise HTTPException(status_code=404, detail="Audio file not found")

    with open(file_path, "rb") as f:
        head = f.read(4)

    if head.startswith(b"ID3") or head.startswith(b"\xff\xfb") or head.startswith(b"\xff\xf3") or head.startswith(b"\xff\xf2"):
        media_type = "audio/mpeg"
    elif head.startswith(b"RIFF"):
        media_type = "audio/wav"
    else:
        media_type = "audio/mpeg" if file_path.endswith(".mp3") else "audio/wav"

    headers = {
        "Accept-Ranges": "bytes",
        "Cache-Control": "public, max-age=3600"
    }
    return FileResponse(file_path, media_type=media_type, headers=headers)
