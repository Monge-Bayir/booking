from typing import Optional, List

from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: Optional[List[str]]
    price: int
    quantity: int
    image_id: int
    rooms_left: int

    class Config:
        from_attributes = True