from __future__ import annotations

from typing import Callable


class EventSignal:
    def __init__(self) -> None:
        self._subscribers: list[Callable[[int], None]] = []

    def subscribe(self, handler: Callable[[int], None]) -> None:
        self._subscribers.append(handler)

    def emit(self, event_row_id: int) -> None:
        for handler in self._subscribers:
            handler(event_row_id)


raw_event_received = EventSignal()
