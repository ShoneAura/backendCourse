from fastapi import Query, APIRouter, Body

from backendCourse.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@router.get(
    "",
    summary="Получение отелей",
    description="Возвращает список всех отелей"
)
async def get_hotels(
        title: str = Query(None, description="Название отеля"),
        id: int = Query(None, description="Айдишник отеля"),
        page: int = Query(None, description="Номер страницы"),
        per_page: int = Query(10, description="Количество отелей на странице"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if page > len(hotels) // per_page:
        page = len(hotels) // per_page
    if page <= 0:
        page = 1
    if per_page < 0:
        per_page = 10
    return hotels_[(page - 1) * per_page: page * per_page]


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
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
