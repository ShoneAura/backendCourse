from fastapi import Query, Body, APIRouter


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
        id: int = Query(None, description="Айдишник отеля")
):
    return hotels


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
async def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title
        }
    )


@router.put(
    "/<hotel_id>",
    summary="Полное обновление данных об отеле",
    description="Необходимо передать все параметры отеля"
)
async def update_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return hotel
    return {"message": f"Отель с айдишником {hotel_id} не найден"}


@router.patch(
    "/<hotel_id>",
    summary="Частичное обновление данных об отеле",
    description="Мы обновляем разные данные об отеле"
)
async def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return hotel
    return {"message": f"Отель с айдишником {hotel_id} не найден"}