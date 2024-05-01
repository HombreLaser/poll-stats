from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.exc import OperationalError
from src.queries import BaseQuery


class JoinedQueryBase(BaseQuery):
    def search_joined_with(self, base_model, *models_to_join, join=True):
        self._scoped = self._scope.whereclause is not None

        if join:
            self._join(*models_to_join)

        for model in models_to_join:
            if self._param_refers_to_model('search_by', model):
                self.search(model)

            if self._param_refers_to_model('order_by', model):
                self.order_by_param(model)

        self._query_base_model(base_model)

        return self.paginate()

    def _join(self, *models_to_join):
        for model in models_to_join:
            self._scope = self._scope.join(model)

    def _param_refers_to_model(self, param, model):
        if self._params.get(param) is None:
            return False

        return model.__tablename__ in self._params.get(param)

    def _query_base_model(self, base_model):
        if not self._performed_search():
            self.search(base_model)

        if not self._performed_ordering():
            self.order_by_param(base_model)

    def _performed_ordering(self):
        return str(self._scope).find('ORDER BY') != -1

    def _performed_search(self):
        if not self._scoped:
            return False

        return (
            not isinstance(self._scope.whereclause, BinaryExpression) and
            len(self._scope.whereclause.clauses) > 1
        )
