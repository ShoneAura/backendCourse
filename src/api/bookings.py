from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["бронирование"])


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
    if not room:
        raise HTTPException(status_code=404, detail="передан не корректный id номера")
    _booking_data = BookingAdd(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get(
    "/bookings",
    summary="Получение всех бронирований",
    description="Возвращает список всех бронирований",
)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get(
    "/bookings/me",
    summary="Получение бронирований пользователя",
    description="Возвращает все бронирования пользователя",
)
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


# @router.delete(
#     "/{hotel_id}/rooms/{room_id}",
#     summary="Удаление номера",
#     description="Удаляет номер",
# )
# async def delete_room(db: DBDep, hotel_id: int, room_id: int):
#     await db.rooms.delete(id=room_id, hotel_id=hotel_id)
#     await db.commit()
#     return {"status": "OK"}
#
#
# @router.put(
#     "/{hotel_id}/rooms/{room_id}",
#     summary="Полное обновление данных ономере",
#     description="Необходимо передать все параметры номера",
# )
# async def update_room(
#     db: DBDep,
#     hotel_id: int,
#     room_id: int,
#     room_data: RoomAddRequest,
# ):
#     _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
#
#     await db.rooms.update(_room_data, id=room_id)
#     await db.commit()
#
#     return {"status": "OK"}
#
#
# @router.patch(
#     "/{hotel_id}/rooms/{room_id}",
#     summary="Частичное обновление данных о номере",
#     description="Мы обновляем разные данные о номере",
# )
# async def patch_room(
#     db: DBDep,
#     hotel_id: int,
#     room_id: int,
#     room_data: RoomPatchRequest,
# ):
#     _room_data = RoomPatch(
#         hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
#     )
#     await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
#     await db.commit()
#     return {"status": "OK"}
