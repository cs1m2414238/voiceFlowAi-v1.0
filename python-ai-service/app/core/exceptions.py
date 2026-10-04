class AIServiceError(Exception):
    """Base exception for all VoiceFlow Python AI service errors."""

    def __init__(self, message: str = "An error occurred in the AI service.", status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class LLMConnectionError(AIServiceError):
    """Raised when the local or remote LLM cannot be reached or fails."""

    def __init__(self, message: str = "Failed to communicate with the LLM service."):
        super().__init__(message=message, status_code=503)


class DocumentProcessingError(AIServiceError):
    """Raised when document loading, chunking, or vector ingestion fails."""

    def __init__(self, message: str = "Failed to process the uploaded document.", status_code: int = 400):
        super().__init__(message=message, status_code=status_code)


class SpeechProcessingError(AIServiceError):
    """Raised when STT transcription, TTS synthesis, or audio validation fails."""

    def __init__(self, message: str = "Failed to process audio data.", status_code: int = 400):
        super().__init__(message=message, status_code=status_code)


class BackendIntegrationError(AIServiceError):
    """Raised when communication with the Java backend fails."""

    def __init__(self, message: str = "Failed to communicate with the Java backend.", status_code: int = 502):
        super().__init__(message=message, status_code=status_code)
