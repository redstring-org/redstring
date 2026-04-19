from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from .config import settings


class RawEventStore:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or settings.demo_events_db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS injected_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payload_kind TEXT NOT NULL,
                    external_id TEXT,
                    event_timestamp TEXT,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS case_groups (
                    case_group_id TEXT PRIMARY KEY,
                    anchor_location TEXT,
                    opened_at TEXT,
                    updated_at TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS case_group_events (
                    case_group_id TEXT NOT NULL,
                    event_row_id INTEGER NOT NULL UNIQUE,
                    linked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (case_group_id, event_row_id),
                    FOREIGN KEY (case_group_id) REFERENCES case_groups(case_group_id),
                    FOREIGN KEY (event_row_id) REFERENCES injected_events(id)
                )
                """
            )

    def save(self, payload: dict[str, Any]) -> int:
        normalized_payload = dict(payload)
        payload_kind = self._classify(normalized_payload)
        external_id = (
            normalized_payload.get("event_id")
            or normalized_payload.get("report_id")
            or normalized_payload.get("post_id")
            or normalized_payload.get("staff_id")
        )
        event_timestamp = (
            normalized_payload.get("occurred_at")
            or normalized_payload.get("timestamp")
            or normalized_payload.get("posted_at")
        )
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO injected_events (payload_kind, external_id, event_timestamp, payload_json)
                VALUES (?, ?, ?, ?)
                """,
                (
                    payload_kind,
                    str(external_id) if external_id is not None else None,
                    str(event_timestamp) if event_timestamp is not None else None,
                    json.dumps(normalized_payload, sort_keys=True),
                ),
            )
            return int(cursor.lastrowid)

    def count(self) -> int:
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) FROM injected_events").fetchone()
        return int(row[0]) if row else 0

    def latest_payload(self) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload_json FROM injected_events ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if not row:
            return None
        return json.loads(row[0])

    def reset(self) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM case_group_events")
            connection.execute("DELETE FROM case_groups")
            connection.execute("DELETE FROM injected_events")

    def get_event(self, event_row_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, payload_kind, external_id, event_timestamp, payload_json
                FROM injected_events
                WHERE id = ?
                """,
                (event_row_id,),
            ).fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "payload_kind": row[1],
            "external_id": row[2],
            "event_timestamp": row[3],
            "payload": json.loads(row[4]),
        }

    def create_case_group(self, anchor_timestamp: str | None, anchor_location: str) -> str:
        case_group_id = f"raw-case-{uuid.uuid4().hex[:12]}"
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO case_groups (case_group_id, anchor_location, opened_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (case_group_id, anchor_location or None, anchor_timestamp, anchor_timestamp),
            )
        return case_group_id

    def link_event_to_case_group(
        self,
        *,
        case_group_id: str,
        event_row_id: int,
        event_timestamp: str | None,
        anchor_location: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO case_group_events (case_group_id, event_row_id)
                VALUES (?, ?)
                """,
                (case_group_id, event_row_id),
            )
            connection.execute(
                """
                UPDATE case_groups
                SET updated_at = COALESCE(?, updated_at),
                    anchor_location = CASE
                        WHEN anchor_location IS NULL OR anchor_location = '' THEN COALESCE(?, anchor_location)
                        ELSE anchor_location
                    END
                WHERE case_group_id = ?
                """,
                (event_timestamp, anchor_location or None, case_group_id),
            )

    def list_case_groups(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT case_group_id, anchor_location, opened_at, updated_at
                FROM case_groups
                ORDER BY COALESCE(updated_at, opened_at) DESC, case_group_id DESC
                """
            ).fetchall()
        return [
            {
                "case_group_id": row[0],
                "anchor_location": row[1] or "",
                "opened_at": row[2],
                "updated_at": row[3],
            }
            for row in rows
        ]

    def list_case_group_event_ids(self, case_group_id: str) -> list[int]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT event_row_id
                FROM case_group_events
                WHERE case_group_id = ?
                ORDER BY event_row_id ASC
                """,
                (case_group_id,),
            ).fetchall()
        return [int(row[0]) for row in rows]

    def list_recent_events(self, *, limit: int = 100) -> dict[str, Any]:
        with self._connect() as connection:
            total_row = connection.execute(
                "SELECT COUNT(*) FROM injected_events WHERE payload_kind != 'demo_event_id'"
            ).fetchone()
            total = int(total_row[0]) if total_row else 0
            rows = connection.execute(
                """
                SELECT id, payload_kind, external_id, event_timestamp, payload_json, created_at
                FROM injected_events
                WHERE payload_kind != 'demo_event_id'
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        events = [
            {
                "id": row[0],
                "kind": row[1],
                "external_id": row[2],
                "timestamp": row[3] or row[5],
                "payload": json.loads(row[4]),
            }
            for row in reversed(rows)
        ]
        return {"total": total, "events": events}

    @staticmethod
    def _classify(payload: dict[str, Any]) -> str:
        if payload.get("event_id"):
            return "demo_event_id"
        if payload.get("report_id"):
            return "suspicious_person_report"
        if payload.get("post_id"):
            return "osint_post"
        if payload.get("staff_id"):
            return "badge_access"
        return "raw_event"


raw_event_store = RawEventStore()
