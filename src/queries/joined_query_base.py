import inflection
import sqlalchemy as sa
import sqlalchemy.orm as orm
from src.queries import BaseQuery


class JoinedQueryBase(BaseQuery):
    def search_with_foreign_models(self, base_model, *models_to_join):
        self._base_model = base_model
        self._model_to_order_by = None
        subqueries = []
        searched = False
        filtered = False

        for model in models_to_join:
            self._scope = sa.select(model)

            if self._query_param_refers_to_model('search_by', model):
                searched = True
                self.search(model)

            if self._query_param_refers_to_model('filter_by', model):
                filtered = True
                self.filter(model)

            if self._query_param_refers_to_model('order_by', model):
                self._model_to_order_by = model

            subqueries.append(orm.aliased(model, self._scope.subquery(),
                                          name=inflection.underscore(
                                              model.__name__)))

        self._scope_to_base_model(searched, filtered, *subqueries)
        self._build_query(subqueries)

        return self

    def _build_query(self, subqueries: list):
        for subquery in subqueries:
            self._scope = self._scope.join(subquery)

    def _scope_to_base_model(self, searched, filtered, *subqueries):
        self._scope = sa.select(self._base_model, *subqueries)

        if not searched:
            self.search(self._base_model)

        if not filtered:
            self.filter(self._base_model)

        self._order_scope()

    def _order_scope(self):
        if self._model_to_order_by:
            self._scope = self._scope.join(self._model_to_order_by)
            self.order_by_param(self._model_to_order_by)

            return

        self.order_by_param(self._base_model)

    def _query_param_refers_to_model(self, query_param, model):
        if self._params.get(query_param) is None:
            return False

        return inflection.underscore(model.__name__) in self._params \
                                                            .get(query_param) \
                                                            .split('.')
