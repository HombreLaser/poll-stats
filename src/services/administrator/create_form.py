from flask import session
from src.database.models import Form, UserAccount, Question
from src.forms import QuestionForm, OptionForm, CustomForm
from src.database import db
import secrets


class CreateForm:
    def __init__(submitted_form: dict):
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
        form = CustomForm(name=self.submitted_form.get('name'))
        form.questions = self.question_creation_service.create_question_forms()

        return form


class CreateQuestions:
    def __init__(raw_questions: dict):
        self.raw_questions = raw_questions
        self.questions = []

    def create_question_forms(self):
        for question in self.raw_questions:
            if question.get('type') == 'open':
                self._create_open_question(question)
            else:
                self._create_selection_question(question)

        # self._validate_questions()
        return self.questions

    def save_questions(self, form):
        # if self.validate()...
        for question in self.questions:
            question_instance = Question(type=question.type.data, content=question.content.data,
                                         options=question.options.data)
            question_instance.form = form
            db.session.add(question_instance)

        db.session.commit()

    def _create_selection_question(self, question):
        question_form = QuestionForm(content=question.get('content'), field_type='selection')
        options = []

        for option in question.get('options'):
            options.append(OptionForm(content=option.get('content'), score=option.get['score']))

        question_form.options = options
        self.questions.append(question_form)

    def _create_open_question(self, question):
        question_form = QuestionForm(content=question.get('content'), field_type='open')
        self.questions.append(question_form)