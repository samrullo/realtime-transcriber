import queue
import sounddevice as sd


class AudioInput:
    def __init__(self, samplerate, channels, blocksize, device=None):
        self.q = queue.Queue()
        self.stream = sd.InputStream(
            samplerate=samplerate,
            channels=channels,
            dtype="int16",
            blocksize=blocksize,
            device=device,
            callback=self.callback,
        )

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    @staticmethod
    def list_devices():
        return sd.query_devices()
