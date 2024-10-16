from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

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




@router.post(
    "",
    summary="Добавление отеля",
    description="Добавляет отель, необходимо отправить данные об отеле"
)
async def create_hotel(hotel_data: Hotel=Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"message": "Отель добавлен"}


@router.delete(
    "/<hotel_id>",
    summary="Удаление отеля",
    description="Удаляет отель"
)
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": f"Отель с айдишником {hotel_id} удален"}


@router.put(
    "/<hotel_id>",
    summary="Полное обновление данных об отеле",
    description="Необходимо передать все параметры отеля"
)
async def update_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return hotel
    return {"message": f"Отель с айдишником {hotel_id} не найден"}


@router.patch(
    "/<hotel_id>",
    summary="Частичное обновление данных об отеле",
    description="Мы обновляем разные данные об отеле"
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return hotel
    return {"message": f"Отель с айдишником {hotel_id} не найден"}
