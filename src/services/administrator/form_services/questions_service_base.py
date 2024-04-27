from src.database.models import Question, Option
from src.forms import QuestionForm, OptionForm
from src.database import db


class QuestionsServiceBase:
    def __init__(self):
        self._questions = []
        self._errors = {}

    def create_question_forms(self):
        for question in self._raw_questions:
            if question.get('type') == 'open':
                self._questions.append(QuestionForm(question))
            else:
                self._create_selection_question(question)

        self._validate()

        return self._questions

    def _create_selection_question(self, question):
        question_form = QuestionForm(question)
        question_form.options.data = []

        for option in question.getlist('options'):
            question_form.options.data.append(OptionForm(option))

        self._questions.append(question_form)

    def _save_options(self, question, options):
        for option in options:
            option_instance = Option(content=option.content.data, score=option.score.data, question=question)
            db.session.add(option_instance)

    def _validate(self):
        question_errors = []
        option_errors = []

        for question in self._questions:
            question_errors.append(self._validate_question(question))
            option_errors.append(self._validate_options(question.options))

        if question_errors.count(None) != len(question_errors):
            self._errors['questions'] = question_errors

        if option_errors.count([]) != len(option_errors):
            self._errors['options'] = option_errors

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

    @property
    def errors(self):
        return self._errors