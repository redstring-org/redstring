from __future__ import annotations

from datetime import datetime
from typing import Any

from app.config import settings
from app.domain.text_templates import PROVENANCE_LABELS, TIMELINE_SUMMARIES
from app.fixtures.loader import load_gold_events, load_reference_data
from app.schemas import ActiveCaseResponse, ProvenanceItem, TimelineItem


class CaseEngine:
    def __init__(self) -> None:
        self.reference = load_reference_data()
        self.events = load_gold_events()

    def validate_injectable_event(self, event_id: str) -> None:
        if event_id not in self.events:
            raise ValueError(f"Unknown event_id: {event_id}")

    def build_case(self, injected_event_ids: list[str]) -> ActiveCaseResponse:
        case_info = self.reference["case"]
        reason_codes = self.reference["reason_codes"]
        next_actions = self.reference["next_actions"]

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
        active_case.next_human_check = next_actions["observe"]

        badge_linked = "AC-0224-001" in injected_event_ids and self._badge_event_links(cyber, self.events["AC-0224-001"])
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
        active_case.next_human_check = next_actions["verify_now"]

        report_linked = "IR-0231-001" in injected_event_ids and self._report_event_links(badge, self.events["IR-0231-001"])
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
        active_case.next_human_check = next_actions["escalate_now"]
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
        identity = self.reference["identity_record"]
        badge_mapping = self.reference["badge_mapping"]
        door_mapping = self.reference["door_mapping"]
        trigger_matches = cyber["event_type"] == "vendor_remote_access_anomaly"
        identity_matches = cyber["account"] == identity["account"]
        badge_matches = badge["badge_id"] == badge_mapping["badge_id"] == identity["badge_id"]
        door_matches = badge["door_id"] == door_mapping["door_id"]
        within_window = self._minutes_between(cyber["occurred_at"], badge["occurred_at"]) <= 30
        return all([trigger_matches, identity_matches, badge_matches, door_matches, within_window])

    def _report_event_links(self, badge: dict[str, Any], report: dict[str, Any]) -> bool:
        door_mapping = self.reference["door_mapping"]
        zone_adjacency = self.reference["zone_adjacency"]
        same_campus = badge["campus_id"] == report["campus_id"]
        within_window = self._minutes_between(badge["occurred_at"], report["occurred_at"]) <= 15
        adjacent_zone = (
            door_mapping["zone_id"] == zone_adjacency["from_zone_id"]
            and report["zone_id"] == zone_adjacency["to_zone_id"]
        )
        same_building = door_mapping["building_id"] == zone_adjacency["building_id"]
        return all([same_campus, within_window, adjacent_zone, same_building])

    @staticmethod
    def _minutes_between(start: str, end: str) -> float:
        return (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60


engine = CaseEngine()
