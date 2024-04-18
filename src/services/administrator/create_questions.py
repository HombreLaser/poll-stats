from werkzeug.datastructures import MultiDict
from src.database.models import Question
from src.forms import QuestionForm, OptionForm
from src.database import db


class CreateQuestions:
    def __init__(self, raw_questions: dict):
        self.raw_questions = raw_questions
        self.questions = []
        self.error_messages = {}

    def create_question_forms(self):
        for question in self.raw_questions:
            if question.get('type') == 'open':
                self._create_open_question(question)
            else:
                self._create_selection_question(question)

        self._validate()
        return self.questions

    def save_questions(self, form):
        for question in self.questions:
            question_instance = Question(type=question.type.data, content=question.content.data,
                                         options=question.options.data)
            question_instance.form = form
            db.session.add(question_instance)

        db.session.commit()

    def _validate(self):
        question_errors = []
        option_errors = []

        for question in self.questions:
            question_errors.append(self._validate_question(question))
            option_errors.append(self._validate_options(question.options))

        print('Check')

    def _validate_question(self, question):
        if not question.validate():
            return question.errors

        return None

    def _validate_options(self, options):
        option_errors = []

        for option in options.data:
            if not option.validate():
                    option_errors.append(option.errors)

        return option_errors

    def _create_selection_question(self, question):
        options = []

        for option in question.get('options'):
            options.append(OptionForm(MultiDict(option)))

        question_form = QuestionForm(MultiDict({ 'content': question.get('content'),
                                                 'field_type':'selection',
                                                 'options': options }))
        self.questions.append(question_form)

    def _create_open_question(self, question):
        question_form = QuestionForm(MultiDict({ 'content': question.get('content'), 'field_type': 'open' }))
        self.questions.append(question_form)