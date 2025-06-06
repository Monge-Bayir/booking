from app.dao.base import BaseDao
from app.booking.models import Booking
from app.database import async_session_maker
from app.hotels.models import Room
import datetime
from fastapi import HTTPException
from sqlalchemy import select, and_, or_, func, insert, delete

class BookingDao(BaseDao):
    model = Booking

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: datetime.date, date_to: datetime.date):
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_to <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')

            get_rooms_left = select(
                (Room.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.room_id == Room.id
            ).where(Room.id == room_id).group_by(
                Room.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_bookings = insert(Booking).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Booking)

                new_booking = await session.execute(add_bookings)
                await session.commit()
                return new_booking.scalar()

            else:
                return None

    @classmethod
    async def delete_booking(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == booking_id)
            result = await session.execute(query)
            booking = result.scalar_one_or_none()

            if not booking:
                raise HTTPException(status_code=404, detail="Бронирование не найдено")

            if booking.user_id != user_id:
                raise HTTPException(status_code=403, detail="Удаление чужого бронирования запрещено")

            delete_query = delete(cls.model).where(cls.model.id == booking_id)
            await session.execute(delete_query)
            await session.commit()