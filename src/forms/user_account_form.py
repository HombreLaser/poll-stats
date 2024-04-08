from src.forms import BaseForm
from src.forms.widgets import TextInputWidget
import wtforms.validators as validators
import wtforms


class UserAccountForm(BaseForm):
    email = wtforms.StringField('Correo electrónico', validators=[validators.InputRequired(), validators.Length(max=256),
                                                                  validators.Email()], 
                                                      widget=TextInputWidget())
    first_name = wtforms.StringField('Nombre(s)', validators=[validators.InputRequired(), validators.Length(max=64)],
                                                  widget=TextInputWidget())
    last_name = wtforms.StringField('Apellido(s)', validators=[validators.InputRequired(), validators.Length(64)],
                                                   widget=TextInputWidget())