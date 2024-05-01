import sqlalchemy
import sqlalchemy.orm as orm
from src.database import db
from src.database.models import Form, Question, UserAccount
from src.queries import JoinedQueryBase


class FormsQuery(JoinedQueryBase):
    def get_forms(self, scope):
        self._scope = scope

        return self.search_joined_with(Form, UserAccount)


def get_form_by_public_key(public_key: str):
    query = (
        sqlalchemy.select(Form)
                  .options(
                      orm.joinedload(
                          Form.questions
                      ).joinedload(Question.options)
                  ).filter(Form.status == 'open')
                   .filter(Form.public_key == public_key)
    )

    return db.session.execute(query).scalar()
