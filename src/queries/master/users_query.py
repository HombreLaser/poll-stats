import sqlalchemy
from src.database import db
from src.database.models import UserAccount
from src.queries import BaseQuery


class UsersQuery(BaseQuery):
    def __init__(self, params):
        super().__init__()
        self.params = params

    def get_administrators(self):
        statement = sqlalchemy.select(UserAccount).where(UserAccount.role == 'administrator')
        
        return self.session.execute(statement).scalars()
