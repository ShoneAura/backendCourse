from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomsWithRels
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_nodel = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_nodel = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_nodel = RoomsOrm
    schema = RoomsWithRels


class UserDataMapper(DataMapper):
    db_nodel = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_nodel = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_nodel = FacilitiesOrm
    schema = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomFacility
