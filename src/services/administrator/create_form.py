from flask import session
from src.database.models import Form, UserAccount
from src.forms import CustomForm
from src.services.administrator import CreateQuestions
from src.database import db
from src.lib import dict_to_multidict
import secrets


class CreateForm:
    def __init__(self, submitted_form: dict):
        self._submitted_form = submitted_form
        self._question_creation_service = CreateQuestions(self._submitted_form.get('questions'))
        self._user_account = db.session.get(UserAccount, session.get('user_id'))
        self._errors = {}

    def call(self):
        self.form = self._create_form()
        self._validate()

    @property
    def errors(self):
        return self._errors

    def _validate(self):
        self._errors = self._question_creation_service.errors

        if not self.form.validate():
            self._errors['form'] = self.form.errors

    def _save_form(self):
        form = Form(name=self.form.name.data, status='review', public_key=secrets.token_hex(12))
        form.author = self._user_account
        db.session.add(form)
        db.session.commit(form)
        self._question_creation_service.save_questions(form)

    def _create_form(self):
        form = CustomForm(dict_to_multidict(name=self._submitted_form.get('name')))
        form.questions = self._question_creation_service.create_question_forms()

        return form