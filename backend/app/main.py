from __future__ import annotations

import csv
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .event_signal import raw_event_received
from .raw_event_store import raw_event_store

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_GEN = REPO_ROOT / "data_gen"

STREAMS = [
    (DATA_GEN / "hospital_badge_events_24h.csv",      0.5,   True),   # badge swipes — loop forever
    (DATA_GEN / "suspicious_person_reports_24h.csv",  8.0,   False),  # reports — stream once
    (DATA_GEN / "dcpolicedept_last_20_posts.csv",     12.0,  False),  # OSINT — stream once
]


def _stream_csv(csv_path: Path, interval: float, *, loop: bool = True) -> None:
    if not csv_path.exists():
        print(f"[streamer] Not found: {csv_path}")
        return
    print(f"[streamer] Starting {csv_path.name} @ {interval}s interval")

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return

    while True:
        for row in rows:
            try:
                row_id = raw_event_store.save(dict(row))
                raw_event_received.emit(row_id)
            except Exception:
                pass
            time.sleep(interval)
        if not loop:
            break


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    for csv_path, interval, loop in STREAMS:
        t = threading.Thread(target=_stream_csv, args=(csv_path, interval), kwargs={"loop": loop}, daemon=True)
        t.start()
    yield


app = FastAPI(title="RedString MVP Backend", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
