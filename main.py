from fastapi import FastAPI
# import url
from api.url import router as api_url
from webhooks.webhook import webhook_router
import socketio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')
sio_app = socketio.ASGIApp(sio, app)

app.mount("/", app=sio_app)
app.add_route("/socket.io", sio_app, methods=["GET", "POST"])
app.add_api_websocket_route("/socket.io", sio_app)

app.include_router(api_url)
app.include_router(webhook_router)