from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.responses import HTMLResponse
from service.simulate import get_random_eeg_sample_json

route = APIRouter()

# List to hold connected WebSockets
connected_clients = set()

@route.websocket("/ws/simulate_send_eeg")
async def send_eeg(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("Client connected to /ws/send_eeg")

    try:
        while True:
            await asyncio.sleep(5)  # send every 5 seconds
            message = get_random_eeg_sample_json()
            await websocket.send_text(message)
    except WebSocketDisconnect:
        print("Client disconnected from /ws/send_eeg")
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"Unexpected error: {e}")
        connected_clients.remove(websocket)



@route.get("/ws/info", tags=["Transcribe"])
async def websocket_info():
    return {
        "endpoint": "/ws/simulate_send_eeg",
        "protocol": "WebSocket",
        "description": "Simulation of sending eeg data.",
        "input": "EEG Data",
        "output": "JSON messages containing eeg data and the translated text.",
    }
