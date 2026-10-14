from app.repositories import events as repo
class NotFound(Exception):
    pass
class BadSeatCount(Exception):
    pass
async def create(pool, name, venue, starts_at, total_seats):
    if total_seats < 1 or total_seats > 1000:
        raise BadSeatCount()
    async with pool.acquire() as conn:
        async with conn.transaction():
            event = await repo.insert(conn, name, venue, starts_at)
            await repo.insert_seats(conn, event["id"], total_seats)
    return event

async def listing(pool):
    return await repo.list_with_seats_left(pool)
async def get_one(pool, event_id):
    row = await repo.get(pool, event_id)
    if row is None:
        raise NotFound()
    return row
async def edit(pool, event_id, name, venue, starts_at):
    row = await repo.update(pool, event_id, name, venue, starts_at)
    if row is None:
        raise NotFound()
    return row
async def remove(pool, event_id):
    result = await repo.delete(pool, event_id)
    if result == "DELETE 0":
        raise NotFound()