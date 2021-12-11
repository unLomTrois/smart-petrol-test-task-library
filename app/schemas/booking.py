from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, validator
from app.db.utils import get_booking_end_time


class BookingBase(BaseModel):
    book_item_id: int
    user_id: int


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    end_of_booking: Optional[datetime]

    @validator("end_of_booking")
    def set_end_of_booking(cls, v):
        return v or get_booking_end_time()
