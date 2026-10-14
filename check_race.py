import asyncio, httpx

async def main():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as c:
        ev = await c.post("/api/events", json={"name": "Race check", "venue": "V",
                 "starts_at": "2026-12-01T10:00:00Z", "total_seats": 1})
        seat = (await c.get(f"/api/events/{ev.json()['id']}/seats")).json()[0]

        results = await asyncio.gather(*(
            c.post("/api/bookings", json={"seat_id": seat["id"], "user_email": f"p{i}@x.com"})
            for i in range(50)))

        codes = [r.status_code for r in results]
        print("got the seat (201):", codes.count(201))
        print("told no      (409):", codes.count(409))
        print("crashed      (500):", sum(1 for x in codes if x >= 500))

asyncio.run(main())