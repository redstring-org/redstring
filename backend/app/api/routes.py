from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.domain.case_engine import engine
from app.schemas import ActiveCaseResponse, InjectEventRequest
from app.state_store import store


router = APIRouter(prefix="/api")


@router.get("/case/active", response_model=ActiveCaseResponse)
def get_active_case() -> ActiveCaseResponse:
    return engine.build_case(store.snapshot())


@router.post("/demo/inject", response_model=ActiveCaseResponse)
def inject_event(payload: InjectEventRequest) -> ActiveCaseResponse:
    try:
        engine.validate_injectable_event(payload.event_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return engine.build_case(store.inject(payload.event_id))


@router.post("/demo/reset", response_model=ActiveCaseResponse)
def reset_demo() -> ActiveCaseResponse:
    store.reset()
    return engine.build_case(store.snapshot())
