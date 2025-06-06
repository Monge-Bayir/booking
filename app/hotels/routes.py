from fastapi import APIRouter, Query
from app.hotels.dao import HotelDao
from datetime import date

from app.hotels.schemas import SHotel

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get('')
async def get_hotels():
    return await HotelDao.find_all()


@router.get('/id/{hotel_id}')
async def get_hotel_by_id(hotel_id: int):
    return await HotelDao.find_by_id(hotel_id)


@router.get("/{location}", response_model=list[SHotel])
async def get_hotels_by_location(
    location: str,
    date_from: date = Query(..., description="Дата заезда"),
    date_to: date = Query(..., description="Дата выезда")
):
    hotels = await HotelDao.find_all_with_free_rooms(location, date_from, date_to)
    return hotels