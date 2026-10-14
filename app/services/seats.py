from app.repositories import events as events_repo
from app.repositories import seats as repo
from app.services.events import NotFound
async def listing(pool, event_id, status):
    event = await events_repo.get(pool, event_id)
    if event is None:
        raise NotFound()
    return await repo.list_for_event(pool, event_id, status)