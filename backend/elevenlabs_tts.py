# backend/elevenlabs_tts.py
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Configuración
env_path = Path(__file__).parent.parent / 'scripts' / '.env'
load_dotenv(dotenv_path=env_path)

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
if not ELEVENLABS_API_KEY:
    raise ValueError("API Key no encontrada en .env")

class ElevenLabsTTS:
    def __init__(self):
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        
    def text_to_speech(
        self,
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Voz por defecto
        model_id: str = "eleven_monolingual_v1",
        save_path: str = None
    ) -> str:
        """
        Convierte texto a voz usando ElevenLabs API
        
        Args:
            text: Texto a convertir (máx 5000 caracteres)
            voice_id: ID de la voz a usar
            model_id: Modelo a usar
            save_path: Ruta para guardar el audio (ej. "audios/salida.mp3")
            
        Returns:
            Ruta del archivo guardado
        """
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            data = {
                "text": text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}: {response.text}")
            
            # Guardar archivo
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Audio guardado en: {save_path}")
                return save_path
            
            return response.content
            
        except Exception as e:
            raise Exception(f"Error en TTS: {str(e)}")

    def get_voices(self) -> list:
        """Obtiene lista de voces disponibles"""
        try:
            response = requests.get(f"{self.base_url}/voices", headers=self.headers)
            return response.json().get('voices', [])
        except Exception as e:
            raise Exception(f"Error obteniendo voces: {str(e)}")

if __name__ == "__main__":
    try:
        tts = ElevenLabsTTS()
        
        # 1. Obtener voces disponibles
        print("🔍 Obteniendo voces disponibles...")
        voices = tts.get_voices()
        print(f"\n🗣 Voces encontradas: {len(voices)}")
        for voice in voices[:3]:  # Mostrar primeras 3
            print(f"- {voice['name']} (ID: {voice['voice_id']})")
        
        # 2. Ejemplo de conversión
        print("\n🔊 Probando conversión de texto a voz...")
        text = "Hola, este es un ejemplo de texto convertido a voz usando la API de ElevenLabs."
        output_file = "tufinanc-audios/ejemplo_tts.mp3"
        
        audio_path = tts.text_to_speech(
            text=text,
            voice_id=voices[0]['voice_id'] if voices else "21m00Tcm4TlvDq8ikWAM",
            save_path=output_file
        )
        
        print("\n🎧 Conversión exitosa!")
        print(f"📝 Texto usado: {text}")
        print(f"💾 Audio guardado en: {audio_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nSolución de problemas:")
        print("1. Verifica tu API Key en scripts/.env")
        print("2. Asegúrate de tener conexión a internet")
        print("3. Prueba con un texto más corto")