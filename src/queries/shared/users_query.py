import sqlalchemy
from src.database import db
from src.database.models import UserAccount
from src.queries import BaseQuery


class UsersQuery(BaseQuery):
    def __init__(self, params):
        super().__init__(params, UserAccount)

    def get_administrators(self):
        self.scope = sqlalchemy.select(UserAccount).filter(UserAccount.role == 'administrator')
        
        return self.search().order_by_param().paginate()


def get_user_by_invite_code(invite_code):
    query = sqlalchemy.select(UserAccount).filter(UserAccount.activated == False) \
                                          .filter(UserAccount.invite_code == invite_code)

    return db.session.execute(query).scalar()