from src.database import db
import inflection


class BaseQuery:
    def __init__(self, params):
        self._scope = None
        self._model = None
        self._session = db.session
        self._params = params

    def search(self, model):
        if self._params.get('search_by') is None or self._paras.get('search') is None:
            return self

        self._model = model
        search = self._perform_search()

        if search is not None:
            self._scope = search

        return self

    def order_by_param(self):
        # Tal vez queramos ordenar en base a otro modelo. En este caso, el parámetro tendrá
        # la forma table.attribute. Quremos conseguir la cadena attribute para hacer la query.
        order_by_attribute = self._params.get('order_by')
        order_by_attribute = order_by_attribute.rsplit('.')[-1] if order_by_attribute is not None else 'created_at'
        attribute = self._get_model_attribute(order_by_attribute)
        ordered_attribute = self._order(attribute)

        if attribute is not None:
            self._scope = self._scope.order_by(ordered_attribute)

        return self

    def paginate(self):
        return db.paginate(self._scope, **self._pagination_params())

    def _perform_search(self):
        # Mismo caso, pero con búsqueda en vez de ordenamiento.
        search_by = self._params.get('search_by').rsplit('.')[-1] # Posibles queries a joins.
        search_term = self._params.get('search')

        try:
           return self._scope.filter(getattr(self._model, search_by).like(f"%{search_term}%"))
        except (AttributeError, TypeError):
            return None

    def _order(self, attribute):
        ordering_method = self._params.get('order')

        if attribute is None:
            return None

        if ordering_method is not None:
            try:
                return getattr(attribute, ordering_method)()
            except AttributeError:
                return getattr(attribute, 'asc')()  
        
        return getattr(attribute, 'asc')()

    def _pagination_params(self):
        page = self._params.get('page')
        per_page = self._params.get('per_page')

        try:
            page = int(page)
        except (ValueError, TypeError):
            page = None

        try:
            per_page = int(per_page)
        except (ValueError, TypeError):
            per_page = None

        return { 
            'page': page,
            'per_page': per_page
        }

    def _get_model_attribute(self, attribute):
        try:
            return getattr(self._model, attribute)
        except (AttributeError, TypeError):
            return None

    @property
    def scope(self):
        return self._scope