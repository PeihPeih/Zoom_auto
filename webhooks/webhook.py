from fastapi import APIRouter, Request, HTTPException, Header
import json
import secrets
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

webhook_router = APIRouter()


SIGNATURE_HEADER = "Signature-Header"
SIGNATURE_ALGORITHM = "sha256"
ENCODE_FORMAT = "hex"
HMAC_SECRET = os.environ.get("ZOOM_WEBHOOK_SECRET_TOKEN")


@webhook_router.post("/webhook")
async def webhook(req: Request, signature_header: str = Header(None)):
    try:
        # Read the raw body (assuming the body is read as bytes)
        raw_body = await req.body()

        # Create HMAC digest with the payload and secret
        hmac_digest = hmac.new(
            HMAC_SECRET.encode(), raw_body, hashlib.sha256
        ).hexdigest()

        # Construct the digest with the algorithm and hex encoded format
        digest = f"{SIGNATURE_ALGORITHM}={hmac_digest}"

        # Compare the provider's signature with the computed digest
        if not signature_header or not secrets.compare_digest(digest, signature_header):
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Webhook Authenticated, process the request
        return {"message": "Success"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))