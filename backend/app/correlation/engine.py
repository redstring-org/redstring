from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from app.models.alert import Alert
from app.models.event import Event


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def find_all_cross_domain_clusters(
    events: list[Event],
    window_minutes: int = 30,
) -> list[list[Event]]:
    by_facility: dict[str, list[Event]] = {}

    for event in events:
        by_facility.setdefault(event.facility_id, []).append(event)

    clusters: list[list[Event]] = []

    for facility_events in by_facility.values():
        facility_events = sorted(facility_events, key=lambda e: parse_ts(e.timestamp))

        for i, start_event in enumerate(facility_events):
            start_time = parse_ts(start_event.timestamp)
            cluster = [start_event]
            source_types = {start_event.source_type}

            for candidate in facility_events[i + 1:]:
                delta = (parse_ts(candidate.timestamp) - start_time).total_seconds() / 60
                if delta > window_minutes:
                    break

                cluster.append(candidate)
                source_types.add(candidate.source_type)

            if len(source_types) >= 2:
                clusters.append(cluster)

    return clusters

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * (2 * atan2(sqrt(a), sqrt(1 - a)))

def build_basic_alert(cluster: list[Event]) -> Alert | None:
    if not cluster:
        return None

    facility_id = cluster[0].facility_id
    source_types = sorted({event.source_type for event in cluster})

    confidence = min(0.95, 0.4 + 0.15 * len(source_types) + 0.03 * len(cluster))
    facility_name = facility_id.replace("_", " ").title()

    # --- NEW: context detection ---
    texts = " ".join(e.text.lower() for e in cluster)

    if "icu" in texts or "ventilator" in texts:
        context = "ICU systems"
    elif "er" in texts or "ambulance" in texts:
        context = "ER operations"
    else:
        context = "hospital operations"
    
    why_connected = []

    for event in cluster:
        if event.source_type == "cyber":
            why_connected.append(event.text)
        elif event.source_type == "physical":
            why_connected.append(event.text)
        elif event.source_type == "osint":
            why_connected.append(event.text)

    why_connected = list(dict.fromkeys(why_connected))[:3]

    times = [parse_ts(e.timestamp) for e in cluster]
    time_span_min = int((max(times) - min(times)).total_seconds() / 60)

    max_dist = 0.0
    for i in range(len(cluster)):
        for j in range(i + 1, len(cluster)):
            a = cluster[i].location
            b = cluster[j].location
            dist = haversine_km(a.lat, a.lon, b.lat, b.lon)
            max_dist = max(max_dist, dist)

    max_dist = round(max_dist, 2)

    summary = (
        f"{len(cluster)} events across {len(source_types)} domains "
        f"indicate disruption to {context} at {facility_name}. "
        f"Signals occurred within {time_span_min} minutes "
        f"and {max_dist} km ({', '.join(source_types)})."
    )

    return Alert(
        id=f"alert_{facility_id}",
        title=f"Possible coordinated activity at {facility_name}",
        summary=summary,
        facility_id=facility_id,
        confidence=round(confidence, 2),
        matched_event_count=len(cluster),
        source_types=source_types,
        event_ids=[event.id for event in cluster],
        why_connected=why_connected,
    )