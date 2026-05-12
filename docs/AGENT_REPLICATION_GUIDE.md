# Agent Replication Guide

## System Architecture

The project is intentionally modular.

Core modules:

- audio.py
- vad.py
- transcriber.py
- pipeline.py
- server.py
- cli.py

## Responsibilities

### AudioInput

Responsible only for capturing raw PCM frames.

Replaceable implementations:

- sounddevice
- PyAudio
- WASAPI loopback
- BlackHole capture
- PulseAudio monitor

### VoiceActivityDetector

Determines whether a frame contains speech.

Currently uses WebRTC VAD.

Future replacements:

- Silero VAD
- pyannote VAD
- neural VAD

### WhisperTranscriber

Converts PCM speech buffers into text.

Current backend:

- faster-whisper

Future backends:

- OpenAI realtime API
- Whisper.cpp
- NVIDIA Riva
- Deepgram

### RealtimePipeline

Coordinates:

- reading audio
- VAD decisions
- speech buffering
- transcription triggering
- event publishing

## Future Extensions

### Partial Streaming Transcripts

Current pipeline emits only finalized utterances.

For low latency:

- maintain rolling audio window
- emit partial hypotheses
- reconcile finalized text later

### Speaker Diarization

Add speaker labels by:

- pyannote.audio
- NVIDIA NeMo

### Persistence

Add storage:

- SQLite
- PostgreSQL
- vector database

### GUI

Potential clients:

- Electron
- Tauri
- PySide6

### System Audio Capture

macOS:

- BlackHole
- Loopback

Windows:

- WASAPI loopback

Linux:

- PipeWire monitor
- PulseAudio monitor
