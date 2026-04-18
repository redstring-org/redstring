from fastapi import APIRouter, Request

from app.models.event import Event

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[Event])
def list_events(request: Request) -> list[Event]:
    return request.app.state.store.list_events()