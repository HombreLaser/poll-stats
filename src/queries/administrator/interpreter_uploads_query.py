import sqlalchemy
from src.queries import BaseQuery
from src.database.models import InterpreterUpload


class InterpreterUploadsQuery(BaseQuery):
    def __init__(self, params, user_id):
        super().__init__(params)
        self._user_id = user_id

    def get_uploads(self):
        self._scope = sqlalchemy.select(InterpreterUpload) \
                                .filter(
                                    InterpreterUpload.owner_id ==
                                    self._user_id)

        return self.search(InterpreterUpload) \
                   .order_by_param(InterpreterUpload) \
                   .paginate()
