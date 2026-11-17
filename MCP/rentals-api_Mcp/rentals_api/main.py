"""
StayEase Rentals API: search rental listings, view one, book it, check a booking.

Run (from the project folder):  uv run uvicorn rentals_api.main:app --port 9000
Try it in a browser:            http://127.0.0.1:9000/docs

Every request is timed and recorded (method, route, status, duration, version), and the API
writes structured log lines, all into telemetry.db (see telemetry.py).
Fault-injection hooks (see faults.py) are off by default.
"""
import asyncio
import random
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from rentals_api import faults, telemetry

app = FastAPI(title="StayEase Rentals API")
telemetry.init_db()
faults.init()

PROPERTIES = {
    i: {"id": i, "city": city, "title": f"{bhk} BHK in {area}", "rent": rent}
    for i, (city, area, bhk, rent) in enumerate([
        ("Hyderabad", "Gachibowli", 2, 32000), ("Hyderabad", "Madhapur", 3, 45000),
        ("Hyderabad", "Kondapur", 1, 18000), ("Bengaluru", "Whitefield", 2, 35000),
        ("Bengaluru", "HSR Layout", 3, 52000), ("Pune", "Hinjewadi", 2, 26000),
        ("Pune", "Baner", 1, 17000), ("Chennai", "OMR", 2, 24000),
    ], start=101)
}
BOOKINGS: dict[int, dict] = {}


class BookingIn(BaseModel):
    property_id: int
    tenant: str
    months: int = 11


# ─────────────── telemetry middleware: times and records EVERY request ───────────────
@app.middleware("http")
async def record_every_request(request: Request, call_next):
    start = time.perf_counter()
    version = telemetry.current_version()
    request.state.version = version
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as exc:                                   # an unhandled bug → 500
        telemetry.record_log("ERROR", f"Unhandled {type(exc).__name__}: {exc}",
                             route=_route_of(request), version=version)
        response, status = JSONResponse({"detail": "Internal Server Error"}, status_code=500), 500
    duration_ms = (time.perf_counter() - start) * 1000
    telemetry.record_request(request.method, _route_of(request), status, round(duration_ms, 1), version)
    return response


def _route_of(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", request.url.path)            # template, e.g. /properties/{property_id}


# ─────────────── a simulated database call (the slow_db fault can slow it down) ───────────────
async def db_query(route: str) -> None:
    await asyncio.sleep(random.uniform(0.008, 0.030))          # a healthy query: 8–30 ms
    if faults.is_on("slow_db"):
        wait_ms = random.uniform(900, 1800)
        await asyncio.sleep(wait_ms / 1000)
        if random.random() < 0.3:
            telemetry.record_log("WARNING", f"DB connection pool exhausted: waited {wait_ms:.0f} ms for a connection",
                                 route=route, pool_size=10, in_use=10, waiting=random.randint(8, 25))


# ─────────────── the API ───────────────
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/properties")
async def search_properties(city: str | None = None, max_rent: int | None = None):
    await db_query("/properties")
    results = [p for p in PROPERTIES.values()
               if (not city or p["city"].lower() == city.lower()) and (not max_rent or p["rent"] <= max_rent)]
    return {"count": len(results), "results": results}


@app.get("/properties/{property_id}")
async def get_property(property_id: int, request: Request):
    await db_query("/properties/{property_id}")
    if request.state.version == "1.4.1" and property_id % 3 == 0:
        # The bug shipped in 1.4.1: a new "amenities" field is missing for older listings
        raise KeyError("amenities")
    if property_id not in PROPERTIES:
        raise HTTPException(404, "Property not found")
    return PROPERTIES[property_id]


@app.post("/bookings", status_code=201)
async def create_booking(booking: BookingIn):
    await db_query("/bookings")
    if booking.property_id not in PROPERTIES:
        raise HTTPException(404, "Property not found")
    await asyncio.sleep(random.uniform(0.05, 0.12))            # call the payment provider
    if faults.is_on("payment_timeout") and random.random() < 0.6:
        await asyncio.sleep(3.0)
        telemetry.record_log("ERROR", "Payment provider timeout after 3000 ms",
                             route="/bookings", provider="PayFast", property_id=booking.property_id)
        raise HTTPException(502, "Payment provider unavailable")
    booking_id = len(BOOKINGS) + 5001
    BOOKINGS[booking_id] = {"id": booking_id, **booking.model_dump()}
    telemetry.record_log("INFO", f"Booking {booking_id} confirmed", route="/bookings",
                         property_id=booking.property_id, months=booking.months)
    return BOOKINGS[booking_id]


@app.get("/bookings/{booking_id}")
async def get_booking(booking_id: int):
    await db_query("/bookings/{booking_id}")
    if booking_id not in BOOKINGS:
        raise HTTPException(404, "Booking not found")
    return BOOKINGS[booking_id]
