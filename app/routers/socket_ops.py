from fastapi import APIRouter, WebSocket
from ..connection_manager import ConnectionManager
from starlette.websockets import WebSocketDisconnect

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/api/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.handle_message(websocket, data, client_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
