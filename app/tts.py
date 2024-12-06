from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from uuid import uuid4
from io import BytesIO
import asyncio

from app.schemas import TTSRequest
from app.encoder import encode_data, media_type_mapping
from app.model_manager import model_manager

executor = ThreadPoolExecutor(max_workers=4)
tts_router = APIRouter()

async def run_tts(text: str, voice_id: str, model_name: str) -> list:
    """Generate speech waveform for the given text, voice ID, and model."""
    tts_model = model_manager.get_model(model_name)
    loop = asyncio.get_running_loop()

    if tts_model.is_multi_speaker:
        waveform = await loop.run_in_executor(
            executor,
            partial(tts_model.tts, text=text, speaker=voice_id)
        )
    else:
        waveform = await loop.run_in_executor(
            executor,
            partial(tts_model.tts, text=text)
        )
    return waveform

@tts_router.post("/tts", response_class=StreamingResponse, summary="Text-to-Speech Endpoint")
async def tts(request: TTSRequest):
    """
    Convert input text to speech audio in the specified format.

    Args:
        request (TTSRequest): Input text, voice ID, and response format.

    Returns:
        StreamingResponse: The encoded audio stream.
    """
    task_id = str(uuid4())

    # Load the model dynamically (lazy loading)
    #model_name = "tts_models/en/vctk/vits"  # This could be passed dynamically in the future
    try:
        model_manager.load_model(request.model)
    except ValueError as e:
        raise e

    # Generate waveform
    data = await run_tts(request.input, request.voice, request.model)

    if request.response_format not in media_type_mapping:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{request.response_format}'. Supported formats: {list(media_type_mapping.keys())}."
        )

    # Encode data
    encoded_data = encode_data(data, request.response_format)
    media_type = media_type_mapping.get(request.response_format, "application/octet-stream")

    return StreamingResponse(
        encoded_data,
        media_type=media_type,
        headers={"X-Task-ID": task_id},
    )
