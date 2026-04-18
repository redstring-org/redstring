from fastapi import APIRouter, Request

from app.models.event import Event, Location

router = APIRouter(prefix="/simulate", tags=["simulate"])


@router.post("/seed", response_model=Event)
def seed_event(request: Request) -> Event:
    store = request.app.state.store
    event_number = len(store.list_events()) + 1

    event = Event(
        id=f"evt_{event_number:03d}",
        source_type="physical",
        event_type="equipment_failure",
        timestamp="2026-04-19T11:15:00Z",
        location=Location(lat=38.871, lon=-77.041),
        facility_id="hospital_alpha",
        severity=0.71,
        text="Ventilator system fault reported in ICU.",
    )
    return store.add_event(event)


@router.post("/seed-osint", response_model=Event)
def seed_osint_event(request: Request) -> Event:
    store = request.app.state.store
    event_number = len(store.list_events()) + 1

    event = Event(
        id=f"evt_{event_number:03d}",
        source_type="osint",
        event_type="social_post",
        timestamp="2026-04-19T11:18:00Z",
        location=Location(lat=38.872, lon=-77.039),
        facility_id="hospital_alpha",
        severity=0.54,
        text="Posts mention ER delays and ambulances queued outside hospital.",
        raw_payload={"platform": "x", "post_count": 6},
    )
    return store.add_event(event)


@router.post("/reset", response_model=list[Event])
def reset_events(request: Request) -> list[Event]:
    return request.app.state.store.reset()