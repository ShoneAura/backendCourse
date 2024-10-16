from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение отелей",
    description="Возвращает список всех отелей"
)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )


@router.get(
    "/<hotel_id>",
    summary="Получение отеля",
    description="Возвращает отель по id"
)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary="Добавление отеля",
    description="Добавляет отель, необходимо отправить данные об отеле"
)
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Sochi",
        "location": "ул. Море 5"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Dubai",
        "location": "ул. Шейха 4"
    }},
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete(
    "/<hotel_id>",
    summary="Удаление отеля",
    description="Удаляет отель"
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put(
    "/<hotel_id>",
    summary="Полное обновление данных об отеле",
    description="Необходимо передать все параметры отеля"
)
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    "/<hotel_id>",
    summary="Частичное обновление данных об отеле",
    description="Мы обновляем разные данные об отеле"
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
