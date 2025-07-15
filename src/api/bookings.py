from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

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
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)

    _booking_data = BookingAdd(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(
            status_code=409, detail=ex.detail
        )
    await db.commit()
    return {"status": "OK", "data": booking}
