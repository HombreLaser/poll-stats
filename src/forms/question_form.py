from src.forms import BaseForm
from src.forms.widgets import TextInputWidget, VariableIdSelectWidget
from src.forms.fields import OptionsField
import wtforms.validators as validators
import secrets
import wtforms


def present_options(form, field):
    if not field and form.field_type.data == 'selection':
        raise wtforms.ValidationError('No se introdujeron opciones')


class QuestionForm(BaseForm):
    content = wtforms.StringField('Contenido', validators=[validators.InputRequired(), validators.Length(max=256)],
                                               widget=TextInputWidget())
    field_type = wtforms.SelectField('Tipo', validators=[validators.InputRequired()], choices=[('open', 'Abierta'), ('selection', 'Selección')],
                                             widget=VariableIdSelectWidget())
    # required = wtforms.BooleanField('Obligatoria', validators=[validators.InputRequired()])
    options = OptionsField('Opciones', validators=[present_options])