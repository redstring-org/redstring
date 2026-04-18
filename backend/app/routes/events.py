from fastapi import APIRouter, Request

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(request: Request) -> list[dict]:
    return request.app.state.store.list_events()