from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    enable_osint_context: bool = os.getenv("ENABLE_OSINT_CONTEXT", "false").lower() == "true"


settings = Settings()
