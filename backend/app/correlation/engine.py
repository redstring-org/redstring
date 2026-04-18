from datetime import datetime

from app.models.event import Event


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def has_cross_domain_correlation(
    events: list[Event],
    window_minutes: int = 30,
) -> bool:
    by_facility: dict[str, list[Event]] = {}

    for event in events:
        by_facility.setdefault(event.facility_id, []).append(event)

    for facility_events in by_facility.values():
        facility_events = sorted(facility_events, key=lambda e: parse_ts(e.timestamp))

        for i, start_event in enumerate(facility_events):
            start_time = parse_ts(start_event.timestamp)
            source_types = {start_event.source_type}

            for candidate in facility_events[i + 1:]:
                delta_minutes = (parse_ts(candidate.timestamp) - start_time).total_seconds() / 60
                if delta_minutes > window_minutes:
                    break
                source_types.add(candidate.source_type)

            if len(source_types) >= 2:
                return True

    return False