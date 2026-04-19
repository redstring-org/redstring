from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import evaluation_engine  # noqa: F401
from ..domain.case_engine import engine
from ..event_signal import raw_event_received
from ..raw_event_store import raw_event_store
from ..schemas import (
    ActiveCaseResponse,
    CaseGroupResponse,
    CaseGroupsResponse,
    InjectEventRequest,
    LiveEventResponse,
    LiveEventsResponse,
)


router = APIRouter(prefix="/api")


@router.get("/case/active", response_model=ActiveCaseResponse)
def get_active_case() -> ActiveCaseResponse:
    return engine.build_active_case()


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
        return engine.build_active_case()

    if not raw_payload:
        raise HTTPException(status_code=400, detail="Inject payload must include event_id or a raw event body.")

    saved_row_id = raw_event_store.save(payload_data)
    raw_event_received.emit(saved_row_id)
    return engine.build_active_case()


@router.post("/demo/reset", response_model=ActiveCaseResponse)
def reset_demo() -> ActiveCaseResponse:
    raw_event_store.reset()
    return engine.build_active_case()


@router.get("/events/live", response_model=LiveEventsResponse)
def get_live_events() -> LiveEventsResponse:
    result = raw_event_store.list_recent_events()
    return LiveEventsResponse(
        total=result["total"],
        events=[LiveEventResponse.from_raw(row) for row in result["events"]],
    )


@router.get("/case-groups", response_model=CaseGroupsResponse)
def get_case_groups() -> CaseGroupsResponse:
    groups = raw_event_store.list_case_groups()
    case_groups: list[CaseGroupResponse] = []
    for group in groups:
        case_group_id = str(group["case_group_id"])
        event_row_ids = raw_event_store.list_case_group_event_ids(case_group_id)
        case_groups.append(
            CaseGroupResponse(
                case_group_id=case_group_id,
                anchor_location=str(group["anchor_location"]),
                opened_at=group["opened_at"],
                updated_at=group["updated_at"],
                qualified_at=group["qualified_at"],
                qualification_rank=group["qualification_rank"],
                event_row_ids=event_row_ids,
                event_count=len(event_row_ids),
            )
        )
    return CaseGroupsResponse(
        total=len(groups),
        case_groups=case_groups,
    )
