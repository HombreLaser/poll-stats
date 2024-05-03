import sqlalchemy
from src.database import db
from src.database.models import UserAccount
from src.queries import BaseQuery


class UsersQuery(BaseQuery):
    def __init__(self, params):
        super().__init__(params)

    def get_administrators(self):
        self._scope = sqlalchemy.select(UserAccount) \
                                .filter(UserAccount.role == 'administrator')

        return self.search(UserAccount).order_by_param(UserAccount).paginate()


def get_user_by_invite_code(invite_code):
    query = sqlalchemy.select(UserAccount).filter(UserAccount.activated == False) \
                                          .filter(UserAccount.invite_code == invite_code)

    return db.session.execute(query).scalar()
