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

@router.get('')
async def get_booking(user: Users = Depends(get_current_user)):
    return await BookingDao.find_all(user_id=user.id)
