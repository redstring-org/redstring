from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .event_signal import raw_event_received
from .raw_event_store import raw_event_store

LOCATION_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {"the", "and", "for", "near", "with", "main", "service", "hospital"}


@dataclass(frozen=True)
class StoredEvent:
    row_id: int
    payload_kind: str
    external_id: str | None
    event_timestamp: str | None
    payload: dict[str, Any]

    @property
    def occurred_at(self) -> datetime | None:
        if not self.event_timestamp:
            return None
        return _parse_iso_timestamp(self.event_timestamp)

    @property
    def location_hint(self) -> str:
        payload = self.payload
        for key in ("location", "location_label", "area", "door_name"):
            value = payload.get(key)
            if value:
                return str(value)
        return ""


class EvaluationEngine:
    def handle_new_event(self, event_row_id: int) -> None:
        stored = raw_event_store.get_event(event_row_id)
        if stored is None:
            return
        event = StoredEvent(
            row_id=int(stored["id"]),
            payload_kind=str(stored["payload_kind"]),
            external_id=stored["external_id"],
            event_timestamp=stored["event_timestamp"],
            payload=dict(stored["payload"]),
        )

        matching_group_id = self._find_matching_case_group(event)
        if matching_group_id is None:
            matching_group_id = raw_event_store.create_case_group(
                anchor_timestamp=event.event_timestamp,
                anchor_location=event.location_hint,
            )

        raw_event_store.link_event_to_case_group(
            case_group_id=matching_group_id,
            event_row_id=event.row_id,
            event_timestamp=event.event_timestamp,
            anchor_location=event.location_hint,
        )

    def _find_matching_case_group(self, event: StoredEvent) -> str | None:
        if event.occurred_at is None:
            return None

        for group in raw_event_store.list_case_groups():
            group_timestamp = _parse_iso_timestamp(group["updated_at"]) if group["updated_at"] else None
            if group_timestamp is None:
                continue

            minutes_apart = abs((event.occurred_at - group_timestamp).total_seconds()) / 60
            if minutes_apart > 30:
                continue

            if _locations_related(event.location_hint, group["anchor_location"]):
                return str(group["case_group_id"])

        for group in raw_event_store.list_case_groups():
            group_timestamp = _parse_iso_timestamp(group["updated_at"]) if group["updated_at"] else None
            if group_timestamp is None:
                continue

            minutes_apart = abs((event.occurred_at - group_timestamp).total_seconds()) / 60
            if minutes_apart <= 10:
                return str(group["case_group_id"])

        return None


def _parse_iso_timestamp(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z") and ("+" in normalized[10:] or "-" in normalized[10:]):
        normalized = normalized[:-1]
    elif normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    return datetime.fromisoformat(normalized).astimezone(timezone.utc)


def _normalize_location(value: str) -> set[str]:
    if not value:
        return set()
    return {
        token
        for token in LOCATION_TOKEN_PATTERN.findall(value.lower())
        if token not in STOP_WORDS and len(token) > 2
    }


def _locations_related(left: str, right: str) -> bool:
    if not left or not right:
        return False

    left_tokens = _normalize_location(left)
    right_tokens = _normalize_location(right)
    if not left_tokens or not right_tokens:
        return False

    overlap = left_tokens & right_tokens
    if overlap:
        return True

    return left.strip().lower() == right.strip().lower()


evaluation_engine = EvaluationEngine()
raw_event_received.subscribe(evaluation_engine.handle_new_event)
