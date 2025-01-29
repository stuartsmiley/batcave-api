from fastapi import FastAPI, Query, Header, status, WebSocket
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from .routers import critters
from .routers import socket_ops
import os
import secure
from .config import settings

# from dotenv import load_dotenv
#
# load_dotenv()

# APP_MODE = os.getenv("APP_MODE")
print('================================')
# print(APP_MODE)
print(settings.app_mode)
print('================================')
docs_url = None if settings.app_mode == "production" else "/docs"
redoc_url = None if settings.app_mode == "production" else "/redoc"
openapi_url = None if settings.app_mode == "production" else "/openapi.json"


app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url)

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
# enforces https - should be skipped / handled by reverse proxy if using?
# hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
# we want referrer info
# referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

# secure_headers = secure.Secure(
#     csp=csp,
#     hsts=hsts,
#     referrer=referrer,
#     cache=cache_value,
#     xfo=x_frame_options,
# )
secure_headers = secure.Secure.with_default_headers()

@app.middleware("http")
async def add_secure_headers(request, call_next):
    response = await call_next(request)
    await secure_headers.set_headers_async(response)
    return response

# can we get an array from settings.client_origin_url?
origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173'
    'https://192.168.1.251'
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   max_age=86400,
                   )

app.include_router(critters.router)
app.include_router(socket_ops.router)

# manager = ConnectionManager()
@app.get("/api")
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

@app.get("/api/whatever")
async def get_whatever():
    return HTMLResponse(html)
