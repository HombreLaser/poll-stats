from src.forms import BaseForm
from src.forms.widgets import TextInputWidget, VariableIdSelectWidget
from src.forms.fields import ListField
import wtforms.validators as validators
import secrets
import wtforms


def present_options(form, field):
    if not field.data and form.type.data == 'selection':
        raise wtforms.ValidationError('No se introdujeron opciones')


class QuestionForm(BaseForm):
    id = wtforms.IntegerField(widget=wtforms.widgets.HiddenInput())
    content = wtforms.StringField('Contenido', validators=[validators.InputRequired(), validators.Length(max=256)],
                                               widget=TextInputWidget())
    type = wtforms.SelectField('Tipo', validators=[validators.InputRequired()], choices=[('open', 'Abierta'), ('selection', 'Selección')],
                                             widget=VariableIdSelectWidget())
    # required = wtforms.BooleanField('Obligatoria', validators=[validators.InputRequired()])
    options = ListField('Opciones', validators=[present_options])