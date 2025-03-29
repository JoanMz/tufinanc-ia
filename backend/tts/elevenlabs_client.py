import os
import requests
from pathlib import Path
#from dotenv import load_dotenv
import io
from typing import Tuple, Optional

# Configuración
# env_path = Path(__file__).parent.parent.parent / 'scripts' / '.env'
# load_dotenv(dotenv_path=env_path)

class ElevenLabsTTSClient:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise RuntimeError("API Key no encontrada en .env")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str
    ) -> Tuple[Optional[io.BytesIO], Optional[str]]:
        """Versión simplificada sin parámetros opcionales"""
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            response = requests.post(
                url,
                headers=self.headers,
                json={
                    "text": text,
                    "model_id": model_id,
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
            )
            
            if response.status_code != 200:
                return None, f"API Error {response.status_code}: {response.text}"
            
            return io.BytesIO(response.content), None
            
        except Exception as e:
            return None, f"Error en conversión: {str(e)}"
