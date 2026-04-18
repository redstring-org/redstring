from __future__ import annotations

from app.domain.case_engine import engine


def test_osint_disabled_by_default() -> None:
    case = engine.build_case(["CY-0213-001", "AC-0224-001", "IR-0231-001"])
    assert case.osint_enabled is False
