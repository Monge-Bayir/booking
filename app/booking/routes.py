from fastapi import APIRouter
from app.booking.models import Booking
from app.booking.dao import BookingDao

router = APIRouter(
    prefix='/booking',
    tags=['Бронирование']
)

@router.get('')
async def get_booking():
    return await BookingDao.find_one_or_none(1)
