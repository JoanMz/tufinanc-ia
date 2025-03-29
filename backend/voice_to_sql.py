import os
from pathlib import Path
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import logging

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carga de variables de entorno
env_path = Path(__file__).parent.parent / 'scripts' / '.env'
load_dotenv(dotenv_path=env_path)

class ElevenLabsTranscriber:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY no encontrada en .env")
        
        self.client = ElevenLabs(api_key=self.api_key)
        self.model_id = "scribe_v1"  # Único modelo actualmente disponible

    def transcribe_audio(
        self,
        audio_path: str,
        language_code: str = None,
        tag_audio_events: bool = True,
        num_speakers: int = None,
        timestamps_granularity: str = "word",
        diarize: bool = False
    ) -> dict:
        """
        Transcribe audio file using ElevenLabs API
        
        Args:
            audio_path: Path to audio file to transcribe
            language_code: ISO-639-1/3 language code (optional)
            tag_audio_events: Whether to tag audio events (default: True)
            num_speakers: Max number of speakers (1-32, optional)
            timestamps_granularity: "none", "word" or "character"
            diarize: Whether to identify speakers (default: False)
            
        Returns:
            Dict with transcription results
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
            
            # Validar formato de granularidad
            if timestamps_granularity not in ["none", "word", "character"]:
                raise ValueError("timestamps_granularity debe ser 'none', 'word' o 'character'")
            
            # Realizar la transcripción
            response = self.client.speech_to_text.convert(
                model_id=self.model_id,
                file=audio_path,
                language_code=language_code,
                tag_audio_events=tag_audio_events,
                num_speakers=num_speakers,
                timestamps_granularity=timestamps_granularity,
                diarize=diarize
            )
            
            logger.info(f"Transcripción exitosa. Idioma detectado: {response['language_code']}")
            return response
            
        except Exception as e:
            logger.error(f"Error en transcripción: {str(e)}")
            raise

# Ejemplo de uso
if __name__ == "__main__":
    try:
        transcriber = ElevenLabsTranscriber()
        
        # Configuración de transcripción
        audio_file = "tufinanc-audios/audio_prueba.mp3"  # Cambiar por tu archivo
        result = transcriber.transcribe_audio(
            audio_path=audio_file,
            language_code="es",  # Opcional: 'es' para español
            num_speakers=2,      # Opcional: ajustar según necesidad
            diarize=True         # Identificar hablantes diferentes
        )
        
        # Resultados
        print("\n✅ Transcripción completada:")
        print(f"Idioma: {result['language_code']} (confianza: {result['language_probability']:.2f})")
        print(f"\nTexto:\n{result['text']}")
        
        # Si se solicitó diarización
        if 'words' in result and result['words']:
            print("\n📝 Palabras con timestamps:")
            for word in result['words'][:10]:  # Mostrar primeras 10 palabras como ejemplo
                print(f"{word['start']:.2f}-{word['end']:.2f}s: {word['text']}")
                
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPosibles soluciones:")
        print("- Verifica que el archivo de audio existe")
        print("- Confirma que tu API key es válida")
        print("- Asegúrate que el archivo sea menor a 1GB")
        print("- Verifica los formatos soportados: MP3, WAV, etc.")