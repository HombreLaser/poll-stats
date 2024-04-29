import sqlalchemy as sa
from src.queries import JoinedQueryBase
from src.database.models import Response, Form


class ResponsesQuery(JoinedQueryBase):
    def get_responses(self):
        return self.search_with_foreign_models(Response, Form)