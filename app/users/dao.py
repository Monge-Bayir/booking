from app.dao.base import BaseDao
from app.users.models import Users


class UserDao(BaseDao):
    model = Users