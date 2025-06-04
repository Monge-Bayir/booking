from app.dao.base import BaseDao
from app.booking.models import Booking

class BookingDao(BaseDao):
    model = Booking