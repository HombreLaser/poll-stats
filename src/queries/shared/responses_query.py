import sqlalchemy as sa
from src.queries import JoinedQueryBase
from src.database.models import Response, Form


class ResponsesQuery(JoinedQueryBase):
    def __init__(self, params, user_id):
        super().__init__(params | { 'filter_by': 'form.user_account_id', 'filter': user_id })
        self._user_id = user_id

    def get_responses(self):
        return self.search_with_foreign_models(Response, Form)