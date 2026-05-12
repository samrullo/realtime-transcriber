import webrtcvad


class VoiceActivityDetector:
    def __init__(self, aggressiveness=2, sample_rate=16000):
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = sample_rate

    def is_speech(self, frame_bytes, frame_duration_ms=30):
        return self.vad.is_speech(frame_bytes, self.sample_rate)
