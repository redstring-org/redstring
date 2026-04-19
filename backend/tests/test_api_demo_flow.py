from __future__ import annotations

from app.api.routes import get_active_case, get_case_groups, inject_event, reset_demo
from app.raw_event_store import raw_event_store
from app.schemas import InjectEventRequest


def setup_function() -> None:
    raw_event_store.reset()


def _inject_qualified_emergency_group() -> None:
    inject_event(
        InjectEventRequest(
            timestamp="2026-04-18T06:05:00.000Z",
            staff_id="11",
            first_name="Taylor",
            last_name="Davis",
            door_name="Emergency Department Ambulance Bay",
            area="Emergency Department Ambulance Bay",
            access_result="Granted",
        )
    )
    inject_event(
        InjectEventRequest(
            report_id="SPR-0001",
            occurred_at="2026-04-18T06:10:56.350Z",
            reporter="medical staff",
            location="Emergency Department Ambulance Bay",
            description="Person in mismatched scrubs observed pushing unattended equipment cases.",
            verified="yes",
        )
    )
    inject_event(
        InjectEventRequest(
            post_id="POST-0001",
            screen_name="citywatch",
            posted_at="2026-04-18T06:12:00.000Z",
            location="Emergency Department Ambulance Bay",
            text="Unusual overnight equipment movement reported outside the ambulance bay.",
        )
    )


def test_active_case_is_empty_before_any_group_qualifies() -> None:
    active_case = get_active_case()

    assert active_case.state is None
    assert active_case.timeline == []
    assert active_case.case_title == "Awaiting qualified correlated case group"
    assert active_case.trigger_summary == "No case group has reached the minimum threshold of 3 linked events yet."


def test_case_groups_api_returns_empty_list_before_events() -> None:
    result = get_case_groups()

    assert result.total == 0
    assert result.case_groups == []


def test_demo_event_injection_does_not_open_active_case() -> None:
    active_case = inject_event(InjectEventRequest(event_id="CY-0213-001"))

    assert active_case.state is None
    assert raw_event_store.count() == 1

    groups = get_case_groups()
    assert groups.total == 1
    assert groups.case_groups[0].event_count == 1
    assert groups.case_groups[0].qualified_at is None


def test_group_of_three_mixed_events_opens_observe_case() -> None:
    _inject_qualified_emergency_group()

    active_case = get_active_case()

    assert active_case.state == "Observe"
    assert active_case.case_title == "Observed correlated case group requiring review"
    assert active_case.location == "Emergency Department Ambulance Bay"
    assert active_case.primary_subject == "Taylor Davis"
    assert active_case.trigger_summary == (
        "Case group qualified after 3 linked events: Badge Access, OSINT, Suspicious-Person Report."
    )
    assert active_case.why_linked == [
        "Case group reached the qualification threshold with 3 linked events",
        "Badge-access activity is present in the qualified case group",
        "Suspicious-person reporting is present in the qualified case group",
        "OSINT context is present in the qualified case group",
    ]
    assert active_case.what_weakens_it == [
        "Identity-level correlation across the grouped events still requires operator review"
    ]
    assert active_case.next_human_check == (
        "Review badge activity, OSINT context, and suspicious-person reporting now to confirm whether they "
        "describe the same onsite activity near Emergency Department Ambulance Bay."
    )
    assert active_case.escalation_recommendation is None
    assert [item.event_id for item in active_case.timeline] == ["11", "SPR-0001", "POST-0001"]

    groups = get_case_groups()
    assert groups.total == 1
    assert groups.case_groups[0].event_count == 3
    assert groups.case_groups[0].qualified_at == "2026-04-18T06:12:00.000Z"
    assert groups.case_groups[0].qualification_rank == 1


def test_first_group_to_qualify_stays_active_when_later_group_qualifies() -> None:
    _inject_qualified_emergency_group()
    first_group = raw_event_store.get_first_qualified_case_group()
    assert first_group is not None

    inject_event(
        InjectEventRequest(
            timestamp="2026-04-18T08:15:00.000Z",
            staff_id="77",
            first_name="Jordan",
            last_name="Lee",
            door_name="Pharmacy Hallway",
            area="Pharmacy Hallway",
            access_result="Granted",
        )
    )
    inject_event(
        InjectEventRequest(
            report_id="SPR-0099",
            occurred_at="2026-04-18T08:16:00.000Z",
            reporter="visitor",
            location="Pharmacy Hallway",
            description="Unknown person was seen opening supply cabinets near Pharmacy Hallway.",
        )
    )
    inject_event(
        InjectEventRequest(
            post_id="POST-0099",
            screen_name="scanner",
            posted_at="2026-04-18T08:17:00.000Z",
            location="Pharmacy Hallway",
            text="Late-night activity reported in the pharmacy corridor.",
        )
    )

    active_case = get_active_case()
    assert active_case.case_id == first_group["case_group_id"]
    assert active_case.location == "Emergency Department Ambulance Bay"

    groups = get_case_groups()
    assert groups.total == 2
    assert sorted(group.qualification_rank for group in groups.case_groups if group.qualification_rank is not None) == [
        1,
        2,
    ]


def test_demo_reset_clears_groups_and_active_case() -> None:
    _inject_qualified_emergency_group()

    reset_case = reset_demo()

    assert reset_case.state is None
    assert reset_case.timeline == []
    assert raw_event_store.count() == 0
    assert get_case_groups().case_groups == []


def test_unknown_event_id_returns_400() -> None:
    try:
        inject_event(InjectEventRequest(event_id="NOPE"))
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
        assert raw_event_store.count() == 0
    else:
        raise AssertionError("Expected HTTPException for unknown event id")
