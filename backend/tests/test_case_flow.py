from __future__ import annotations

from copy import deepcopy

from app.domain.case_engine import build_test_engine, engine
from app.fixtures.loader import load_gold_events, load_reference_data


def _test_engine():
    return build_test_engine(reference=load_reference_data(), events=load_gold_events())


def test_case_shell_before_injection() -> None:
    case = engine.build_case([])
    assert case.state is None
    assert case.timeline == []
    assert case.why_linked == []
    assert case.escalation_recommendation is None


def test_observe_after_cyber_trigger() -> None:
    case = engine.build_case(["CY-0213-001"])
    assert case.state == "Observe"
    assert case.next_human_check == (
        "Call the SOC now to confirm whether the active VPN session for jmercer@vendorco is still live "
        "and whether the MFA approval was legitimate."
    )
    assert case.escalation_recommendation is None
    assert case.why_linked == [
        "Unexpected device login succeeded on vendor contractor account",
        "Active VPN session remains live",
    ]
    assert case.what_weakens_it == [
        "No linked on-campus evidence yet",
        "Remote session legitimacy not yet confirmed",
    ]


def test_verify_now_after_badge_event() -> None:
    case = engine.build_case(["CY-0213-001", "AC-0224-001"])
    assert case.state == "Verify Now"
    assert case.next_human_check == (
        "Call the VendorCo night supervisor now to confirm whether John Mercer is scheduled onsite "
        "and carrying badge B-1842."
    )
    assert case.escalation_recommendation is None
    assert case.why_linked[-2:] == [
        "Badge B-1842 maps to John Mercer",
        "After-hours badge use at South Service Entrance SE-3",
    ]


def test_escalate_now_after_officer_report() -> None:
    case = engine.build_case(["CY-0213-001", "AC-0224-001", "IR-0231-001"])
    assert case.state == "Escalate Now"
    assert case.next_human_check == (
        "Dispatch an officer to Imaging Service Corridor now to identify the person reported near Door SE-3."
    )
    assert case.escalation_recommendation == "Notify protective services leadership and SOC now."
    assert case.why_linked[-2:] == [
        "Officer report in adjacent Imaging Service Corridor within seven minutes",
        "No escort observed",
    ]
    assert [item.event_id for item in case.timeline] == ["CY-0213-001", "AC-0224-001", "IR-0231-001"]


def test_report_without_badge_does_not_escalate() -> None:
    case = engine.build_case(["CY-0213-001", "IR-0231-001"])
    assert case.state == "Observe"
    assert case.escalation_recommendation is None


def test_identity_mismatch_blocks_verify_now() -> None:
    reference = deepcopy(load_reference_data())
    reference["identity_record"]["account"] = "other@vendorco"
    test_engine = build_test_engine(reference=reference, events=load_gold_events())

    case = test_engine.build_case(["CY-0213-001", "AC-0224-001"])

    assert case.state == "Observe"
    assert [item.event_id for item in case.timeline] == ["CY-0213-001"]


def test_badge_mapping_mismatch_blocks_verify_now() -> None:
    reference = deepcopy(load_reference_data())
    reference["badge_mapping"]["person_id"] = "P-9999"
    test_engine = build_test_engine(reference=reference, events=load_gold_events())

    case = test_engine.build_case(["CY-0213-001", "AC-0224-001"])

    assert case.state == "Observe"
    assert [item.event_id for item in case.timeline] == ["CY-0213-001"]


def test_door_mapping_mismatch_blocks_verify_now() -> None:
    reference = deepcopy(load_reference_data())
    reference["door_mapping"]["door_id"] = "SE-9"
    test_engine = build_test_engine(reference=reference, events=load_gold_events())

    case = test_engine.build_case(["CY-0213-001", "AC-0224-001"])

    assert case.state == "Observe"
    assert [item.event_id for item in case.timeline] == ["CY-0213-001"]


def test_badge_event_outside_30_minute_window_blocks_verify_now() -> None:
    events = deepcopy(load_gold_events())
    events["AC-0224-001"]["occurred_at"] = "2026-04-18T02:44:00-04:00"
    test_engine = build_test_engine(reference=load_reference_data(), events=events)

    case = test_engine.build_case(["CY-0213-001", "AC-0224-001"])

    assert case.state == "Observe"
    assert [item.event_id for item in case.timeline] == ["CY-0213-001"]


def test_report_outside_15_minute_window_blocks_escalate_now() -> None:
    events = deepcopy(load_gold_events())
    events["IR-0231-001"]["occurred_at"] = "2026-04-18T02:40:00-04:00"
    test_engine = build_test_engine(reference=load_reference_data(), events=events)

    case = test_engine.build_case(["CY-0213-001", "AC-0224-001", "IR-0231-001"])

    assert case.state == "Verify Now"
    assert case.escalation_recommendation is None
    assert [item.event_id for item in case.timeline] == ["CY-0213-001", "AC-0224-001"]


def test_same_zone_report_is_accepted_for_escalation() -> None:
    events = deepcopy(load_gold_events())
    reference = deepcopy(load_reference_data())
    events["IR-0231-001"]["zone_id"] = reference["door_mapping"]["zone_id"]
    test_engine = build_test_engine(reference=reference, events=events)

    case = test_engine.build_case(["CY-0213-001", "AC-0224-001", "IR-0231-001"])

    assert case.state == "Escalate Now"
    assert case.escalation_recommendation == "Notify protective services leadership and SOC now."


def test_duplicate_injections_do_not_duplicate_timeline_items() -> None:
    case = engine.build_case(["CY-0213-001", "CY-0213-001", "AC-0224-001", "IR-0231-001", "IR-0231-001"])

    assert [item.event_id for item in case.timeline] == ["CY-0213-001", "AC-0224-001", "IR-0231-001"]
