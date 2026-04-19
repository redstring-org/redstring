from __future__ import annotations

from app.domain.case_engine import engine
from app.event_signal import raw_event_received
from app.raw_event_store import raw_event_store


def setup_function() -> None:
    raw_event_store.reset()


def _save(payload: dict[str, str]) -> None:
    row_id = raw_event_store.save(payload)
    raw_event_received.emit(row_id)


def test_case_shell_before_any_group_qualifies() -> None:
    case = engine.build_active_case()

    assert case.state is None
    assert case.timeline == []
    assert case.why_linked == []
    assert case.escalation_recommendation is None


def test_qualified_group_builds_observe_case() -> None:
    _save(
        {
            "timestamp": "2026-04-18T06:05:00.000Z",
            "staff_id": "11",
            "first_name": "Taylor",
            "last_name": "Davis",
            "door_name": "Emergency Department Ambulance Bay",
            "area": "Emergency Department Ambulance Bay",
            "access_result": "Granted",
        }
    )
    _save(
        {
            "report_id": "SPR-0001",
            "occurred_at": "2026-04-18T06:10:56.350Z",
            "location": "Emergency Department Ambulance Bay",
            "description": "Person in mismatched scrubs observed pushing unattended equipment cases.",
        }
    )
    _save(
        {
            "post_id": "POST-0001",
            "posted_at": "2026-04-18T06:12:00.000Z",
            "screen_name": "citywatch",
            "location": "Emergency Department Ambulance Bay",
            "text": "Unusual overnight equipment movement reported outside the ambulance bay.",
        }
    )

    case = engine.build_active_case()

    assert case.state == "Observe"
    assert case.location == "Emergency Department Ambulance Bay"
    assert case.primary_subject == "Taylor Davis"
    assert [item.source for item in case.provenance] == ["Badge Access", "Officer Report", "citywatch"]


def test_first_group_to_qualify_remains_active() -> None:
    _save(
        {
            "timestamp": "2026-04-18T06:05:00.000Z",
            "staff_id": "11",
            "area": "Emergency Department Ambulance Bay",
        }
    )
    _save(
        {
            "report_id": "SPR-0001",
            "occurred_at": "2026-04-18T06:10:56.350Z",
            "location": "Emergency Department Ambulance Bay",
            "description": "Observed equipment movement.",
        }
    )
    _save(
        {
            "post_id": "POST-0001",
            "posted_at": "2026-04-18T06:12:00.000Z",
            "location": "Emergency Department Ambulance Bay",
            "text": "Ambulance bay activity noted.",
        }
    )
    first_group = raw_event_store.get_first_qualified_case_group()

    _save(
        {
            "timestamp": "2026-04-18T08:15:00.000Z",
            "staff_id": "77",
            "area": "Pharmacy Hallway",
        }
    )
    _save(
        {
            "report_id": "SPR-0099",
            "occurred_at": "2026-04-18T08:16:00.000Z",
            "location": "Pharmacy Hallway",
            "description": "Unknown person was seen opening supply cabinets.",
        }
    )
    _save(
        {
            "post_id": "POST-0099",
            "posted_at": "2026-04-18T08:17:00.000Z",
            "location": "Pharmacy Hallway",
            "text": "Late-night pharmacy activity reported.",
        }
    )

    case = engine.build_active_case()

    assert first_group is not None
    assert case.case_id == first_group["case_group_id"]
    assert case.location == "Emergency Department Ambulance Bay"


def test_group_does_not_qualify_before_three_events() -> None:
    _save(
        {
            "timestamp": "2026-04-18T06:05:00.000Z",
            "staff_id": "11",
            "area": "Emergency Department Ambulance Bay",
        }
    )
    _save(
        {
            "report_id": "SPR-0001",
            "occurred_at": "2026-04-18T06:10:56.350Z",
            "location": "Emergency Department Ambulance Bay",
            "description": "Observed equipment movement.",
        }
    )

    case = engine.build_active_case()
    assert case.state is None
    assert raw_event_store.get_first_qualified_case_group() is None
