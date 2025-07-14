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

    await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none()
    assert booking
    booking_data = Booking(
        id=booking.id,
        user_id=booking.user_id,
        room_id=booking.room_id,
        date_from=booking.date_from,
        date_to=booking.date_to,
        price=200,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )
    await db.bookings.update(booking_data)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking.price == 200
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert not booking
    await db.commit()
