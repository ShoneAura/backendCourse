from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import (
    RoomAdd,
    RoomAddRequest,
    RoomPatchRequest,
    RoomPatch,
)

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение всех комнат",
    description="Возвращает список всех комнат",
)
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение отеля",
    description="Возвращает отель по id",
)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление номера",
    description="Добавляет номер, необходимо отправить данные об номере",
)
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="Удаляет номер",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных ономере",
    description="Необходимо передать все параметры номера",
)
async def update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.update(_room_data, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="Мы обновляем разные данные о номере",
)
async def patch_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
