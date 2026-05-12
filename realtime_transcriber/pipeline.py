import time


class RealtimePipeline:
    def __init__(self, audio_input, vad, transcriber, frame_ms=30):
        self.audio_input = audio_input
        self.vad = vad
        self.transcriber = transcriber
        self.frame_ms = frame_ms

    def run(self):
        self.audio_input.start()

        speech_buffer = bytearray()
        silence_frames = 0

        while True:
            frame = self.audio_input.q.get()

            if self.vad.is_speech(frame, self.frame_ms):
                speech_buffer.extend(frame)
                silence_frames = 0
            else:
                silence_frames += 1

            if speech_buffer and silence_frames > 20:
                text = self.transcriber.transcribe_pcm(bytes(speech_buffer))

                if text.strip():
                    yield {
                        "timestamp": time.time(),
                        "text": text,
                    }

                speech_buffer.clear()
                silence_frames = 0
