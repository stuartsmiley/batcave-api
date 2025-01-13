from fastapi import FastAPI, Query, Header, status, WebSocket
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from .routers import critters
from .routers import socket_ops
import os

APP_MODE = os.getenv("APP_MODE")
docs_url = None if APP_MODE == "production" else "/docs"
redoc_url = None if APP_MODE == "production" else "/redoc"
openapi_url = None if APP_MODE == "production" else "/openapi.json"

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url)

origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["*"],
                   allow_headers=["*"],)

app.include_router(critters.router)
app.include_router(socket_ops.router)

# manager = ConnectionManager()
@app.get("/")
def read_root():
    return {"hello", "Stu"}


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Web Socket Test</title>
    </head>
    <body>
        <h1>WebSocket TEST</h1>
        <h2>Your ID: <span id="ws-id"></span><h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/whatever")
async def get_whatever():
    return HTMLResponse(html)

# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.handle_message(websocket, data, client_id)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")

