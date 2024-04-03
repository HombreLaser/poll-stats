from src.tests.utils.factories import QuestionFactory
from . import TestModelBase


class TestQuestion(TestModelBase):
    def test_question_creation(self, app, db):
        question = QuestionFactory.build()
        db.session.add(question)
        db.session.commit()

        assert question.id is not None