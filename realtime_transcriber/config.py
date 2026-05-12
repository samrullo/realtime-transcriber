from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    sample_rate: int = int(os.getenv("TRANSCRIBER_SAMPLE_RATE", "16000"))
    channels: int = int(os.getenv("TRANSCRIBER_CHANNELS", "1"))
    frame_duration_ms: int = int(os.getenv("TRANSCRIBER_FRAME_MS", "30"))
    vad_aggressiveness: int = int(os.getenv("TRANSCRIBER_VAD", "2"))
    device_index: int | None = (
        int(os.getenv("TRANSCRIBER_DEVICE_INDEX"))
        if os.getenv("TRANSCRIBER_DEVICE_INDEX")
        else None
    )
    whisper_model: str = os.getenv("TRANSCRIBER_WHISPER_MODEL", "small")
    whisper_device: str = os.getenv("TRANSCRIBER_WHISPER_DEVICE", "cpu")
    whisper_compute_type: str = os.getenv(
        "TRANSCRIBER_WHISPER_COMPUTE_TYPE", "int8"
    )
