from fastapi import APIRouter, HTTPException, Request
from app.schemas import BookingIn
from app.services import booking as service


router = APIRouter(prefix="/api/bookings")

@router.post("", status_code=201)

async def create_booking(body: BookingIn, request: Request):
    try:
        row = await service.create(request.app.state.pool, body.seat_id, body.user_email)
    except service.SeatNotFound:
        raise HTTPException(status_code=404, detail="Seat not found")
    except service.SeatTaken:
        raise HTTPException(status_code=409, detail="Seat already booked")
    return dict(row)

@router.delete("/{booking_id}", status_code=204)
async def cancel_booking(booking_id: int, request: Request):
    try:
        await service.cancel(request.app.state.pool, booking_id)
    except service.BookingNotFound:
        raise HTTPException(status_code=404, detail="Booking not found")