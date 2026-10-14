from fastapi import APIRouter, HTTPException, Request
from app.schemas import EventIn, EventUpdate
from app.services import events as service
from app.services import seats as seats_service


router = APIRouter(prefix="/api/events")

@router.post("", status_code=201)
async def create_event(body: EventIn, request: Request):
    try:
        row = await service.create(
        request.app.state.pool,
body.name, body.venue, body.starts_at, body.total_seats,
)
    except service.BadSeatCount:
        raise HTTPException(status_code=400, detail="total_seats must be between 1 and 1000")
    return dict(row)

@router.get("")
async def list_events(request: Request):
    rows = await service.listing(request.app.state.pool)
    return [dict(r) for r in rows]


@router.get("/{event_id}")
async def get_event(event_id: int, request: Request):
    try:
        row = await service.get_one(request.app.state.pool, event_id)
    except service.NotFound:
        raise HTTPException(status_code=404, detail="Event not found")
    return dict(row)


@router.patch("/{event_id}")
async def update_event(event_id: int, body: EventUpdate, request: Request):
    try:
        row = await service.edit(
request.app.state.pool, event_id, body.name, body.venue, body.starts_at
)
    except service.NotFound:
        raise HTTPException(status_code=404, detail="Event not found")
    return dict(row)


@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int, request: Request):
    try:
        await service.remove(request.app.state.pool, event_id)
    except service.NotFound:
        raise HTTPException(status_code=404, detail="Event not found")

    
@router.get("/{event_id}/seats")
async def list_seats(event_id: int, request: Request, status: str | None = None):
    try:
        rows = await seats_service.listing(request.app.state.pool, event_id, status)
    except seats_service.NotFound:
        raise HTTPException(status_code=404, detail="Event not found")
    return [dict(r) for r in rows]