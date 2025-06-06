from app.dao.base import BaseDao
from app.database import async_session_maker
from app.hotels.models import Hotel, Room
from app.booking.models import Booking
from sqlalchemy import select, func, or_, and_


class HotelDao(BaseDao):
    model = Hotel


    @classmethod
    async def find_all_with_free_rooms(cls, location: str, date_from, date_to):
        async with async_session_maker() as session:
            # Подзапрос: количество забронированных номеров в период для каждого номера
            subquery_booked = (
                select(
                    Booking.room_id,
                    func.count(Booking.id).label("booked_count")
                )
                .where(
                    or_(
                        and_(Booking.date_from <= date_from, Booking.date_to > date_from),
                        and_(Booking.date_from < date_to, Booking.date_to >= date_to),
                        and_(Booking.date_from >= date_from, Booking.date_to <= date_to)
                    )
                )
                .group_by(Booking.room_id)
                .subquery()
            )

            # Основной запрос: отели с суммой свободных комнат (rooms_left)
            query = (
                select(
                    Hotel.id,
                    Hotel.name,
                    Hotel.location,
                    Hotel.services,
                    Hotel.rooms_quantity,
                    Hotel.image_id,
                    func.sum(Room.quantity - func.coalesce(subquery_booked.c.booked_count, 0)).label("rooms_left")
                )
                .join(Room, Room.hotel_id == Hotel.id)
                .outerjoin(subquery_booked, subquery_booked.c.room_id == Room.id)
                .where(
                    Hotel.location.ilike(f"%{location}%")
                )
                .group_by(Hotel.id)
                .having(func.sum(Room.quantity - func.coalesce(subquery_booked.c.booked_count, 0)) > 0)
            )

            result = await session.execute(query)
            return result.all()  # Возвращаем список кортежей с нужными полями