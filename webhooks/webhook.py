from fastapi import APIRouter, Request, HTTPException, Header
import json
import secrets
import hmac
import hashlib
import os
from dotenv import load_dotenv
import socketio

load_dotenv()

webhook_router = APIRouter()

ZOOM_SECRET_TOKEN = os.environ.get("f")

sio = socketio.AsyncServer(async_mode='asgi')

@webhook_router.post("/webhook")
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