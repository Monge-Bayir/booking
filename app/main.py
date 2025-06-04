import uvicorn
from fastapi import FastAPI, Query
from typing import Optional
from app.booking.routes import router as router_booking

from pydantic import BaseModel

app = FastAPI()

app.include_router(router_booking)


@app.get('/hotels/{hotels_id}')
def get_hotels(hotels_id: int, date_to: str, date_from: str, stars: Optional[int] = Query(None, ge=1, le=5), has_spa: Optional[bool]=None):
    return hotels_id

class BookingSchema(BaseModel):
    room_id: int
    date_to: str
    date_from: str


@app.post('/booking')
def add_booking(booking: BookingSchema):
    pass


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)