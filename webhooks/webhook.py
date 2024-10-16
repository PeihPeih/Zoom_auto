from fastapi import APIRouter, Request, HTTPException, Header
import json
import secrets
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

webhook_router = APIRouter()

ZOOM_SECRET_TOKEN = os.environ.get("ZOOM_WEBHOOK_SECRET_TOKEN")


@webhook_router.post("/webhook")
async def webhook(request: Request):
    print(ZOOM_SECRET_TOKEN)
    headers = dict(request.headers)
    body = await request.json()
    print(headers)
    print(body)

    if 'payload' in body and 'plainToken' in body['payload']:
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
        print(response['message'])
        return response['message']
    else:
        return {'error': 'Invalid payload'}