import datetime
from http.client import HTTPException
from fastapi import status

from fastapi import APIRouter
from fastapi.params import Depends

from app.booking.schemas import SBooking
from app.booking.dao import BookingDao
from app.users.dependies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/booking',
    tags=['Бронирование']
)

@router.get("")
async def get_bookings(user=Depends(get_current_user)):
    return await BookingDao.find_all_by_user(user.id)


@router.post('/add_booking')
async def add_booking(room_id: int, date_from: datetime.date, date_to: datetime.date,
                    user: Users = Depends(get_current_user)
                      ):
    booking = await BookingDao.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete('/{booking_id}')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDao.delete_booking(booking_id, user.id)


