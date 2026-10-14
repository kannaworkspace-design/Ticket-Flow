async def list_for_event(conn, event_id, status):
    return await conn.fetch(
    """SELECT * FROM seats
    WHERE event_id = $1
    AND ($2::text IS NULL OR status = $2)
    ORDER BY seat_no""",
    event_id, status,
    )