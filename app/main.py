from fastapi import FastAPI
from app.tts import tts_router

app = FastAPI(title="Text-to-Speech Service", version="1.0")

app.include_router(tts_router)
