from src.forms.base_form import BaseForm
from src.forms.widgets import FileInputWidget
from flask_wtf.file import FileField, FileRequired, FileAllowed


class InterpreterUploadForm(BaseForm):
    database = FileField(validators=[FileRequired(),
                                     FileAllowed(
                                         ['db', 'sqlite'],
                                         'Sólo se permiten archivos .db y .sqlite'
                                     )],
                         widget=FileInputWidget()
                         )
