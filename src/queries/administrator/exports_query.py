import sqlalchemy
from src.queries import BaseQuery
from src.database.models import Export


class ExportsQuery(BaseQuery):
    def __init__(self, params, user_id):
        super().__init__(params)
        self._user_id = user_id

    def get_exports(self):
        self._scope = sqlalchemy.select(Export) \
                                .filter(Export.owner_id == self._user_id) \
                                .filter(Export.type == 'csv')

        return self.search(Export).order_by_param(Export).paginate()
