from src.forms import BaseForm
from src.forms.widgets import TextInputWidget
from src.forms.fields import ListField
import wtforms.validators as validators
import wtforms


def present_questions(form, field):
    if not field:
        raise wtforms.ValidationError('Formulario vacío')


def question_limit(form, field):
    if len(field.data) > 12:
        raise wtforms.ValidationError('Supera el límite de preguntas')


class CustomForm(BaseForm):
    id = wtforms.IntegerField(widget=wtforms.widgets.HiddenInput())
    name = wtforms.StringField('Nombre', validators=[validators.InputRequired(), validators.Length(max=512)],
                                         widget=TextInputWidget())
    questions = ListField('Preguntas', validators=[present_questions, question_limit])