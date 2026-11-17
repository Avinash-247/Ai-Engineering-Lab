"""
Telemetry store for the Rentals API.

The API records three things here, in one SQLite file (telemetry.db, at the project root):

  requests  every HTTP request: when, which route, status code, how long it took, which version
  logs      structured log lines: level, route, message, extra details as JSON
  deploys   every release: when, which version, who shipped it, and why

Anything that wants to observe the API (a dashboard, a script, another service) reads this file.
WAL mode lets the API keep writing while other processes read.
"""
import json
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "telemetry.db"   # absolute: works from any folder

SCHEMA = """
CREATE TABLE IF NOT EXISTS requests (
    ts          REAL NOT NULL,      -- unix time, seconds
    method      TEXT NOT NULL,
    route       TEXT NOT NULL,      -- the route TEMPLATE, e.g. /properties/{property_id}
    status      INTEGER NOT NULL,
    duration_ms REAL NOT NULL,
    version     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_requests_ts ON requests(ts);

CREATE TABLE IF NOT EXISTS logs (
    ts      REAL NOT NULL,
    level   TEXT NOT NULL,          -- INFO, WARNING, ERROR
    route   TEXT,
    message TEXT NOT NULL,
    extra   TEXT                    -- JSON with any extra fields
);
CREATE INDEX IF NOT EXISTS idx_logs_ts ON logs(ts);

CREATE TABLE IF NOT EXISTS deploys (
    ts      REAL NOT NULL,
    version TEXT NOT NULL,
    author  TEXT NOT NULL,
    note    TEXT NOT NULL
);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) FROM deploys").fetchone()[0] == 0:
            conn.execute("INSERT INTO deploys VALUES (?, ?, ?, ?)",
                         (time.time() - 86400, "1.4.0", "ci-bot", "Weekly release: search filters, faster listing page"))


def current_version() -> str:
    with connect() as conn:
        row = conn.execute("SELECT version FROM deploys ORDER BY ts DESC LIMIT 1").fetchone()
    return row["version"] if row else "unknown"


def record_request(method: str, route: str, status: int, duration_ms: float, version: str) -> None:
    with connect() as conn:
        conn.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?)",
                     (time.time(), method, route, status, duration_ms, version))


def record_log(level: str, message: str, route: str | None = None, **extra) -> None:
    with connect() as conn:
        conn.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)",
                     (time.time(), level, route, message, json.dumps(extra) if extra else None))


def record_deploy(version: str, author: str, note: str) -> None:
    with connect() as conn:
        conn.execute("INSERT INTO deploys VALUES (?, ?, ?, ?)", (time.time(), version, author, note))
