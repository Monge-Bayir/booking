from typing import Optional, List

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]
    rooms_left: int