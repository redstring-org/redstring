from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES_ROOT = REPO_ROOT / "data" / "fixtures"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


@lru_cache
def load_gold_events() -> dict[str, dict[str, Any]]:
    payload = _load_json(FIXTURES_ROOT / "gold_events.json")
    return {event["event_id"]: event for event in payload["events"]}


@lru_cache
def load_reference_data() -> dict[str, Any]:
    return _load_json(FIXTURES_ROOT / "reference_data.json")


@lru_cache
def load_optional_osint() -> dict[str, Any]:
    return _load_json(FIXTURES_ROOT / "optional_osint.json")
