from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class EventIn(BaseModel):
    name: str
    venue: str
    starts_at: datetime
    total_seats: int


class EventUpdate(BaseModel):
    name: str | None = None
    venue: str | None = None
    starts_at: datetime | None = None

    
class BookingIn(BaseModel):
    seat_id: int
    user_email: str