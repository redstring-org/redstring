from __future__ import annotations

from app.api.routes import get_active_case, inject_event, reset_demo
from app.raw_event_store import raw_event_store
from app.schemas import InjectEventRequest
from app.state_store import store


def setup_function() -> None:
    store.reset()
    raw_event_store.reset()


def test_demo_injection_flow_updates_single_case() -> None:
    active_case = get_active_case()
    assert active_case.state is None

    observe_case = inject_event(InjectEventRequest(event_id="CY-0213-001"))
    assert observe_case.case_id == "CASE-GOLD-001"
    assert observe_case.state == "Observe"
    assert observe_case.next_human_check == (
        "Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live "
        "and whether the MFA approval was legitimate."
    )
    assert observe_case.escalation_recommendation is None
    assert observe_case.why_linked == [
        "Unexpected device login succeeded on vendor contractor account",
        "Active VPN session remains live",
    ]

    verify_case = inject_event(InjectEventRequest(event_id="AC-0224-001"))
    assert verify_case.case_id == "CASE-GOLD-001"
    assert verify_case.state == "Verify Now"
    assert verify_case.next_human_check == (
        "Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite "
        "and carrying badge B-1842."
    )
    assert verify_case.escalation_recommendation is None
    assert verify_case.why_linked == [
        "Unexpected device login succeeded on vendor contractor account",
        "Active VPN session remains live",
        "Badge B-1842 maps to John Mercer",
        "After-hours badge use at South Service Entrance SE-3",
    ]

    escalate_case = inject_event(InjectEventRequest(event_id="IR-0231-001"))
    assert escalate_case.case_id == "CASE-GOLD-001"
    assert escalate_case.state == "Escalate Now"
    assert escalate_case.next_human_check == (
        "Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3."
    )
    assert escalate_case.escalation_recommendation == "Notify protective services leadership and SOC now."
    assert escalate_case.why_linked == [
        "Unexpected device login succeeded on vendor contractor account",
        "Active VPN session remains live",
        "Badge B-1842 maps to John Mercer",
        "After-hours badge use at South Service Entrance SE-3",
        "Officer report in adjacent Imaging Service Corridor within seven minutes",
        "No escort observed",
    ]
    assert [item.event_id for item in escalate_case.timeline] == ["CY-0213-001", "AC-0224-001", "IR-0231-001"]
    assert raw_event_store.count() == 3


def test_duplicate_inject_does_not_create_duplicate_case_events() -> None:
    first = inject_event(InjectEventRequest(event_id="CY-0213-001"))
    second = inject_event(InjectEventRequest(event_id="CY-0213-001"))

    assert first.case_id == second.case_id == "CASE-GOLD-001"
    assert [item.event_id for item in second.timeline] == ["CY-0213-001"]


def test_demo_reset_clears_active_case_state() -> None:
    inject_event(InjectEventRequest(event_id="CY-0213-001"))

    reset_case = reset_demo()

    assert reset_case.state is None
    assert reset_case.timeline == []
    assert reset_case.why_linked == []
    assert reset_case.escalation_recommendation is None
    assert raw_event_store.count() == 0


def test_unknown_event_id_returns_400() -> None:
    try:
        inject_event(InjectEventRequest(event_id="NOPE"))
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
        assert raw_event_store.count() == 0
    else:
        raise AssertionError("Expected HTTPException for unknown event id")


def test_raw_badge_payload_is_accepted_and_saved_without_changing_case_state() -> None:
    case = inject_event(
        InjectEventRequest(
            timestamp="2026-04-18T07:45:00.000+00:00Z",
            staff_id="11",
            first_name="Taylor",
            last_name="Davis",
            role_title="Registered Nurse",
            role_category="Clinical staff",
            department="Laboratory",
            shift="Rotating",
            door_name="Main Entrance",
            category="Perimeter",
            area="Hospital Perimeter",
            door_type="Perimeter Door",
            badge_required="Yes",
            action="enter",
            access_result="Granted",
        )
    )

    assert case.state is None
    assert case.timeline == []
    assert raw_event_store.count() == 1
    assert raw_event_store.latest_payload() == {
        "timestamp": "2026-04-18T07:45:00.000+00:00Z",
        "staff_id": "11",
        "first_name": "Taylor",
        "last_name": "Davis",
        "role_title": "Registered Nurse",
        "role_category": "Clinical staff",
        "department": "Laboratory",
        "shift": "Rotating",
        "door_name": "Main Entrance",
        "category": "Perimeter",
        "area": "Hospital Perimeter",
        "door_type": "Perimeter Door",
        "badge_required": "Yes",
        "action": "enter",
        "access_result": "Granted",
    }
    case_groups = raw_event_store.list_case_groups()
    assert len(case_groups) == 1
    assert len(raw_event_store.list_case_group_event_ids(case_groups[0]["case_group_id"])) == 1


