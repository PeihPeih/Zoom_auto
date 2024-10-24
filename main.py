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

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')
sio_app = socketio.ASGIApp(sio, app)

app.mount("/", app=sio_app)
app.add_route("/socket.io", sio_app, methods=["GET", "POST"])
app.add_api_websocket_route("/socket.io", sio_app)

app.include_router(api_url)

ZOOM_SECRET_TOKEN = os.environ.get("f")

@app.get("/")
async def root():
    return "Hello BE"

@app.post("/webhook")
async def webhook(request: Request):
    print(ZOOM_SECRET_TOKEN)
    headers = dict(request.headers)
    body = await request.json()
    print(headers)
    print(body)

    if 'payload' in body and 'plainToken' in body['payload']: # Dùng để validated url trên link zoom webhook
        secret_token = ZOOM_SECRET_TOKEN.encode("utf-8")
        plaintoken = body['payload']['plainToken']
        mess = plaintoken.encode("utf-8")
        has = hmac.new(secret_token, mess, hashlib.sha256).digest()
        hexmessage = has.hex()

        response = {
            'message': {
                'plainToken': plaintoken,
                'encryptedToken': hexmessage
            }
        }
        return response['message']
    
    event = body['event']
    payload = body['payload']

    # Event started meeting        
    if event == 'meeting.participant_joined':
        data = {}
        object = payload['object']
        participant = object['participant']
        data['name']=participant['user_name']
        data['join_time']=participant['join_time']
        await sio.emit("participant_joined", data)
        return "Đã gửi data qua socket"
