from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.models import Room
from app.booking.models import Booking
from sqlalchemy import select, and_, func
from datetime import date

class RoomDao(BaseDao):
    model = Room


    @classmethod
    async def find_all_by_hotel_with_availability(cls, hotel_id: int, date_from: date, date_to: date):
        """
        Получить список комнат отеля с расчетом доступного количества (rooms_left),
        учитывая бронирования в заданном интервале.
        """

        async with async_session_maker() as session:  # AsyncSession
            # Подзапрос для подсчёта занятых комнат за период
            booked_subquery = (
                select(
                    Booking.room_id,
                    func.coalesce(func.sum(1), 0).label('booked_count')  # считаем сколько комнат забронировано
                )
                .where(
                    and_(
                        Booking.room_id == Room.id,
                        Booking.date_from < date_to,
                        Booking.date_to > date_from,
                    )
                )
                .group_by(Booking.room_id)
                .subquery()
            )

            # Основной запрос: берем комнаты, левый join с подзапросом бронирований
            query = (
                select(
                    Room,
                    (Room.quantity - func.coalesce(booked_subquery.c.booked_count, 0)).label('rooms_left')
                )
                .outerjoin(booked_subquery, Room.id == booked_subquery.c.room_id)
                .where(Room.hotel_id == hotel_id)
            )

            result = await session.execute(query)
            rows = result.all()

            # Формируем список с подсчитанными rooms_left
            rooms_with_availability = []
            for room, rooms_left in rows:
                room.rooms_left = rooms_left if rooms_left > 0 else 0
                rooms_with_availability.append(room)

            return rooms_with_availability