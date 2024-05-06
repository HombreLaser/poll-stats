from src.database.models import Form
from src.database import db
from src.forms.base_form import BaseForm
import src.forms.widgets as widgets
import sqlalchemy as sa
import wtforms.validators as validators
from wtforms_sqlalchemy.fields import QuerySelectField


def choices(user_id):
    query = sa.select(Form) \
              .filter(Form.user_account_id == user_id)

    return db.session.execute(query).scalars()


class CSVExportForm(BaseForm):
    form_id = QuerySelectField('Formulario a exportar',
                                      widget=widgets.SelectWidget(),
                                      validators=[
                                          validators.input_required()
                                      ])
