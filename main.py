from fastapi import FastAPI
# import url
from api.url import router as api_url
from webhooks.webhook import webhook_router, sio
import socketio

app = FastAPI()

app.mount("/ws", app=socketio.ASGIApp(sio))

app.include_router(api_url)
app.include_router(webhook_router)