"""
Peek at the Rentals API's live telemetry with plain SQL: a tiny terminal dashboard.

  uv run python -m scripts.peek          (last 2 minutes)
  uv run python -m scripts.peek 5        (last 5 minutes)

Shows requests, errors and latency per route, the latest warnings and errors,
and the most recent deploy.
"""
import sys
import time

from rentals_api import telemetry


def main(minutes: int) -> None:
    telemetry.init_db()
    since = time.time() - minutes * 60
    with telemetry.connect() as conn:
        rows = conn.execute(
            """SELECT route,
                      COUNT(*)                              AS requests,
                      SUM(status >= 500)                    AS errors,
                      ROUND(AVG(duration_ms), 1)            AS avg_ms,
                      ROUND(MAX(duration_ms), 1)            AS max_ms
               FROM requests WHERE ts >= ?
               GROUP BY route ORDER BY requests DESC""",
            (since,),
        ).fetchall()
        logs = conn.execute(
            "SELECT ts, level, route, message FROM logs WHERE ts >= ? AND level != 'INFO' "
            "ORDER BY ts DESC LIMIT 5",
            (since,),
        ).fetchall()
        deploy = conn.execute("SELECT ts, version, author, note FROM deploys ORDER BY ts DESC LIMIT 1").fetchone()

    print(f"Last {minutes} min · as of {time.strftime('%H:%M:%S')} · version {telemetry.current_version()}\n")
    if not rows:
        print("No requests yet. Is the API running, and is something sending it traffic?")
        return
    print(f"{'route':<28}{'requests':>9}{'errors':>8}{'avg ms':>9}{'max ms':>9}")
    for r in rows:
        print(f"{r['route']:<28}{r['requests']:>9}{r['errors']:>8}{r['avg_ms']:>9}{r['max_ms']:>9}")

    print("\nLatest warnings and errors:")
    for line in logs or []:
        print(f"  {time.strftime('%H:%M:%S', time.localtime(line['ts']))}  {line['level']:<8}"
              f"{line['route'] or '':<28}{line['message']}")
    if not logs:
        print("  none")

    print(f"\nLast deploy: {deploy['version']} by {deploy['author']} at "
          f"{time.strftime('%H:%M:%S', time.localtime(deploy['ts']))}: {deploy['note']}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
