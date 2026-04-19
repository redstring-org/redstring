from __future__ import annotations

from app.domain.case_engine import engine
from app.raw_event_store import raw_event_store


def test_osint_disabled_by_default() -> None:
    raw_event_store.reset()
    case = engine.build_active_case()
    assert case.osint_enabled is False
