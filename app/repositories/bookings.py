async def get_seat(conn, seat_id):
    return await conn.fetchrow("SELECT * FROM seats WHERE id = $1", seat_id)

async def mark_booked(conn, seat_id):
    await conn.execute("UPDATE seats SET status = 'booked' WHERE id = $1", seat_id)

async def insert(conn, seat_id, user_email):
    return await conn.fetchrow(
    """INSERT INTO bookings (seat_id, user_email)
    VALUES ($1, $2)
    RETURNING *""",
    seat_id, user_email,
    )

async def get_seat_locked(conn, seat_id):
    return await conn.fetchrow(
    "SELECT * FROM seats WHERE id = $1 FOR UPDATE", seat_id
    )

async def mark_available(conn, seat_id):
    await conn.execute("UPDATE seats SET status = 'available' WHERE id = $1", seat_id)

async def get(conn, booking_id):
    return await conn.fetchrow("SELECT * FROM bookings WHERE id = $1", booking_id)

async def delete(conn, booking_id):
    return await conn.execute("DELETE FROM bookings WHERE id = $1", booking_id)


async def list_all(conn):
    return await conn.fetch(
    """SELECT b.id, b.user_email, b.created,
    s.seat_no,
    e.name AS event_name
    FROM bookings b
    JOIN seats s ON s.id = b.seat_id
    JOIN events e ON e.id = s.event_id
    ORDER BY b.id"""
    )