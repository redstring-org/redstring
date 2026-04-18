from app.models.event import Event, Location


class MemoryStore:
    def __init__(self) -> None:
        self.events: list[Event] = self._initial_events()
        self.alerts: list[dict] = []

    def _initial_events(self) -> list[Event]:
        return [
            Event(
                id="evt_001",
                source_type="cyber",
                event_type="failed_login",
                timestamp="2026-04-19T11:03:00Z",
                location=Location(lat=38.87, lon=-77.04),
                facility_id="port_alpha",
                severity=0.62,
                text="Multiple failed logins observed in port ops system.",
            )
        ]

    def list_events(self) -> list[Event]:
        return self.events

    def add_event(self, event: Event) -> Event:
        self.events.append(event)
        return event

    def reset(self) -> list[Event]:
        self.events = self._initial_events()
        self.alerts = []
        return self.events