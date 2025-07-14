from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["бронирование"])


@router.get(
    "",
    summary="Получение всех бронирований",
    description="Возвращает список всех бронирований",
)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get(
    "/me",
    summary="Получение бронирований пользователя",
    description="Возвращает все бронирования пользователя",
)
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="Добавление бронирования",
    description="Добавляет номер, необходимо отправить данные о бронировании",
)
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="передан не корректный id номера")
    _booking_data = BookingAdd(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}
