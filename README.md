# Simple Text-to-Speech Service

A FastAPI-based service for generating speech from text using the Coqui TTS library.

## Features
- Text-to-speech generation using pre-trained models.
- Supports multiple audio formats (e.g., wav, mp3, opus).
- Asynchronous processing for high performance.

## Setup

### Clone the repository:
   ```bash
   git clone <repository-url>
   cd text_to_speech_service
   ```
### Install dependencies
```bash

pip install -r requirements.txt
```

#### Install espeak TTS backend
##### Ubuntu
`sudo apt install espeak`

### Run the application
```bash
uvicorn app.main:app --reload
```

## Supported models
Single and multispeaker models. Voice conversion models are not supported yet.

## API Endpoints
### POST /tts
```
curl -X POST http://localhost:8000/tts \
    -H "Content-Type: Application/json" \
    -d '{"model": "tts_models/en/vctk/vits", "voice": "p273", "response_format": "wav", "input": "Hello world!"}' \
    --output audio.wav
```
Returns a streaming audio file in the specified format.