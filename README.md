# Ticketflow

A seat booking API. The CRUD is the boring part - the point of this project is
that two people clicking "book" on the same seat in the same millisecond can't
both get it.

**Live:** https://ticket-flow-k7ah.onrender.com/docs

*(free hosting - the first request after a quiet spell takes about a minute to
wake up)*

## The problem

Booking a seat is four steps: find the seat, check it's free, mark it booked,
save the booking. That's correct when one person clicks. It is not when fifty do.

Between "check it's free" and "mark it booked" there is a gap, and another
request can read the same row inside that gap and reach the same conclusion.
Both think the seat is free. Both book it.

## The fix

`SELECT ... FOR UPDATE`, inside a transaction. The first request locks the seat
row. Everyone else waits - not fails, waits - until that transaction ends, then
reads the row as it was left: booked. They get a clean 409.

Measured, 50 simultaneous requests for one seat:

    got the seat (201): 1
    told no      (409): 49
    crashed      (500): 0

`check_race.py` in this repo runs that.

There is a second line of defence in the schema: `UNIQUE (seat_id)` on bookings.
Even if the application logic were wrong, Postgres physically cannot store two
bookings for the same seat.

## Stack

FastAPI, PostgreSQL, asyncpg. No ORM - the SQL is written out.

Three layers: routers handle HTTP, services hold the rules, repositories hold
SQL. Nothing in a repository imports FastAPI.

Deployed on Render, database on Neon.

## Endpoints

| | |
|---|---|
| `POST /api/events` | create an event and its seats, in one transaction |
| `GET /api/events` | list events with seats remaining |
| `GET /api/events/{id}/seats` | seats for an event, filterable by status |
| `POST /api/bookings` | book a seat - this is the one that matters |
| `DELETE /api/bookings/{id}` | cancel, and free the seat |

## Running it locally

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
createdb ticketflow && psql -d ticketflow -f schema.sql
echo "DATABASE_URL=postgresql://localhost/ticketflow" > .env
uvicorn main:app --reload
```

## What I would add next

- Seat holds that expire - book it, ten minutes to pay, then released
- Auth; right now a booking just carries an email address
- A queue in front of booking for events where demand spikes
