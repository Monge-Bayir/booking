from app.booking.models import Booking
from app.database import async_session_maker
from sqlalchemy import select, insert, delete

class BaseDao:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_all_by_user(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(user_id=user_id)
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, id):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=id)
            await session.execute(query)
            await session.commit()