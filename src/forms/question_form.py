from src.forms import BaseForm
from src.forms.widgets import TextInputWidget, VariableIdSelectWidget
import wtforms.validators as validators
import secrets
import wtforms


class QuestionForm(BaseForm):
    content = wtforms.StringField('Contenido', validators=[validators.InputRequired(), validators.Length(max=256)],
                                               widget=TextInputWidget())
    field_type = wtforms.SelectField('Tipo', validators=[validators.InputRequired()], choices=[('open', 'Abierta'), ('selection', 'Selección')],
                                             widget=VariableIdSelectWidget())
    required = wtforms.BooleanField('Obligatoria', validators=[validators.InputRequired()])