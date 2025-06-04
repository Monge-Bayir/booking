from app.database import async_session_maker
from sqlalchemy import select

class BaseDao:
    model = None

    @classmethod
    async def find_one_or_none(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            res = await session.execute(query)
            return res.scalars().all()
