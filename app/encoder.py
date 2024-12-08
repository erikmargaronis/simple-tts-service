from io import BytesIO
from pydub import AudioSegment
import numpy as np

media_type_mapping = {
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "opus": "audio/ogg; codecs=opus",
    "aac": "audio/aac",
    "flac": "audio/flac",
    "pcm": "audio/L16",
}

def encode_pcm(data) -> np.ndarray:
    """
    Convert waveform data to PCM (Pulse Code Modulation) format.

    Args:
        data (list or np.ndarray): Input waveform data, expected to be a list or NumPy array 
            of floating-point values.

    Returns:
        np.ndarray: Normalized waveform data converted to 16-bit PCM format.

    Raises:
        ValueError: If the input audio data contains only silence (maximum absolute value is 0).
    """
    
    audio_np = np.array(data, dtype=np.float32)
    max_val = np.max(np.abs(audio_np))
    if max_val == 0:
        raise ValueError("Audio data contains only silence.")
    return np.int16(audio_np / max_val * 32767)

def encode_data(data, format: str, sample_rate: int = 22050) -> BytesIO:
    """
    Encode waveform data into the specified audio format.

    Args:
        data: Raw waveform data.
        format: Target audio format (e.g., wav, mp3).
        sample_rate: Audio sample rate.

    Returns:
        BytesIO: Encoded audio data.
    """
    audio_raw = encode_pcm(data)

    if format == "pcm":
        return BytesIO(audio_raw)

    audio_segment = AudioSegment(
        data=audio_raw.tobytes(),
        sample_width=2,
        frame_rate=sample_rate,
        channels=1,
    )

    audio_buffer = BytesIO()
    if format == "opus":
        audio_segment.export(audio_buffer, format="ogg", codec="libopus")
    else:
        audio_segment.export(audio_buffer, format=format)
    audio_buffer.seek(0)

    return audio_buffer
