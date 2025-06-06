from typing import List

from fastapi import APIRouter, Query, HTTPException

from app.rooms.dao import RoomDao
from app.rooms.schemas import RoomResponse
from datetime import date


router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)

@router.get("/hotels/{hotel_id}", response_model=List[RoomResponse])
async def get_rooms(
    hotel_id: int,
    date_from: date = Query(..., alias="date_from"),
    date_to: date = Query(..., alias="date_to"),
):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from must be before date_to")

    rooms = await RoomDao.find_all_by_hotel_with_availability(hotel_id, date_from, date_to)
    return rooms