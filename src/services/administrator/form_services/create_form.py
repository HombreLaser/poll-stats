from flask import session
from src.database.models import Form, UserAccount
from src.forms import CustomForm
from src.services.administrator.form_services import CreateQuestions, FormsServiceBase
from src.services.administrator.form_services.parsers import NewFormParser
from src.database import db
from src.lib import dict_to_multidict
import secrets


class CreateForm(FormsServiceBase):
    def __init__(self, submitted_form):
        super().__init__(submitted_form)
        self._parser = NewFormParser()
        self._submitted_form = self._parser.parse(self._submitted_form)
        self._question_creation_service = CreateQuestions(self._submitted_form.get('questions'))
        self._user_account = db.session.get(UserAccount, session.get('user_id'))

    def call(self):
        self._form = self._create_form()
        self._validate()

        if not self._errors:
            self._save_form()

    def create_form_from_instance(self, form_instance):
        question_forms = self._question_creation_service \
                             .create_question_forms_from_instances(form_instance.questions)
        custom_form = CustomForm(obj=form_instance)
        custom_form.questions.data = question_forms

        return custom_form

    @property
    def form(self):
        return self._form

    def _save_form(self):
        form = Form(name=self._form.name.data, status='review', public_key=secrets.token_hex(12), author=self._user_account)
        form.author = self._user_account
        db.session.add(form)
        db.session.commit()
        self._question_creation_service.save_questions(form)

    def _create_form(self):
        form = CustomForm(dict_to_multidict(name=self._submitted_form.get('name')))
        form.questions = self._question_creation_service.create_question_forms()

        return form