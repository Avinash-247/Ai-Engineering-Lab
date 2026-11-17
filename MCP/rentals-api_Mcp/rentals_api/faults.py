"""
Fault-injection hooks for testing how the Rentals API behaves when things go wrong.

Every fault is OFF by default, so the API behaves normally unless something turns one on.
The simulation tools (simulation/chaos.py) switch faults on and off; the API only checks them.

  slow_db           every database call waits for a connection (pool exhaustion)
  payment_timeout   the payment provider times out on most bookings
"""
from rentals_api import telemetry

KNOWN_FAULTS = {
    "slow_db": "DB connection pool exhaustion: every endpoint that touches the DB slows to 1–2 s",
    "payment_timeout": "Payment provider times out on ~60% of POST /bookings (502 after 3 s)",
}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS faults (
    name    TEXT PRIMARY KEY,
    enabled INTEGER NOT NULL DEFAULT 0
);
"""


def init() -> None:
    with telemetry.connect() as conn:
        conn.executescript(_SCHEMA)


def is_on(name: str) -> bool:
    with telemetry.connect() as conn:
        row = conn.execute("SELECT enabled FROM faults WHERE name = ?", (name,)).fetchone()
    return bool(row and row["enabled"])


def set_fault(name: str, enabled: bool) -> None:
    if name not in KNOWN_FAULTS:
        raise ValueError(f"Unknown fault {name!r}. Known faults: {', '.join(KNOWN_FAULTS)}")
    with telemetry.connect() as conn:
        conn.execute("INSERT INTO faults(name, enabled) VALUES (?, ?) "
                     "ON CONFLICT(name) DO UPDATE SET enabled = excluded.enabled", (name, int(enabled)))
