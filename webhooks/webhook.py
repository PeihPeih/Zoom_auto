from fastapi import APIRouter, Request, HTTPException, Header
import json
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

webhook_router = APIRouter()

ZOOM_WEBHOOK_SECRET_TOKEN = os.environ.get("ZOOM_WEBHOOK_SECRET_TOKEN='qESnq1vHTQalC7o65xjV2A")

def verify_zoom_signature(request_timestamp: str, request_body: dict, zoom_signature: str):
    # Construct the message
    message = f"v0:{request_timestamp}:{json.dumps(request_body)}"
    
    # Hash the message using HMAC SHA-256 and the secret token
    hash_for_verify = hmac.new(
        ZOOM_WEBHOOK_SECRET_TOKEN.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    # Create the signature
    generated_signature = f"v0={hash_for_verify}"

    # Compare with the signature in the header
    return hmac.compare_digest(generated_signature, zoom_signature)

@webhook_router.post("/webhook")
async def zoom_webhook(request: Request, 
                       x_zm_request_timestamp: str = Header(...), 
                       x_zm_signature: str = Header(...)):
    try:
        # Parse the request body
        request_body = await request.json()

        # Validate the Zoom signature
        if verify_zoom_signature(x_zm_request_timestamp, request_body, x_zm_signature):
            return {"message": "Webhook verified", "data": request_body}
        else:
            raise HTTPException(status_code=400, detail="Invalid signature")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))