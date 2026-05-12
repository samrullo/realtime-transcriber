# Realtime Transcriber

A modular real-time PC audio transcription app.

It captures audio from an input device, detects speech with WebRTC VAD, chunks speech into utterances, transcribes locally with `faster-whisper`, and publishes transcript events through a CLI or FastAPI WebSocket server.

## Features

- List PC audio devices.
- Capture microphone or virtual input-device audio.
- Voice activity detection.
- Near-real-time local transcription.
- CLI output.
- FastAPI HTTP/WebSocket API.
- Modular design for future OpenAI Realtime/API backend, speaker diarization, GUI, or system-audio capture.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
```

On some systems, `sounddevice` requires PortAudio.

macOS:

```bash
brew install portaudio
```

Ubuntu/Debian:

```bash
sudo apt-get install portaudio19-dev
```

## Configure

Copy the example environment file:

```bash
cp .env.example .env
```

List devices:

```bash
rt-transcriber devices
```

Then set the selected device index in `.env`:

```env
TRANSCRIBER_DEVICE_INDEX=3
```

For CPU, keep:

```env
TRANSCRIBER_WHISPER_DEVICE=cpu
TRANSCRIBER_WHISPER_COMPUTE_TYPE=int8
```

For NVIDIA CUDA, try:

```env
TRANSCRIBER_WHISPER_DEVICE=cuda
TRANSCRIBER_WHISPER_COMPUTE_TYPE=float16
```

## Run in terminal

```bash
rt-transcriber listen
```

## Run server

```bash
rt-transcriber server
```

Open:

```text
http://127.0.0.1:8765
```

WebSocket:

```text
ws://127.0.0.1:8765/ws/transcript
```
