import argparse

from realtime_transcriber.audio import AudioInput
from realtime_transcriber.config import Settings
from realtime_transcriber.pipeline import RealtimePipeline
from realtime_transcriber.server import run_server
from realtime_transcriber.transcriber import WhisperTranscriber
from realtime_transcriber.vad import VoiceActivityDetector


def command_devices():
    for idx, device in enumerate(AudioInput.list_devices()):
        print(idx, device)


def command_listen():
    settings = Settings()

    audio = AudioInput(
        samplerate=settings.sample_rate,
        channels=settings.channels,
        blocksize=int(settings.sample_rate * settings.frame_duration_ms / 1000),
        device=settings.device_index,
    )

    vad = VoiceActivityDetector(
        aggressiveness=settings.vad_aggressiveness,
        sample_rate=settings.sample_rate,
    )

    transcriber = WhisperTranscriber(
        settings.whisper_model,
        settings.whisper_device,
        settings.whisper_compute_type,
    )

    pipeline = RealtimePipeline(audio, vad, transcriber)

    print("Listening...")

    for event in pipeline.run():
        print(event["text"])


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("devices")
    sub.add_parser("listen")
    sub.add_parser("server")

    args = parser.parse_args()

    if args.command == "devices":
        command_devices()
    elif args.command == "listen":
        command_listen()
    elif args.command == "server":
        run_server()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
