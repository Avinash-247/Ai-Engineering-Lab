"""
Chaos switch: break the Rentals API on purpose, the way real incidents happen.

  uv run python -m simulation.chaos status
  uv run python -m simulation.chaos slow_db on            # DB connection pool exhaustion
  uv run python -m simulation.chaos payment_timeout on    # payment provider times out on most bookings
  uv run python -m simulation.chaos bad_deploy            # ship version 1.4.1, which has a bug
  uv run python -m simulation.chaos reset                 # all faults off, back to 1.4.0

Run it while the API and the load generator are running, then watch what changes.
"""
import sys

from rentals_api import faults, telemetry


def main(args: list[str]) -> None:
    telemetry.init_db()
    faults.init()
    if not args or args[0] == "status":
        for name, about in faults.KNOWN_FAULTS.items():
            print(f"{name:<16} {'ON ' if faults.is_on(name) else 'off'}   {about}")
        print(f"{'version':<16} {telemetry.current_version()}")
    elif args[0] in faults.KNOWN_FAULTS and len(args) == 2 and args[1] in ("on", "off"):
        faults.set_fault(args[0], args[1] == "on")
        print(f"{args[0]} is now {args[1].upper()}")
    elif args[0] == "bad_deploy":
        telemetry.record_deploy("1.4.1", "ravi.k", "Show amenities on the listing page")
        print("Deployed 1.4.1 (it has a bug: some listings now return 500)")
    elif args[0] == "reset":
        for name in faults.KNOWN_FAULTS:
            faults.set_fault(name, False)
        if telemetry.current_version() != "1.4.0":
            telemetry.record_deploy("1.4.0", "trainer", "Reset to the stable release")
        print("All faults off; version 1.4.0")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
