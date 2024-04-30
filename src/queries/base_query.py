from src.database import db


class BaseQuery:
    def __init__(self, params, model):
        self.scope = None
        self.model = model
        self.session = db.session
        self.params = params

    def search(self):
        search = self._perform_search()

        if search is not None:
            self.scope = search

        return self

    def order_by_param(self):
        attribute = self._get_model_attribute(self.params.get('order_by'))
        ordered_attribute = self._order(attribute)

        if attribute is not None:
            self.scope = self.scope.order_by(ordered_attribute)

        return self

    def paginate(self):
        return db.paginate(self.scope, **self._pagination_params())

    def _perform_search(self):
        search_by = self.params.get('search_by')
        search_term = self.params.get('search')

        try:
           return self.scope.filter(getattr(self.model, search_by).like(f"%{search_term}%"))
        except (AttributeError, TypeError):
            return None

    def _order(self, attribute):
        ordering_method = self.params.get('order')

        if attribute is None:
            return None

        if ordering_method is not None:
            try:
                return getattr(attribute, ordering_method)()
            except AttributeError:
                return getattr(attribute, 'asc')()  
        
        return getattr(attribute, 'asc')()

    def _pagination_params(self):
        page = self.params.get('page')
        per_page = self.params.get('per_page')

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
            return getattr(self.model, attribute)
        except (AttributeError, TypeError):
            return None
