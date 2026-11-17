from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "telemetry.db"

def percentile(values: list[float], pct: float) -> float:
    """
    Nearest Rank percentille, p95  = the time 95% of the requests finished  within
    """
    if not values:
        return 0.0

    ordered = sorted(values)
    index = max(0, min(len(ordered)-1, round(pct / 100 * len(ordered))- 1 ))
    return round(ordered[index] - 1)


def summarize(rows: list) -> dict:
    """Turn many request rows into the handful of numbers an engineer looks at
    """
    durations = [ r['duration_ms'] for r in rows ]
    errors = sum ( 1 for r in rows if r["status"] >= 500 )
    return {
        "requests": len(rows),
        "errors_5xx": errors,
        "errors_rate_pct": round (100 * errors/len(rows), 2) if rows else 0.0,
        "p50_ms": percentile(durations, 50),
        "p95_ms": percentile(durations, 95)

    }

def requests_between(since: float, until: float |None = None, route: str|None = None) -> list:
    sql, args = "SELECT * FROM requests where ts >= ?", [since]
    if until is not None:
        sql += " AND ts < ?"
        args.append(until)
    if route:
        sql += " AND route = ?"
        args.append(route)
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(sql, args).fetchall()


def known_routes() -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        return [r['route'] for r in conn.execute("SELECT DISTINCT route FROM requests ORDER BY route")]
    
