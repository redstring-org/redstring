from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import evaluation_engine  # noqa: F401
from ..domain.case_engine import engine
from ..event_signal import raw_event_received
from ..raw_event_store import raw_event_store
from ..schemas import ActiveCaseResponse, InjectEventRequest
from ..state_store import store


router = APIRouter(prefix="/api")


@router.get("/case/active", response_model=ActiveCaseResponse)
def get_active_case() -> ActiveCaseResponse:
    return engine.build_case(store.snapshot())


@router.post("/demo/inject", response_model=ActiveCaseResponse)
def inject_event(payload: InjectEventRequest) -> ActiveCaseResponse:
    payload_data = payload.model_dump(exclude_none=True)
    raw_payload = payload.raw_payload()

    if not payload_data:
        raise HTTPException(status_code=400, detail="Inject payload must include event_id or a raw event body.")

    if payload.event_id:
        try:
            event_id = engine.resolve_injectable_event_id(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        saved_row_id = raw_event_store.save(payload_data)
        raw_event_received.emit(saved_row_id)
        return engine.build_case(store.inject(event_id))

    if not raw_payload:
        raise HTTPException(status_code=400, detail="Inject payload must include event_id or a raw event body.")

    saved_row_id = raw_event_store.save(payload_data)
    raw_event_received.emit(saved_row_id)
    return engine.build_case(store.snapshot())


@router.post("/demo/reset", response_model=ActiveCaseResponse)
def reset_demo() -> ActiveCaseResponse:
    store.reset()
    raw_event_store.reset()
    return engine.build_case(store.snapshot())
