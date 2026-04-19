from __future__ import annotations

from typing import Any

from ..config import settings
from ..fixtures.loader import load_gold_events
from ..raw_event_store import raw_event_store
from ..schemas import ActiveCaseResponse, InjectEventRequest, ProvenanceItem, TimelineItem


class CaseEngine:
    def __init__(self) -> None:
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

    def build_active_case(self) -> ActiveCaseResponse:
        qualified_group = raw_event_store.get_first_qualified_case_group()
        if qualified_group is None:
            return self._empty_case()

        events = raw_event_store.list_case_group_events(str(qualified_group["case_group_id"]))
        return self._build_case_from_group(qualified_group, events)

    def _empty_case(self) -> ActiveCaseResponse:
        return ActiveCaseResponse(
            case_id="CASE-GROUP-PENDING",
            case_title="Awaiting qualified correlated case group",
            location="",
            state=None,
            primary_subject="Unknown subject",
            trigger_summary="No case group has reached the minimum threshold of 3 linked events yet.",
            timeline=[],
            why_linked=[],
            what_weakens_it=[],
            next_human_check="",
            escalation_recommendation=None,
            provenance=[],
            osint_enabled=settings.enable_osint_context,
        )

    def _build_case_from_group(
        self,
        case_group: dict[str, Any],
        events: list[dict[str, Any]],
    ) -> ActiveCaseResponse:
        event_count = len(events)
        event_kinds = {str(event["payload_kind"]) for event in events}
        location = self._derive_location(case_group, events)

        active_case = ActiveCaseResponse(
            case_id=str(case_group["case_group_id"]),
            case_title="Observed correlated case group requiring review",
            location=location,
            state="Observe",
            primary_subject=self._derive_primary_subject(events),
            trigger_summary=self._build_trigger_summary(event_count, event_kinds),
            timeline=[self._timeline_item(event) for event in events],
            why_linked=self._build_why_linked(event_count, event_kinds),
            what_weakens_it=self._build_what_weakens_it(event_kinds),
            next_human_check=self._build_next_human_check(location, event_kinds),
            escalation_recommendation=None,
            provenance=[self._provenance_item(event) for event in events],
            osint_enabled=settings.enable_osint_context,
        )
        return active_case

    def _build_trigger_summary(self, event_count: int, event_kinds: set[str]) -> str:
        kind_labels = ", ".join(self._kind_display_name(kind) for kind in sorted(event_kinds))
        return f"Case group qualified after {event_count} linked events: {kind_labels}."

    def _build_why_linked(self, event_count: int, event_kinds: set[str]) -> list[str]:
        why_linked = [f"Case group reached the qualification threshold with {event_count} linked events"]
        if "badge_access" in event_kinds:
            why_linked.append("Badge-access activity is present in the qualified case group")
        if "suspicious_person_report" in event_kinds:
            why_linked.append("Suspicious-person reporting is present in the qualified case group")
        if "osint_post" in event_kinds:
            why_linked.append("OSINT context is present in the qualified case group")
        if "demo_event_id" in event_kinds:
            why_linked.append("Demo event traffic is linked into the qualified case group")
        if "raw_event" in event_kinds:
            why_linked.append("Additional raw event activity is linked into the qualified case group")
        return why_linked

    def _build_what_weakens_it(self, event_kinds: set[str]) -> list[str]:
        weak_points: list[str] = []
        if "badge_access" not in event_kinds:
            weak_points.append("Badge-access evidence is not present in the qualified case group")
        if "suspicious_person_report" not in event_kinds:
            weak_points.append("Suspicious-person reporting is not present in the qualified case group")
        if "osint_post" not in event_kinds:
            weak_points.append("OSINT context is not present in the qualified case group")
        if not weak_points:
            weak_points.append("Identity-level correlation across the grouped events still requires operator review")
        return weak_points

    def _build_next_human_check(self, location: str, event_kinds: set[str]) -> str:
        evidence = []
        if "badge_access" in event_kinds:
            evidence.append("badge activity")
        if "osint_post" in event_kinds:
            evidence.append("OSINT context")
        if "suspicious_person_report" in event_kinds:
            evidence.append("suspicious-person reporting")
        if not evidence:
            evidence.append("the linked events")

        evidence_summary = ", ".join(evidence[:-1]) + (f", and {evidence[-1]}" if len(evidence) > 1 else evidence[0])
        if location:
            return (
                f"Review {evidence_summary} now to confirm whether they describe the same onsite activity near "
                f"{location}."
            )
        return f"Review {evidence_summary} now to confirm whether they describe the same onsite activity."

    def _derive_location(self, case_group: dict[str, Any], events: list[dict[str, Any]]) -> str:
        if case_group.get("anchor_location"):
            return str(case_group["anchor_location"])

        seen: list[str] = []
        for event in events:
            payload = dict(event["payload"])
            for key in ("location", "location_label", "area", "door_name"):
                value = payload.get(key)
                if value:
                    text = str(value)
                    if text not in seen:
                        seen.append(text)
        return " / ".join(seen[:2])

    def _derive_primary_subject(self, events: list[dict[str, Any]]) -> str:
        for event in events:
            payload = dict(event["payload"])
            if event["payload_kind"] == "badge_access":
                full_name = f"{payload.get('first_name', '')} {payload.get('last_name', '')}".strip()
                if full_name:
                    return full_name
                if payload.get("staff_id"):
                    return f"Staff ID {payload['staff_id']}"
            if event["payload_kind"] == "demo_event_id" and payload.get("event_id"):
                return f"Demo event {payload['event_id']}"
        return "Unknown subject"

    def _timeline_item(self, event: dict[str, Any]) -> TimelineItem:
        return TimelineItem(
            event_id=self._event_identifier(event),
            timestamp=str(event["event_timestamp"]),
            summary=self._event_summary(event),
            source=self._event_source(event),
        )

    def _provenance_item(self, event: dict[str, Any]) -> ProvenanceItem:
        return ProvenanceItem(
            event_id=self._event_identifier(event),
            label=self._provenance_label(event),
            source=self._event_source(event),
            timestamp=str(event["event_timestamp"]),
        )

    def _event_identifier(self, event: dict[str, Any]) -> str:
        external_id = event.get("external_id")
        if external_id:
            return str(external_id)
        return f"event-row-{event['id']}"

    def _event_source(self, event: dict[str, Any]) -> str:
        payload = dict(event["payload"])
        kind = str(event["payload_kind"])
        if kind == "badge_access":
            return "Badge Access"
        if kind == "suspicious_person_report":
            return "Officer Report"
        if kind == "osint_post":
            return str(payload.get("screen_name") or payload.get("username") or "OSINT")
        if kind == "demo_event_id":
            return "Demo Event Injection"
        return kind

    def _provenance_label(self, event: dict[str, Any]) -> str:
        labels = {
            "badge_access": "Badge/access event",
            "suspicious_person_report": "Suspicious-person report",
            "osint_post": "OSINT post",
            "demo_event_id": "Injected demo event",
            "raw_event": "Raw event",
        }
        return labels.get(str(event["payload_kind"]), "Raw event")

    def _event_summary(self, event: dict[str, Any]) -> str:
        payload = dict(event["payload"])
        kind = str(event["payload_kind"])

        if kind == "badge_access":
            name = f"{payload.get('first_name', '')} {payload.get('last_name', '')}".strip() or payload.get(
                "staff_id", "Unknown badgeholder"
            )
            door = payload.get("door_name") or payload.get("area") or "unknown door"
            result = payload.get("access_result")
            if result:
                return f"{name} - {door} ({result})"
            return f"{name} - {door}"

        if kind == "suspicious_person_report":
            location = payload.get("location") or "unknown location"
            description = payload.get("description") or "Suspicious-person report received."
            return f"{location}: {description}"

        if kind == "osint_post":
            text = str(payload.get("text") or payload.get("content") or "").strip()
            return text[:120] if text else "OSINT post received."

        if kind == "demo_event_id":
            event_id = payload.get("event_id", "unknown")
            return f"Injected demo event {event_id}"

        return str(payload)[:120]

    def _kind_display_name(self, kind: str) -> str:
        names = {
            "badge_access": "Badge Access",
            "suspicious_person_report": "Suspicious-Person Report",
            "osint_post": "OSINT",
            "demo_event_id": "Demo Event",
            "raw_event": "Raw Event",
        }
        return names.get(kind, kind)


engine = CaseEngine()
