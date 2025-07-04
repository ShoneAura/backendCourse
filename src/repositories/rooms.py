from sqlalchemy import select, func

from src.database import engine
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
        self,
        hotel_id,
        title,
        description,
        price,
        quantity,
    ) -> list[Room]:
        query = select(RoomsOrm)
        if hotel_id:
            query = query.filter(RoomsOrm.hotel_id == hotel_id)
        if title:
            query = query.filter(
                func.lower(RoomsOrm.title).contains(title.strip().lower())
            )
        if description:
            query = query.filter(
                func.lower(RoomsOrm.description).contains(description.strip().lower())
            )
        if price:
            query = query.filter(RoomsOrm.price == price)
        if quantity:
            query = query.filter(RoomsOrm.quantity == quantity)

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [
            Room.model_validate(room, from_attributes=True)
            for room in result.scalars().all()
        ]
