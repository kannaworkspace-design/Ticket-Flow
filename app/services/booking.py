from app.repositories import bookings as repo

class SeatNotFound(Exception):
    pass

class SeatTaken(Exception):
    pass

class BookingNotFound(Exception):
    pass

async def create(pool, seat_id, user_email):
    async with pool.acquire() as conn:
        async with conn.transaction():
            seat = await repo.get_seat_locked(conn, seat_id)
            if seat is None:
                raise SeatNotFound()
            if seat["status"] == "booked":
                raise SeatTaken()
            await repo.mark_booked(conn, seat_id)
            booking = await repo.insert(conn, seat_id, user_email)
    return booking

async def cancel(pool, booking_id):
    async with pool.acquire() as conn:
        async with conn.transaction():
            booking = await repo.get(conn, booking_id)
            if booking is None:
                raise BookingNotFound()
            await repo.delete(conn, booking_id)
            await repo.mark_available(conn, booking["seat_id"])