def test_raw_osint_post_payload_is_accepted_and_saved_without_changing_case_state() -> None:
    case = inject_event(
        InjectEventRequest(
            post_id="2045539490546995340",
            screen_name="DCPoliceDept",
            posted_at="2026-04-18T16:26:33.000Z",
            url="https://x.com/DCPoliceDept/status/2045539490546995340",
            text="Expect road closures for several hours for the Major Crash Investigation.",
            is_reply="no",
        )
    )

    assert case.state is None
    assert case.timeline == []
    assert raw_event_store.count() == 1
    assert raw_event_store.latest_payload() == {
        "post_id": "2045539490546995340",
        "screen_name": "DCPoliceDept",
        "posted_at": "2026-04-18T16:26:33.000Z",
        "url": "https://x.com/DCPoliceDept/status/2045539490546995340",
        "text": "Expect road closures for several hours for the Major Crash Investigation.",
        "is_reply": "no",
    }


def test_raw_suspicious_person_payload_is_accepted_and_saved_without_changing_case_state() -> None:
    case = inject_event(
        InjectEventRequest(
            report_id="SPR-0001",
            occurred_at="2026-04-18T06:10:56.350Z",
            reporter="medical staff",
            location="Emergency Department Ambulance Bay",
            description=(
                "Person in mismatched scrubs observed pushing unattended equipment cases toward "
                "Emergency Department Ambulance Bay."
            ),
            verified="yes",
            person_removed="yes",
        )
    )

    assert case.state is None
    assert case.timeline == []
    assert raw_event_store.count() == 1
    assert raw_event_store.latest_payload() == {
        "report_id": "SPR-0001",
        "occurred_at": "2026-04-18T06:10:56.350Z",
        "reporter": "medical staff",
        "location": "Emergency Department Ambulance Bay",
        "description": (
            "Person in mismatched scrubs observed pushing unattended equipment cases toward "
            "Emergency Department Ambulance Bay."
        ),
        "verified": "yes",
        "person_removed": "yes",
    }


def test_related_raw_events_are_grouped_into_one_case_cluster() -> None:
    inject_event(
        InjectEventRequest(
            timestamp="2026-04-18T06:05:00.000Z",
            staff_id="11",
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
            description="Person in mismatched scrubs observed pushing unattended equipment cases toward Emergency Department Ambulance Bay.",
            verified="yes",
            person_removed="yes",
        )
    )

    case_groups = raw_event_store.list_case_groups()
    assert len(case_groups) == 1
    assert len(raw_event_store.list_case_group_event_ids(case_groups[0]["case_group_id"])) == 2


def test_unrelated_raw_events_split_into_separate_case_clusters() -> None:
    inject_event(
        InjectEventRequest(
            timestamp="2026-04-18T06:05:00.000Z",
            staff_id="11",
            door_name="Emergency Department Ambulance Bay",
            area="Emergency Department Ambulance Bay",
            access_result="Granted",
        )
    )
    inject_event(
        InjectEventRequest(
            report_id="SPR-0099",
            occurred_at="2026-04-18T08:15:00.000Z",
            reporter="visitor",
            location="Pharmacy Hallway",
            description="Unknown person was seen opening supply cabinets near Pharmacy Hallway.",
            verified="no",
            person_removed="no",
        )
    )

    case_groups = raw_event_store.list_case_groups()
    assert len(case_groups) == 2
