"""
Synthetic load for the Rentals API: virtual users browsing and booking rentals, non-stop.

Run:  uv run python -m simulation.loadgen                 (12 users against http://127.0.0.1:9000)
      uv run python -m simulation.loadgen --users 30      (busier)

Each virtual user loops: search → view a listing → sometimes book → sometimes check a booking,
with short random pauses, like real people. Press Ctrl + C to stop.
"""
import argparse
import asyncio
import random
import time

import httpx

CITIES = ["Hyderabad", "Bengaluru", "Pune", "Chennai"]
TENANTS = ["Asha", "Ravi", "Priya", "Kiran", "Meera", "Arjun", "Sneha", "Vikram"]
PROPERTY_IDS = list(range(101, 109))

stats = {"requests": 0, "errors": 0}


async def call(client: httpx.AsyncClient, method: str, url: str, **kwargs) -> httpx.Response | None:
    try:
        response = await client.request(method, url, **kwargs)
        stats["requests"] += 1
        if response.status_code >= 500:
            stats["errors"] += 1
        return response
    except httpx.HTTPError:
        stats["errors"] += 1
        return None


async def virtual_user(client: httpx.AsyncClient) -> None:
    booked: list[int] = []
    while True:
        await call(client, "GET", "/properties", params={"city": random.choice(CITIES)})
        await asyncio.sleep(random.uniform(0.2, 0.8))
        pid = random.choice(PROPERTY_IDS)
        await call(client, "GET", f"/properties/{pid}")
        if random.random() < 0.25:                                     # 1 in 4 visits ends in a booking
            r = await call(client, "POST", "/bookings",
                           json={"property_id": pid, "tenant": random.choice(TENANTS), "months": 11})
            if r is not None and r.status_code == 201:
                booked.append(r.json()["id"])
        if booked and random.random() < 0.2:
            await call(client, "GET", f"/bookings/{random.choice(booked)}")
        await asyncio.sleep(random.uniform(0.5, 1.5))


async def reporter() -> None:
    last = 0
    while True:
        await asyncio.sleep(10)
        done = stats["requests"]
        print(f"{time.strftime('%H:%M:%S')}  {(done - last) / 10:5.1f} req/s   total {done}   5xx/failed {stats['errors']}")
        last = done


async def main(base_url: str, users: int) -> None:
    print(f"Sending load to {base_url} with {users} virtual users. Ctrl + C to stop.")
    async with httpx.AsyncClient(base_url=base_url, timeout=10) as client:
        await asyncio.gather(reporter(), *(virtual_user(client) for _ in range(users)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:9000")
    parser.add_argument("--users", type=int, default=12)
    args = parser.parse_args()
    try:
        asyncio.run(main(args.url, args.users))
    except KeyboardInterrupt:
        print("Load stopped.")
