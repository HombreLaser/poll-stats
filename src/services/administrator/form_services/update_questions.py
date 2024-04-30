import sqlalchemy
from src.database.models import Question, Option
from src.forms import QuestionForm, OptionForm
from src.database import db
from src.services.administrator.form_services import QuestionsServiceBase


class UpdateQuestions(QuestionsServiceBase):
    def __init__(self, new_questions, new_options):
        super().__init__()
        self._new_options = new_options

    def call(self):
        self._validate()

        if self._errors:
            return

        question_ids = list(self._new_options.keys())
        stmt = sqlalchemy.select(Question).filter(Question.id.in_(question_ids))
        questions = db.session.execute(stmt).scalars()
        self._update(questions)
        db.session.commit()

        pass

    def _update(self, questions):
        for question in questions:
            for option_form in self._new_options[str(question.id)]:
                option = Option(question=question, content=option_form.content.data,
                                score=option_form.score.data)
                db.session.add(option)
