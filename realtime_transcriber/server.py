import asyncio
from fastapi import FastAPI, WebSocket
import uvicorn

from realtime_transcriber.audio import AudioInput
from realtime_transcriber.config import Settings
from realtime_transcriber.pipeline import RealtimePipeline
from realtime_transcriber.transcriber import WhisperTranscriber
from realtime_transcriber.vad import VoiceActivityDetector

app = FastAPI()
clients = []


@app.get("/")
def root():
    return {"status": "ok"}


@app.websocket("/ws/transcript")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    try:
        while True:
            await asyncio.sleep(60)
    finally:
        clients.remove(ws)


async def producer():
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

    for event in pipeline.run():
        dead = []

        for client in clients:
            try:
                await client.send_json(event)
            except Exception:
                dead.append(client)

        for client in dead:
            clients.remove(client)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(producer())


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8765)
