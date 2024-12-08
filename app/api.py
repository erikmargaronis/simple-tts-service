from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from uuid import uuid4
import asyncio

from schemas import TTSRequest
from encoder import encode_data, media_type_mapping
from model_manager import model_manager

executor = ThreadPoolExecutor(max_workers=4)
tts_router = APIRouter()

async def run_tts(text: str, voice_id: str, model_name: str) -> list[float]:
    """
    Asynchronously generate speech waveform for the given text, voice ID, and model.

    Args:
        text (str): The input text to be converted into speech.
        voice_id (str): The identifier for the speaker/voice.
        model_name (str): The name of the TTS model to be used.

    Returns:
        list (float): Generated speech waveform data.
    """
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
async def tts(request: TTSRequest) -> StreamingResponse:
    """
    Convert input text to speech audio in the specified format.

    Args:
        request (TTSRequest): Input text, voice ID, and response format.

    Returns:
        StreamingResponse: The encoded audio stream.
    """
    task_id = str(uuid4())

    try:
        model_manager.load_model(request.model)
    except ValueError as e:
        return HTTPException(
            status_code=400,
            detail=f"Unrecognizable model name {request.model}"
        )

    data = await run_tts(request.input, request.voice, request.model)

    if request.response_format not in media_type_mapping:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{request.response_format}'. Supported formats: {list(media_type_mapping.keys())}."
        )

    encoded_data = encode_data(data, request.response_format)
    media_type = media_type_mapping.get(request.response_format, "application/octet-stream")

    return StreamingResponse(
        encoded_data,
        media_type=media_type,
        headers={"X-Task-ID": task_id},
    )
