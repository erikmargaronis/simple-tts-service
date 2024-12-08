from fastapi import FastAPI
from api import tts_router
from config import Config

config = Config()
app = FastAPI(title="Text-to-Speech Service", version="0.1.0")
app.include_router(tts_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.host, port=config.port)