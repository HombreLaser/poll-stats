from src.database.models import Question, Option
from src.forms import QuestionForm, OptionForm
from src.services.administrator.form_services import QuestionsServiceBase
from src.database import db


class CreateQuestions(QuestionsServiceBase):
    def __init__(self, raw_questions: dict):
        super().__init__()
        self._raw_questions = raw_questions

    def create_question_forms_from_instances(self, questions):
        question_forms = []

        for question in questions:
            question_form = QuestionForm(obj=question)
            question_form.options.data = self._create_option_forms_from_instances(
                question.options
            )
            question_forms.append(question_form)

        return question_forms

    def save_questions(self, form):
        for question in self._questions:
            question_instance = Question(type=question.type.data, content=question.content.data, form=form,
                                         score=None)
            self._save_options(question_instance, question.options.data)
            db.session.add(question_instance)

        db.session.commit()

    def _create_option_forms_from_instances(self, options):
        option_forms = []

        for option in options:
            option_forms.append(OptionForm(obj=option))

        return option_forms

    def _save_options(self, question, options):
        for option in options:
            option_instance = Option(content=option.content.data, score=option.score.data, question=question)
            db.session.add(option_instance)