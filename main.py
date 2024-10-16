from fastapi import FastAPI
# import url
from api.url import router as api_url

app = FastAPI()
app.include_router(api_url)


