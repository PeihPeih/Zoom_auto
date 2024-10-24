from fastapi import FastAPI, Request
# import url
from api.url import router as api_url
# from webhooks.webhook import webhook_router
import socketio
from fastapi.middleware.cors import CORSMiddleware
import os
import hmac
import hashlib

app = FastAPI()

# CORS Middleware setup
app = FastAPI()

# Tạo socketio server và kết nối với FastAPI
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')
sio_app = socketio.ASGIApp(sio, app)

app.mount("/ws", sio_app)
app.add_route("/socket.io", sio_app, methods=["GET", "POST"])
app.add_api_websocket_route("/socket.io", sio_app)


# API routes setup
app.include_router(api_url)

ZOOM_SECRET_TOKEN = os.environ.get("f")

@app.get("/")
async def root():
    return "Hello"

@app.post("/webhook")
async def webhook(request: Request):
    print(ZOOM_SECRET_TOKEN)
    headers = dict(request.headers)
    body = await request.json()
    print(headers)
    print(body)

    if 'payload' in body and 'plainToken' in body['payload']:  # Zoom URL validation
        secret_token = ZOOM_SECRET_TOKEN.encode("utf-8")
        plaintoken = body['payload']['plainToken']
        mess = plaintoken.encode("utf-8")
        has = hmac.new(secret_token, mess, hashlib.sha256).digest()
        hexmessage = has.hex()

        response = {
            'plainToken': plaintoken,
            'encryptedToken': hexmessage
        }
        return response

    event = body.get('event')
    payload = body.get('payload')

    # Event for participant joined meeting
    if event == 'meeting.participant_joined':
        data = {}
        object = payload.get('object', {})
        participant = object.get('participant', {})
        data['name'] = participant.get('user_name')
        data['join_time'] = participant.get('join_time')

        await sio.emit("participant_joined", data)
        return {"message": "Data sent via socket"}
