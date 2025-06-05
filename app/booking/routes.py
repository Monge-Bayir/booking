from fastapi import APIRouter
from app.booking.schemas import SBooking
from app.booking.dao import BookingDao

router = APIRouter(
    prefix='/booking',
    tags=['Бронирование']
)

@router.get('')
async def get_booking() -> list[SBooking]:
    return await BookingDao.find_all()
