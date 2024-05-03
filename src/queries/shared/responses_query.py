import sqlalchemy as sa
from sqlalchemy import orm
from src.queries import JoinedQueryBase
from src.database.models import Response, Form


class ResponsesQuery(JoinedQueryBase):
    def __init__(self, params, user_id):
        super().__init__(params)
        self._user_id = user_id

    def get_responses(self):
        self._scope = sa.select(Response) \
                        .join(Response.form) \
                        .options(orm.contains_eager(Response.form)) \
                        .filter(Form.user_account_id == self._user_id)

        return self.search_joined_with(Response, Form, join=False)
