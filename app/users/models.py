from app.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)