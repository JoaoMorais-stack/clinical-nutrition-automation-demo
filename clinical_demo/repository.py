from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class SQLiteRunRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._migrate()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _migrate(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS demo_runs (
                    run_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    total_cases INTEGER NOT NULL,
                    alerts INTEGER NOT NULL,
                    follow_ups INTEGER NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )

    def save(self, report: dict[str, Any]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO demo_runs (
                    run_id, created_at, mode, total_cases, alerts,
                    follow_ups, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report["run_id"],
                    report["created_at"],
                    report["mode"],
                    report["summary"]["total_cases"],
                    report["summary"]["alerts"],
                    report["summary"]["follow_ups"],
                    json.dumps(report, ensure_ascii=False),
                ),
            )

    def latest(self) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload_json FROM demo_runs ORDER BY created_at DESC, rowid DESC LIMIT 1"
            ).fetchone()
        return json.loads(row["payload_json"]) if row else None

    def history(self, limit: int = 8) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT run_id, created_at, mode, total_cases, alerts, follow_ups
                FROM demo_runs
                ORDER BY created_at DESC, rowid DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def count(self) -> int:
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM demo_runs").fetchone()
        return int(row["total"])

    def reset(self) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM demo_runs")
