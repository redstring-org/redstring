from app.models.alert import Alert
from app.models.event import Event, Location


class MemoryStore:
    def __init__(self) -> None:
        self.events: list[Event] = self._initial_events()
        self.alerts: list[Alert] = []

    def _initial_events(self) -> list[Event]:
        return [
            Event(
                id="evt_001",
                source_type="cyber",
                event_type="failed_login",
                timestamp="2026-04-19T11:03:00Z",
                location=Location(lat=38.87, lon=-77.04),
                facility_id="hospital_alpha",
                severity=0.62,
                text="Multiple failed logins observed in hospital records system."
            )
        ]

    def list_events(self) -> list[Event]:
        return self.events

    def add_event(self, event: Event) -> Event:
        self.events.append(event)
        return event

    def get_event(self, event_id: str) -> Event | None:
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def list_alerts(self) -> list[Alert]:
        return self.alerts

    def get_alert(self, alert_id: str) -> Alert | None:
        for alert in self.alerts:
            if alert.id == alert_id:
                return alert
        return None

    def replace_alerts(self, alerts: list[Alert]) -> list[Alert]:
        self.alerts = alerts
        return self.alerts

    def reset(self) -> list[Event]:
        self.events = self._initial_events()
        self.alerts = []
        return self.events