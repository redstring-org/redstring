from __future__ import annotations


class DemoStateStore:
    def __init__(self) -> None:
        self._event_ids: list[str] = []

    def inject(self, event_id: str) -> list[str]:
        if event_id not in self._event_ids:
            self._event_ids.append(event_id)
        return self.snapshot()

    def reset(self) -> None:
        self._event_ids = []

    def snapshot(self) -> list[str]:
        return list(self._event_ids)


store = DemoStateStore()
