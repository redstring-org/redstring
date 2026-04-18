from fastapi import APIRouter, Request, HTTPException

from app.models.event import Event

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[Event])
def list_events(request: Request) -> list[Event]:
    return request.app.state.store.list_events()


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: str, request: Request) -> Event:
    event = request.app.state.store.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event