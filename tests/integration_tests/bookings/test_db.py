from datetime import date, datetime

from src.schemas.bookings import BookingAdd, Booking


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = {
        "user_id": user_id,
        "room_id": room_id,
        "date_from": date(year=2024, month=8, day=10),
        "date_to": date(year=2024, month=8, day=20),
        "price": 100,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    booking_data = BookingAdd(**booking_data)

    new_booking = await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.price == 100
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id

    update_booking_data = booking.model_copy(update={
        "price": 200
    })
    await db.bookings.update(update_booking_data, id=booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert updated_booking
    assert updated_booking.price == 200
    assert updated_booking.user_id == new_booking.user_id
    assert updated_booking.room_id == new_booking.room_id

    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert not booking
