import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@app.get("/hotels")
async def get_hotels():
    return hotels


@app.delete("/hotels/<hotel_id>")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"message": f"Отель с айдишником {hotel_id} удален"}


@app.post("/hotels")
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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)