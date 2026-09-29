from abc import ABC, abstractmethod
from typing import Optional

class BaseSpeechProvider(ABC):
    @abstractmethod
    async def text_to_speech(self, text: str, language: str = "en") -> Optional[str]:
        pass

    @abstractmethod
    async def speech_to_text(self, audio_data: bytes, language: str = "en") -> str:
        pass


class WebStandardSpeechProvider(BaseSpeechProvider):
    """
    Standard speech handler that leverages browser Web Speech API on the client side
    and provides structured transcription guidance on the backend.
    """
    async def text_to_speech(self, text: str, language: str = "en") -> Optional[str]:
        # Frontend utilizes Web Speech API (speechSynthesis) with zero latency.
        return None

    async def speech_to_text(self, audio_data: bytes, language: str = "en") -> str:
        # Frontend uses SpeechRecognition with multilingual Indian language acoustic models.
        return ""

speech_provider = WebStandardSpeechProvider()
