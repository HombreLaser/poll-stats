import sqlalchemy as sa
from src.queries import JoinedQueryBase
from src.database.models import Response, Form


class ResponsesQuery(JoinedQueryBase):
    def get_responses(self):
        return self.search_with_foreign_models(Response, Form)

    def _order_by_form_param(self):
        if 'form' in self._params.get('order_by'):
            return True

        return False