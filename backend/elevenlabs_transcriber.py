# backend/elevenlabs_transcriber.py
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('scripts/.env')

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
if not ELEVENLABS_API_KEY:
    raise ValueError("API Key no encontrada en .env")

def transcribe_audio(audio_path: str):
    """Transcribe audio usando ElevenLabs API"""
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    try:
        with open(audio_path, 'rb') as audio_file:
            # Preparamos los datos como multipart/form-data
            files = {
                'file': (os.path.basename(audio_path), audio_file, 'audio/mpeg'),
                'model_id': (None, 'scribe_v1'),
                'language_code': (None, 'es')
            }
            
            response = requests.post(url, headers=headers, files=files)
            
            if response.status_code == 200:
                return response.json()
            raise Exception(f"API Error {response.status_code}: {response.text}")
    
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

if __name__ == "__main__":
    try:
        audio_file = "tufinanc-audios/audio_prueba.mp3"
        
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Archivo no encontrado: {audio_file}")
        
        print(f"🔊 Procesando archivo: {audio_file}")
        result = transcribe_audio(audio_file)
        
        print("\n✅ Transcripción exitosa:")
        print(f"Texto: {result['text']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nSolución alternativa:")
        print("1. Verifica que tu plan de ElevenLabs incluya Speech-to-Text")
        print("2. Prueba con OpenAI Whisper (instrucciones abajo)")