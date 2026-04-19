from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class LiveEventResponse(BaseModel):
    id: int
    kind: str
    timestamp: Optional[str]
    summary: str
    source: str

    @classmethod
    def from_raw(cls, row: dict[str, Any]) -> "LiveEventResponse":
        p = row["payload"]
        kind = row["kind"]

        if kind == "badge_access":
            name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or p.get("staff_id", "unknown")
            door = p.get("door_name", p.get("area", "unknown door"))
            result = p.get("access_result", "")
            summary = f"{name} — {door}" + (f" ({result})" if result else "")
            source = "Badge Access"
        elif kind == "suspicious_person_report":
            desc = p.get("description", "")
            loc = p.get("location", "")
            summary = f"{loc}: {desc}" if loc else desc
            source = "Officer Report"
        elif kind == "osint_post":
            summary = p.get("text", p.get("content", ""))[:120]
            source = p.get("username", "OSINT")
        else:
            summary = str(p)[:120]
            source = kind

        return cls(
            id=row["id"],
            kind=kind,
            timestamp=row.get("timestamp"),
            summary=summary,
            source=source,
        )


class LiveEventsResponse(BaseModel):
    total: int
    events: list["LiveEventResponse"]


class CaseGroupResponse(BaseModel):
    case_group_id: str
    anchor_location: str
    opened_at: Optional[str]
    updated_at: Optional[str]
    qualified_at: Optional[str]
    qualification_rank: Optional[int]
    event_row_ids: list[int]
    event_count: int


class CaseGroupsResponse(BaseModel):
    total: int
    case_groups: list["CaseGroupResponse"]


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
