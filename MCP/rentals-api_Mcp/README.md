# Rentals API

**StayEase Rentals API**: a FastAPI service for searching and booking rental homes, with built-in
telemetry, plus simulation services that put it under load and break it on purpose.

```text
 simulation/loadgen.py ──HTTP traffic──▶ rentals_api (FastAPI) ──records──▶ telemetry.db ──▶ scripts/peek.py
 simulation/chaos.py ───flips faults───▶        │                            requests · logs · deploys
```

## Project layout

```text
rentals-api/
├── rentals_api/            ← Part 1: the application
│   ├── main.py             the FastAPI app: properties and bookings endpoints
│   ├── telemetry.py        records every request, log line and deploy into telemetry.db
│   └── faults.py           fault-injection hooks (all off by default)
├── simulation/             ← Part 2: simulation services
│   ├── loadgen.py          synthetic users that search, view and book non-stop
│   └── chaos.py            switches faults on and off, ships a buggy release
├── scripts/
│   └── peek.py             a terminal dashboard over telemetry.db
├── pyproject.toml          dependencies
├── uv.lock                 exact versions, the same for everyone
└── .python-version         Python 3.12
```

---

## Setup

### 1 · Install uv (one time)

**Windows** (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a **new** terminal and check with `uv --version`.

### 2 · Get the code and install

```powershell
cd D:\Training\GenAI\Projects               # or any folder you like
git clone <repository URL shared by your trainer>
cd rentals-api
uv sync
```

`uv sync` downloads Python 3.12 if needed, creates a private `.venv` folder, and installs the exact versions in `uv.lock`.

> Run every command below from the `rentals-api` folder.

---

## Part 1 · The Rentals API

### Run it

```powershell
uv run uvicorn rentals_api.main:app --port 9000
```

Open **http://127.0.0.1:9000/docs** to try every endpoint in the browser.

| Method | Endpoint | Does |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/properties?city=Hyderabad&max_rent=40000` | Search listings |
| GET | `/properties/{property_id}` | One listing (IDs 101–108) |
| POST | `/bookings` | Book: `{"property_id": 102, "tenant": "Asha", "months": 11}` |
| GET | `/bookings/{booking_id}` | One booking |

### How the telemetry works

A FastAPI **middleware** in `main.py` wraps every request. It times the request and writes one row to `telemetry.db`: method, **route template** (such as `/properties/{property_id}`), status code, duration and app version. The API also writes **structured log lines** (level, route, message and details), and `telemetry.db` keeps a history of **deploys**.

After a few requests, look at it:

```powershell
uv run python -m scripts.peek
```

---

## Part 2 · Simulation services

Use **three terminal windows**, all in the `rentals-api` folder:

| Window | Command | You should see |
|---|---|---|
| 1 · API | `uv run uvicorn rentals_api.main:app --port 9000` | `Uvicorn running on http://127.0.0.1:9000` |
| 2 · load | `uv run python -m simulation.loadgen` | About 19 req/s, reported every 10 seconds |
| 3 · you | `uv run python -m scripts.peek` | Requests, errors and latency per route |

### Break it on purpose

```powershell
uv run python -m simulation.chaos status
uv run python -m simulation.chaos bad_deploy             # ship buggy version 1.4.1
#   ...wait a minute...
uv run python -m scripts.peek 1
uv run python -m simulation.chaos reset
```

| Incident | Command | What to look for in `peek` |
|---|---|---|
| Bad deploy | `simulation.chaos bad_deploy` | Errors on one route, right after a new version |
| Slow database | `simulation.chaos slow_db on` | Every route slow; "connection pool exhausted" warnings |
| Payment timeout | `simulation.chaos payment_timeout on` | Only bookings failing, with 502 errors |

Turn faults off with `off`, or everything at once with `reset`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `'uv' is not recognized` | Open a new terminal after installing uv |
| `uv sync` fails behind a college or office proxy | Set `HTTPS_PROXY`, or try from another network |
| `No module named 'rentals_api'` | Run commands from the `rentals-api` folder, and use `-m`: `python -m simulation.chaos`, not `python simulation/chaos.py` |
| `Address already in use` on port 9000 | Another copy is running. Close it, or use `--port 9001` (and `simulation.loadgen --url http://127.0.0.1:9001`) |
| `peek` says "No requests yet" | The API (window 1) and the load generator (window 2) must be running |
| Clean start | Stop everything and delete `telemetry.db`, `telemetry.db-shm`, `telemetry.db-wal` |
| Command Prompt won't switch to D: | Use `cd /d D:\...` |
