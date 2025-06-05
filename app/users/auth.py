import datetime
import jwt
from asyncpg.pgproto.pgproto import timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from app.users.dao import UserDao
from app.config import settings

pwd_content = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_content.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDao.find_one_or_none(email=email)
    if not user and verify_password(password, user.password):
        return None
    return user