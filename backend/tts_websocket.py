import os
import json
import asyncio
import websockets
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from pathlib import Path
from dotenv import load_dotenv

# Configuración
env_path = Path(__file__).parent.parent / 'scripts' / '.env'
load_dotenv(dotenv_path=env_path)

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"

app = FastAPI()

async def forward_to_elevenlabs(websocket: WebSocket):
    """Conexión WebSocket con ElevenLabs"""
    elevenlabs_ws_url = f"wss://api.elevenlabs.io/v1/text-to-speech/{DEFAULT_VOICE_ID}/stream-input"
    
    async with websockets.connect(
        elevenlabs_ws_url,
        extra_headers={"xi-api-key": ELEVENLABS_API_KEY}
    ) as elevenlabs_ws:
        
        # Configuración inicial
        init_payload = {
            "text": " ",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            },
            "model_id": DEFAULT_MODEL_ID
        }
        await elevenlabs_ws.send(json.dumps(init_payload))
        
        # Bucle principal
        while True:
            try:
                # Recibir texto del cliente
                client_data = await websocket.receive_text()
                data = json.loads(client_data)
                
                if data.get("action") == "close":
                    # Enviar señal de cierre a ElevenLabs
                    await elevenlabs_ws.send(json.dumps({"text": ""}))
                    break
                
                # Enviar texto a ElevenLabs
                tts_payload = {
                    "text": data["text"],
                    "try_trigger_generation": True
                }
                await elevenlabs_ws.send(json.dumps(tts_payload))
                
                # Recibir audio de ElevenLabs y enviar al cliente
                elevenlabs_data = await elevenlabs_ws.recv()
                await websocket.send_text(elevenlabs_data)
                
            except websockets.exceptions.ConnectionClosed:
                break

@app.websocket("/ws/tts")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para el cliente"""
    await websocket.accept()
    try:
        await forward_to_elevenlabs(websocket)
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, ws_ping_interval=30, ws_ping_timeout=30)