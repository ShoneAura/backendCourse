from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/rooms",
    summary="Получение всех комнат",
    description="Возвращает список всех комнат",
)
async def get_rooms(
    hotel_id: int | None = Query(None, description="id отеля"),
    title: str | None = Query(None, description="Название номера"),
    description: str | None = Query(None, description="Описание номера"),
    price: int | None = Query(None, description="Цена номера"),
    quantity: int | None = Query(None, description="Количество номеров"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )


@router.post(
    "/rooms",
    summary="Добавление номера",
    description="Добавляет номер, необходимо отправить данные об номере",
)
async def create_room(
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Комната Сочи 2",
                "value": {
                    "hotel_id": 1,
                    "title": "Комната Сочи 2",
                    "description": "Комната для 2 человек",
                    "price": 1000,
                    "quantity": 10,
                },
            },
            "2": {
                "summary": "Комната Сочи 3",
                "value": {
                    "hotel_id": 1,
                    "title": "Комната Сочи 3",
                    "description": "Комната для 3 человек",
                    "price": 2000,
                    "quantity": 10,
                },
            },
            "3": {
                "summary": "Комната Дубаи 4",
                "value": {
                    "hotel_id": 2,
                    "title": "Комната Дубаи 4",
                    "description": "Комната для 4 человек",
                    "price": 3000,
                    "quantity": 10,
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/<room_id>", summary="Удаление номера", description="Удаляет номер")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put(
    "/<room_id>",
    summary="Полное обновление данных ономере",
    description="Необходимо передать все параметры номера",
)
async def update_room(
    room_id: int,
    room_data: RoomAdd,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    "/<room_id>",
    summary="Частичное обновление данных о номере",
    description="Мы обновляем разные данные о номере",
)
async def patch_room(
    room_id: int,
    room_data: RoomPATCH,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}
