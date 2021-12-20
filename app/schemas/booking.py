from datetime import date, datetime
from typing import Union
from pydantic import BaseModel, validator
from app.db.utils import get_booking_end_time


class BookingBase(BaseModel):
    book_item_id: int
    user_id: int


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    user_id: int
    book_id: int
    end_of_booking: Union[datetime, date]

    @validator("end_of_booking")
    def set_end_of_booking(cls, v):
        return v or get_booking_end_time()
