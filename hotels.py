from fastapi import Query, APIRouter, Body

from backendCourse.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Пекин", "name": "beijing"},
    {"id": 4, "title": "Москва", "name": "moscow"},
    {"id": 5, "title": "Лондон", "name": "london"},
    {"id": 6, "title": "Токио", "name": "tokyo"},
    {"id": 7, "title": "Париж", "name": "paris"},
    {"id": 8, "title": "Ливерпуль", "name": "liverpool"},
    {"id": 9, "title": "Милан", "name": "milan"},
]


@router.get(
    "",
    summary="Получение отелей",
    description="Возвращает список всех отелей"
)
async def get_hotels(
        title: str | None = Query(None, description="Название отеля"),
        id: int | None = Query(None, description="Айдишник отеля"),
        page: int | None = Query(None, description="Номер страницы", gt=1),
        per_page: int | None = Query(None, description="Количество отелей на странице", gt=1, lt=30),
):
    DEFAULT_COUNT_PER_PAGE = 3
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if page or per_page:
        return hotels_[(page - 1) * per_page:][:per_page]
    return hotels_


@router.delete(
    "/<hotel_id>",
    summary="Удаление отеля",
    description="Удаляет отель"
)
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": f"Отель с айдишником {hotel_id} удален"}


@router.post(
    "",
    summary="Добавление отеля",
    description="Добавляет отель, необходимо отправить данные об отеле"
)
async def create_hotel(hotel_data: Hotel=Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Sochi",
        "name": "sochi_u_morya"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Dubai",
        "name": "dubai_v_krym"
    }},
})
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )


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
