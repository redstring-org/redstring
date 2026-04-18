from pydantic import BaseModel


class Alert(BaseModel):
    id: str
    title: str
    summary: str
    facility_id: str
    confidence: float
    matched_event_count: int
    source_types: list[str]
    event_ids: list[str]
    why_connected: list[str]