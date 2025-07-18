from datetime import date

from pydantic import ConfigDict

from src.schemas.base import TimestampSchema


class BookingAddRequest(TimestampSchema):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(TimestampSchema):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
