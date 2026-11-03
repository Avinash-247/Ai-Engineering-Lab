import json
import sqlite3
import threading
from typing import Any, Iterable, Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS keys (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_key TEXT NOT NULL,
    session_id  TEXT NOT NULL,
    subpath     TEXT
);

-- COALESCE makes NULL subpaths count as equal (plain UNIQUE treats NULLs as distinct in SQLite)
CREATE UNIQUE INDEX IF NOT EXISTS idx_keys_unique
    ON keys (project_key, session_id, COALESCE(subpath, ''));

CREATE TABLE IF NOT EXISTS entries (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    key_id     INTEGER NOT NULL REFERENCES keys(id) ON DELETE CASCADE,
    entry      TEXT NOT NULL CHECK (json_valid(entry)),
    created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_entries_key_id
    ON entries (key_id);

CREATE TABLE IF NOT EXISTS summaries (
    key_id     INTEGER PRIMARY KEY REFERENCES keys(id) ON DELETE CASCADE,
    summary    TEXT NOT NULL CHECK (json_valid(summary)),
    updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
"""


class SQLiteSessionStore:
    """Stores session entries and summaries in a SQLite database.

    Data is organised by a key of (project_key, session_id, subpath).
    Each key has any number of entries (append-only JSON documents) and
    at most one summary (a JSON document).
    """

    def __init__(self, path: str = "session.db") -> None:
        self.path = path
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------ keys

    def _key_id(
        self,
        project_key: str,
        session_id: str,
        subpath: Optional[str] = None,
        create: bool = False,
    ) -> Optional[int]:
        if create:
            self._conn.execute(
                "INSERT INTO keys (project_key, session_id, subpath) "
                "VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
                (project_key, session_id, subpath),
            )
        row = self._conn.execute(
            "SELECT id FROM keys "
            "WHERE project_key = ? AND session_id = ? "
            "AND COALESCE(subpath, '') = COALESCE(?, '')",
            (project_key, session_id, subpath),
        ).fetchone()
        return row["id"] if row else None

    # --------------------------------------------------------------- entries

    def append(
        self,
        project_key: str,
        session_id: str,
        entry: Any,
        subpath: Optional[str] = None,
    ) -> int:
        """Append one entry and return its row id."""
        return self.append_many(project_key, session_id, [entry], subpath)[0]

    def append_many(
        self,
        project_key: str,
        session_id: str,
        entries: Iterable[Any],
        subpath: Optional[str] = None,
    ) -> list[int]:
        """Append several entries in one transaction and return their row ids."""
        with self._lock, self._conn:
            key_id = self._key_id(project_key, session_id, subpath, create=True)
            ids = []
            for entry in entries:
                cur = self._conn.execute(
                    "INSERT INTO entries (key_id, entry) VALUES (?, ?)",
                    (key_id, json.dumps(entry)),
                )
                ids.append(cur.lastrowid)
            return ids

    def load(
        self,
        project_key: str,
        session_id: str,
        subpath: Optional[str] = None,
    ) -> list[Any]:
        """Return all entries for a key, oldest first."""
        with self._lock:
            key_id = self._key_id(project_key, session_id, subpath)
            if key_id is None:
                return []
            rows = self._conn.execute(
                "SELECT entry FROM entries WHERE key_id = ? ORDER BY id",
                (key_id,),
            ).fetchall()
        return [json.loads(r["entry"]) for r in rows]

    # ------------------------------------------------------------- summaries

    def set_summary(
        self,
        project_key: str,
        session_id: str,
        summary: Any,
        subpath: Optional[str] = None,
    ) -> None:
        """Create or replace the summary for a key."""
        with self._lock, self._conn:
            key_id = self._key_id(project_key, session_id, subpath, create=True)
            self._conn.execute(
                "INSERT INTO summaries (key_id, summary) VALUES (?, ?) "
                "ON CONFLICT (key_id) DO UPDATE SET "
                "summary = excluded.summary, "
                "updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')",
                (key_id, json.dumps(summary)),
            )

    def get_summary(
        self,
        project_key: str,
        session_id: str,
        subpath: Optional[str] = None,
    ) -> Optional[Any]:
        """Return the summary for a key, or None if there isn't one."""
        with self._lock:
            key_id = self._key_id(project_key, session_id, subpath)
            if key_id is None:
                return None
            row = self._conn.execute(
                "SELECT summary FROM summaries WHERE key_id = ?", (key_id,)
            ).fetchone()
        return json.loads(row["summary"]) if row else None

    # ------------------------------------------------------------ navigation

    def list_sessions(self, project_key: str) -> list[str]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT DISTINCT session_id FROM keys "
                "WHERE project_key = ? ORDER BY session_id",
                (project_key,),
            ).fetchall()
        return [r["session_id"] for r in rows]

    def list_subpaths(self, project_key: str, session_id: str) -> list[Optional[str]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT subpath FROM keys "
                "WHERE project_key = ? AND session_id = ? "
                "ORDER BY subpath",
                (project_key, session_id),
            ).fetchall()
        return [r["subpath"] for r in rows]

    # --------------------------------------------------------------- deletion

    def delete(
        self,
        project_key: str,
        session_id: str,
        subpath: Optional[str] = None,
    ) -> bool:
        """Delete one key with its entries and summary. Returns True if it existed."""
        with self._lock, self._conn:
            cur = self._conn.execute(
                "DELETE FROM keys WHERE project_key = ? AND session_id = ? "
                "AND COALESCE(subpath, '') = COALESCE(?, '')",
                (project_key, session_id, subpath),
            )
            return cur.rowcount > 0

    def delete_session(self, project_key: str, session_id: str) -> int:
        """Delete every subpath of a session. Returns the number of keys removed."""
        with self._lock, self._conn:
            cur = self._conn.execute(
                "DELETE FROM keys WHERE project_key = ? AND session_id = ?",
                (project_key, session_id),
            )
            return cur.rowcount

    # -------------------------------------------------------------- lifecycle

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def __enter__(self) -> "SQLiteSessionStore":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


if __name__ == "__main__":
    with SQLiteSessionStore() as store:
        store.append("my-project", "abc123", {"type": "user", "text": "hello"})
        store.append("my-project", "abc123", {"type": "assistant", "text": "hi"})
        store.append("my-project", "abc123", {"type": "tool", "name": "ls"}, subpath="agent-1")
        store.set_summary("my-project", "abc123", {"title": "Greeting"})

        print(store.load("my-project", "abc123"))
        print(store.load("my-project", "abc123", subpath="agent-1"))
        print(store.get_summary("my-project", "abc123"))
        print(store.list_sessions("my-project"))
        print(store.list_subpaths("my-project", "abc123"))