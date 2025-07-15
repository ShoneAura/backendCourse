from src.exceptions import AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_bookings_me(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
            self,
            user_id: int,
            booking_data: BookingAddRequest,
    ):

        room: Room = await RoomService(self.db).get_room_with_check(room_id=booking_data.room_id)

        hotel: Hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=room.hotel_id)

        _booking_data = BookingAdd(
            user_id=user_id, price=room.price, **booking_data.model_dump()
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as ex:
            raise AllRoomsAreBookedException from ex

        await self.db.commit()
        return booking