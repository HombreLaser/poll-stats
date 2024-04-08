from src.forms.base_form import BaseForm
from src.forms.widgets import TextInputWidget, PasswordInputWidget, CheckboxInputWidget, CheckboxLabel
import wtforms.validators as validators
import wtforms


class LoginForm(BaseForm):
    email = wtforms.StringField('Correo electrónico', validators=[validators.InputRequired()], widget=TextInputWidget())
    password = wtforms.StringField('Contraseña', validators=[validators.InputRequired()], widget=PasswordInputWidget())
    remember = wtforms.BooleanField(CheckboxLabel('remember', 'Recordar contraseña'), widget=CheckboxInputWidget())