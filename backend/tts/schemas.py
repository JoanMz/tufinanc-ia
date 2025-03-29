from pydantic import BaseModel
from typing import Optional
# Reemplaza la clase TTSPayload con:
from tts.schemas import TTSPayload

class VoiceInfo(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None

class TTSResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    error: Optional[str] = None