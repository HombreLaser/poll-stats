from src.forms import BaseForm
from src.forms.widgets import TextInputWidget
import wtforms.validators as validators
import secrets
import wtforms


class QuestionFormBase(BaseForm):
    content = wtforms.StringField('Contenido', validators=[validators.InputRequired(), validators.Length(max=256)],
                                               widget=TextInputWidget(), id=f"content-{secrets.token_hex(4)}")
    required = wtforms.BooleanField('Obligatoria', validators=[validators.InputRequired()], 
                                                   id=f"required-{secrets.token_hex(4)}")