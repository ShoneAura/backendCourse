from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import DatesAreIncorrectException, ObjectNotFoundException
from src.schemas.facilities import RoomFacilityAdd
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
    db: DBDep,
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    if date_from < date_to:
        raise DatesAreIncorrectException(404, "Дата начала должна быть меньше даты конца")

    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение отеля",
    description="Возвращает отель по id",
)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Номер не найден"
        )


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление номера",
    description="Добавляет номер, необходимо отправить данные об номере",
)
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Отель отсутствует"
        )

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="Удаляет номер",
)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):

    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Номер не найден"
        )
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
    try:
        await db.rooms.update(_room_data, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Номер не найден"
        )
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities=room_data.facilities_ids
    )
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
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    try:
        await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=404, detail="Номер не найден"
        )

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}
