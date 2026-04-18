from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


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
    event_id: str
