from flask import session
from werkzeug.datastructures import MultiDict
from src.database.models import Form, UserAccount
from src.forms import CustomForm
from src.services.administrator import CreateQuestions
from src.database import db
import secrets


class CreateForm:
    def __init__(self, submitted_form: dict):
        self.submitted_form = submitted_form
        self.question_creation_service = CreateQuestions(self.submitted_form.get('questions'))
        self.user_account = db.session.get(UserAccount, session.get('user_id'))

    def call(self):
        self.form = self._create_form()

    def _validate(self):
        pass

    def _save_form(self):
        form = Form(name=self.form.name.data, status='review', public_key=secrets.token_hex(12))
        form.author = self.user_account
        db.session.add(form)
        db.session.commit(form)
        self.question_creation_service.save_questions(form)

    def _create_form(self):
        form = CustomForm(MultiDict({ 'name': self.submitted_form.get('name') }))
        form.questions = self.question_creation_service.create_question_forms()

        return form