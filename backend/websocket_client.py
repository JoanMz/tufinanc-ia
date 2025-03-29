import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/tts"
    
    async with websockets.connect(uri) as websocket:
        # Enviar texto en chunks
        texts = [
            "Hola, este es un",
            " ejemplo de streaming",
            " con WebSockets."
        ]
        
        for text in texts:
            await websocket.send(json.dumps({"text": text}))
            response = await websocket.recv()
            print("Recibido:", json.loads(response))
        
        # Cerrar conexión
        await websocket.send(json.dumps({"action": "close"}))

asyncio.get_event_loop().run_until_complete(test_websocket())