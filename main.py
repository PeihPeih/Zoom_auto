from fastapi import FastAPI
# import url
from api.url import router as api_url
from webhooks.webhook import webhook_router

app = FastAPI()
app.include_router(api_url)
app.include_router(webhook_router)