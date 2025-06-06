import datetime
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UserDao


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token decode error")

    expire_timestamp = payload.get("exp")
    if not expire_timestamp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing expiration")

    expire_datetime = datetime.datetime.utcfromtimestamp(expire_timestamp)
    if expire_datetime < datetime.datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    user = await UserDao.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user