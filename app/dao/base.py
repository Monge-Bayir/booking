from app.database import async_session_maker
from sqlalchemy import select, insert

class BaseDao:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter)
            res = await session.execute(query)
            return res.scalar_one_or_none()

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
