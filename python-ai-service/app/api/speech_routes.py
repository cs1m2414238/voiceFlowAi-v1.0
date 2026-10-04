from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.exceptions import SpeechProcessingError
from app.speech.stt_service import transcribe_audio
from app.speech.tts_service import synthesize_speech

router = APIRouter(prefix="/speech", tags=["Speech"])


class TTSRequest(BaseModel):
    text: str
    voice: str = "Rachel"


class TTSResponse(BaseModel):
    text: str
    voice: str
    format: str
    audio_base64: str
    duration_seconds: float


class STTResponse(BaseModel):
    text: str
    language: str
    confidence: float
    duration_seconds: float | None = None


@router.post("/stt", response_model=STTResponse)
def speech_to_text(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
):
    filename = file.filename or ""
    try:
        content = file.file.read()
        result = transcribe_audio(
            audio_bytes=content,
            filename=filename,
            language=language,
        )
        return STTResponse(**result)
    except SpeechProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        file.file.close()


@router.post("/tts", response_model=TTSResponse)
def text_to_speech(request: TTSRequest):
    try:
        result = synthesize_speech(text=request.text, voice=request.voice)
        return TTSResponse(**result)
    except SpeechProcessingError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
