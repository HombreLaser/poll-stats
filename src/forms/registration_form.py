from src.forms import BaseForm
from src.forms.widgets import PasswordInputWidget
import wtforms.validators as validators
import wtforms


def validate_password(form, field):
    if form.password.data != field.data:
        raise wtforms.ValidationError('Las contraseñas no coinciden')


class RegistrationForm(BaseForm):
    password = wtforms.StringField('Contraseña', validators=[validators.InputRequired()], widget=PasswordInputWidget())
    password_confirm = wtforms.StringField('Contraseña', validators=[validators.InputRequired(), validate_password],
                                                         widget=PasswordInputWidget())