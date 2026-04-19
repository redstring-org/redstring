from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from ..config import settings
from .text_templates import PROVENANCE_LABELS, TIMELINE_SUMMARIES
from ..fixtures.loader import load_gold_events, load_reference_data
from ..schemas import ActiveCaseResponse, InjectEventRequest, ProvenanceItem, TimelineItem


class CaseEngine:
    def __init__(self) -> None:
        self.reference = load_reference_data()
        self.events = load_gold_events()

    def validate_injectable_event(self, event_id: str) -> None:
        if event_id not in self.events:
            raise ValueError(f"Unknown event_id: {event_id}")

    def resolve_injectable_event_id(self, payload: InjectEventRequest) -> str:
        if payload.event_id:
            self.validate_injectable_event(payload.event_id)
            return payload.event_id

        raw_payload = payload.raw_payload()
        if raw_payload:
            raise ValueError(
                "Raw payloads are accepted by /api/demo/inject, but this locked MVP can only inject the demo "
                "event_ids CY-0213-001, AC-0224-001, or IR-0231-001."
            )

        raise ValueError("Inject payload must include event_id or a raw event body.")

    def build_case(self, injected_event_ids: list[str]) -> ActiveCaseResponse:
        case_info = self.reference["case"]
        reason_codes = self.reference["reason_codes"]

        active_case = ActiveCaseResponse(
            case_id=case_info["case_id"],
            case_title=case_info["case_title"],
            location=case_info["location"],
            state=None,
            primary_subject=case_info["primary_subject"],
            trigger_summary=case_info["trigger_summary"],
            timeline=[],
            why_linked=[],
            what_weakens_it=[],
            next_human_check="",
            escalation_recommendation=None,
            provenance=[],
            osint_enabled=settings.enable_osint_context,
        )

        if "CY-0213-001" not in injected_event_ids:
            return active_case

        cyber = self.events["CY-0213-001"]
        self._append_event(active_case, cyber)
        active_case.state = "Observe"
        active_case.why_linked = [
            reason_codes["unexpected_login"],
            reason_codes["active_session"],
        ]
        active_case.what_weakens_it = [
            reason_codes["no_campus_evidence"],
            reason_codes["session_unconfirmed"],
        ]
        active_case.next_human_check = self._select_next_action(state="Observe", badge_linked=False)

        badge_linked = "AC-0224-001" in injected_event_ids and self._badge_event_links(
            cyber, self.events["AC-0224-001"]
        )
        if not badge_linked:
            return active_case

        badge = self.events["AC-0224-001"]
        self._append_event(active_case, badge)
        active_case.state = "Verify Now"
        active_case.why_linked.extend(
            [
                reason_codes["badge_maps"],
                reason_codes["after_hours_badge"],
            ]
        )
        active_case.what_weakens_it = [
            reason_codes["schedule_unconfirmed"],
            reason_codes["session_unconfirmed"],
        ]
        active_case.next_human_check = self._select_next_action(state="Verify Now", badge_linked=True)

        report_linked = "IR-0231-001" in injected_event_ids and self._report_event_links(
            badge, self.events["IR-0231-001"]
        )
        if not report_linked:
            return active_case

        report = self.events["IR-0231-001"]
        self._append_event(active_case, report)
        active_case.state = "Escalate Now"
        active_case.why_linked.extend(
            [
                reason_codes["officer_report_adjacent"],
                reason_codes["no_escort"],
            ]
        )
        active_case.what_weakens_it = [
            reason_codes["schedule_unconfirmed"],
            reason_codes["session_unconfirmed"],
        ]
        active_case.next_human_check = self._select_next_action(state="Escalate Now", badge_linked=True)
        active_case.escalation_recommendation = self.reference["escalation_recommendation"]
        return active_case

    def _append_event(self, active_case: ActiveCaseResponse, event: dict[str, Any]) -> None:
        event_id = event["event_id"]
        timestamp = event["occurred_at"]
        active_case.timeline.append(
            TimelineItem(
                event_id=event_id,
                timestamp=timestamp,
                summary=TIMELINE_SUMMARIES[event_id],
                source=event["source"],
            )
        )
        active_case.provenance.append(
            ProvenanceItem(
                event_id=event_id,
                label=PROVENANCE_LABELS[event_id],
                source=event["source"],
                timestamp=timestamp,
            )
        )

    def _badge_event_links(self, cyber: dict[str, Any], badge: dict[str, Any]) -> bool:
        identity = self._resolve_identity(cyber)
        badge_mapping = self._resolve_badge_mapping(badge)
        door_mapping = self._resolve_door_mapping(badge)
        if not identity or not badge_mapping or not door_mapping:
            return False

        trigger_matches = cyber["event_type"] == "vendor_remote_access_anomaly"
        same_subject = (
            badge_mapping["person_id"] == identity["person_id"]
            and badge_mapping["full_name"] == identity["full_name"]
        )
        same_company = badge_mapping["company"] == identity["company"]
        within_window = self._minutes_between(cyber["occurred_at"], badge["occurred_at"]) <= 30
        return all([trigger_matches, same_subject, same_company, within_window])

    def _report_event_links(self, badge: dict[str, Any], report: dict[str, Any]) -> bool:
        door_mapping = self._resolve_door_mapping(badge)
        zone_adjacency = self.reference["zone_adjacency"]
        if not door_mapping:
            return False

        same_campus = badge["campus_id"] == report["campus_id"]
        within_window = self._minutes_between(badge["occurred_at"], report["occurred_at"]) <= 15
        same_zone = report["zone_id"] == door_mapping["zone_id"]
        adjacent_zone = (
            door_mapping["zone_id"] == zone_adjacency["from_zone_id"]
            and report["zone_id"] == zone_adjacency["to_zone_id"]
        )
        same_building = door_mapping["building_id"] == zone_adjacency["building_id"]
        zone_matches = same_zone or (adjacent_zone and same_building)
        return all([same_campus, within_window, zone_matches])

    def _resolve_identity(self, cyber: dict[str, Any]) -> dict[str, Any] | None:
        identity = self.reference["identity_record"]
        if cyber["account"] != identity["account"]:
            return None
        return identity

    def _resolve_badge_mapping(self, badge: dict[str, Any]) -> dict[str, Any] | None:
        badge_mapping = self.reference["badge_mapping"]
        if badge["badge_id"] != badge_mapping["badge_id"]:
            return None
        return badge_mapping

    def _resolve_door_mapping(self, badge: dict[str, Any]) -> dict[str, Any] | None:
        door_mapping = self.reference["door_mapping"]
        if badge["door_id"] != door_mapping["door_id"]:
            return None
        if not door_mapping.get("zone_id"):
            return None
        return door_mapping

    def _select_next_action(self, *, state: str, badge_linked: bool) -> str:
        next_actions = self.reference["next_actions"]
        if state == "Escalate Now":
            return next_actions["escalate_now"]
        if badge_linked:
            return next_actions["verify_now"]
        return next_actions["observe"]

    @staticmethod
    def _minutes_between(start: str, end: str) -> float:
        return (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60


engine = CaseEngine()


def build_test_engine(
    *,
    reference: dict[str, Any] | None = None,
    events: dict[str, dict[str, Any]] | None = None,
) -> CaseEngine:
    test_engine = CaseEngine()
    if reference is not None:
        test_engine.reference = deepcopy(reference)
    if events is not None:
        test_engine.events = deepcopy(events)
    return test_engine
