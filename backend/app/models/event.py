from pydantic import BaseModel, Field


class Location(BaseModel):
    lat: float
    lon: float


class Event(BaseModel):
    id: str
    source_type: str
    event_type: str
    timestamp: str
    location: Location
    facility_id: str
    severity: float
    text: str
    raw_payload: dict = Field(default_factory=dict)