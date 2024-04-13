from src.forms import BaseForm
from src.forms.widgets import TextInputWidget, VariableIdSelectWidget
import wtforms.validators as validators
import wtforms


class OptionForm(BaseForm):
    content = wtforms.StringField('Contenido', validators=[validators.InputRequired(), validators.Length(max=256)],
                                               widget=TextInputWidget())
    score = wtforms.SelectField('Puntaje de riesgo', validators=[validators.InputRequired()], 
                                                     choices=[(0, 'Nulo'), (0.3, 'Bajo'), (0.6, 'Medio'), (1, 'Alto')])