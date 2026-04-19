from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class TimelineItem(BaseModel):
    event_id: str
    timestamp: str
    summary: str
    source: str


class ProvenanceItem(BaseModel):
    event_id: str
    label: str
    source: str
    timestamp: str


class ActiveCaseResponse(BaseModel):
    case_id: str
    case_title: str
    location: str
    state: Optional[str]
    primary_subject: str
    trigger_summary: str
    timeline: list[TimelineItem]
    why_linked: list[str]
    what_weakens_it: list[str]
    next_human_check: str
    escalation_recommendation: Optional[str]
    provenance: list[ProvenanceItem]
    osint_enabled: bool


class InjectEventRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    staff_id: Optional[int | str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_title: Optional[str] = None
    role_category: Optional[str] = None
    department: Optional[str] = None
    shift: Optional[str] = None
    door_name: Optional[str] = None
    category: Optional[str] = None
    area: Optional[str] = None
    door_type: Optional[str] = None
    badge_required: Optional[str] = None
    action: Optional[str] = None
    access_result: Optional[str] = None

    def raw_payload(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True, exclude={"event_id"})
