from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
from tts.elevenlabs_client import ElevenLabsTTSClient

app = FastAPI()
tts_client = ElevenLabsTTSClient()

# Configuración fija
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Voz por defecto
DEFAULT_MODEL_ID = "eleven_multilingual_v2"  # Modelo multilingüe

class TTSPayload(BaseModel):
    """Solo necesita el texto, los demás parámetros son fijos"""
    text: str

@app.post("/api/tts")
async def convert_text_to_speech(payload: TTSPayload):
    """
    Endpoint simplificado para convertir texto a voz
    - Usa voice_id y model_id predefinidos
    - Solo recibe el texto a convertir
    """
    audio_stream, error = tts_client.text_to_speech(
        text=payload.text,
        voice_id=DEFAULT_VOICE_ID,
        model_id=DEFAULT_MODEL_ID
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return StreamingResponse(
        audio_stream,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "inline; filename=tts_output.mp3",
            "Access-Control-Allow-Origin": "*"
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)