from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.booking import BookingService

router = APIRouter(prefix="/bookings", tags=["бронирование"])


@router.get(
    "",
    summary="Получение всех бронирований",
    description="Возвращает список всех бронирований",
)
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get(
    "/me",
    summary="Получение бронирований пользователя",
    description="Возвращает все бронирования пользователя",
)
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_bookings_me(user_id=user_id)


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
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
