from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from fastapi.responses import HTMLResponse
route = APIRouter()


# List to hold connected WebSockets
connected_clients = set()

@route.websocket("/ws/thought")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("Client connected")
    try:
        while True:
            await asyncio.sleep(5)  # Every 5 seconds
            message = "This is a thought at 5-second interval"
            await websocket.send_text(message)
    except WebSocketDisconnect:
        print("Client disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"Error: {e}")
        connected_clients.remove(websocket)