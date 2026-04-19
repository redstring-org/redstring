from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent


@dataclass(frozen=True)
class Settings:
    enable_osint_context: bool = os.getenv("ENABLE_OSINT_CONTEXT", "false").lower() == "true"
    demo_events_db_path: Path = Path(
        os.getenv("DEMO_EVENTS_DB_PATH", str(BACKEND_DIR / "data" / "demo_events.sqlite3"))
    )


settings = Settings()
