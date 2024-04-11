import sqlalchemy
from src.database import db
from src.database.models import Form
from src.queries import BaseQuery


class FormsQuery(BaseQuery):
    def __init__(self, params):
        super().__init__(params, Form)

    def get_forms(self):
        self.scope = sqlalchemy.select(Form)

        return self.search().order_by_param().paginate()