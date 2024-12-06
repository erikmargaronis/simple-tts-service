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

### Run the application
```bash
uvicorn app.main:app --reload
```

## Supported models
Single and multispeaker models. Voice conversion models are not supported yet.

## API Endpoints
### POST /tts
Converts text to speech audio.
```
{
  "model": {name of coqui model}
  "input": "Hello, world!",
  "voice": "default",
  "response_format": "mp3"
}

```

Response:

Streamed audio data in the specified format.
