import sqlalchemy
import sqlalchemy.orm as orm
from src.database import db
from src.database.models import Form, Question
from src.queries import BaseQuery


class FormsQuery(BaseQuery):
    def __init__(self, params, user_account_id):
        self._user_account_id = user_account_id
        super().__init__(params)

    def get_forms(self):
        self._scope = sqlalchemy.select(Form).filter(Form.user_account_id == self._user_account_id)

        return self.search(Form).order_by_param().paginate()


def get_form_by_public_key(public_key: str):
    query = (
        sqlalchemy.select(Form)
                  .options(orm.joinedload(Form.questions).joinedload(Question.options))
                  .filter(Form.status == 'open')
                  .filter(Form.public_key == public_key)
    )
                                
    return db.session.execute(query).scalar()