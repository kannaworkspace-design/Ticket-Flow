async def insert(conn, name, venue, starts_at):
    return await conn.fetchrow(
    """INSERT INTO events (name, venue, starts_at)
    VALUES ($1, $2, $3)
    RETURNING *""",
    name, venue, starts_at,
)

async def insert_seats(conn, event_id, total_seats):
    await conn.execute(
    """INSERT INTO seats (event_id, seat_no)
    SELECT $1, generate_series(1, $2)""",
    event_id, total_seats,
)

async def list_with_seats_left(conn):
    return await conn.fetch(
    """SELECT e.*, count(s.id) AS seats_left
    FROM events e
    LEFT JOIN seats s ON s.event_id = e.id AND s.status = 'available'
    GROUP BY e.id
    ORDER BY e.starts_at"""
)

async def update(conn, event_id, name, venue, starts_at):
    return await conn.fetchrow(
    """UPDATE events
    SET name = COALESCE($2, name),
    venue = COALESCE($3, venue),
    starts_at = COALESCE($4, starts_at)
    WHERE id = $1
    RETURNING *""",
    event_id, name, venue, starts_at,
)

async def get(conn, event_id):
    return await conn.fetchrow("SELECT * FROM events WHERE id = $1", event_id)
async def delete(conn, event_id):
    return await conn.execute("DELETE FROM events WHERE id = $1", event_id)