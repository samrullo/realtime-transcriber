import io
import wave
import numpy as np
from faster_whisper import WhisperModel


class WhisperTranscriber:
    def __init__(self, model_name, device, compute_type, sample_rate=16000):
        self.sample_rate = sample_rate
        self.model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

    def transcribe_pcm(self, pcm_bytes):
        audio_np = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio_np,
            vad_filter=True,
            beam_size=1,
        )

        return " ".join(segment.text.strip() for segment in segments)
