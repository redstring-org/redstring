from typing import Any


class MemoryStore:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.alerts: list[dict[str, Any]] = []

    def list_events(self) -> list[dict[str, Any]]:
        return self.events