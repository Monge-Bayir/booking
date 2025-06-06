import uvicorn
from fastapi import FastAPI, Query
from typing import Optional
from app.booking.routes import router as router_booking
from app.users.routes import router as router_user_register
from app.hotels.routes import router as router_hotel
from app.rooms.routes import router as router_room

from pydantic import BaseModel

app = FastAPI()

app.include_router(router_user_register)
app.include_router(router_booking)
app.include_router(router_hotel)
app.include_router(router_room)




if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)