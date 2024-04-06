import sqlalchemy
from src.database import db
from src.database.models import UserAccount
from src.queries import BaseQuery


class UsersQuery(BaseQuery):
    def __init__(self, params):
        super().__init__(params, UserAccount)
        self.params = params

    def get_administrators(self):
        self.scope = sqlalchemy.select(UserAccount).where(UserAccount.role == 'administrator')
        
        return self._search()._order_by_param()._paginate()
