from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
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
async def get_rooms(
    hotel_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение отеля",
    description="Возвращает отель по id",
)
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id, hotel_id=hotel_id
        )


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление номера",
    description="Добавляет номер, необходимо отправить данные об номере",
)
async def create_room(
    hotel_id: int,
    room_data: RoomAddRequest = Body(),
):
    async with async_session_maker() as session:
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="Удаляет номер",
)
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных ономере",
    description="Необходимо передать все параметры номера",
)
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="Мы обновляем разные данные о номере",
)
async def patch_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    async with async_session_maker() as session:
        await RoomsRepository(session).update(
            _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}
