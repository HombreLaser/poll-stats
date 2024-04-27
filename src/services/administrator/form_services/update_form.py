import sqlalchemy as sa
from src.database import db
from src.database.models import Form, Question, Option
from src.services.administrator.form_services import UpdateQuestions, CreateQuestions, FormsServiceBase
from src.services.administrator.form_services.parsers import UpdateFormParser


class UpdateForm(FormsServiceBase):
    def __init__(self, form_instance, submitted_form):
        super().__init__(submitted_form)
        self._form_instance = form_instance
        self._parser = UpdateFormParser()
        self._new_questions, self._new_options = self._parser.parse(self._submitted_form)
        self._question_creation_service = CreateQuestions(self._new_questions)
        self._question_update_service = UpdateQuestions(self._new_questions, self._new_options)

    def call(self):
        self._check_deletions()
        self._update()

    def _check_deletions(self):
        question_ids = { 
            int(id) for id in self._parser.get_question_ids('selection') | self._parser.get_question_ids('open')
        }
        option_ids = self._parser.get_option_ids()
        self._delete_questions(question_ids)
        self._delete_options(option_ids)

    def _delete_options(self, form_option_ids: set):
        option_ids_to_delete = self._get_option_ids_to_delete(form_option_ids)

        options = db.session.execute(
            sa.select(Option).filter(Option.id.in_(option_ids_to_delete))
        ).scalars()

        for option in options:
            db.session.delete(option)

        db.session.commit()

    def _get_option_ids_to_delete(self, form_option_ids: set):
        return set(
            db.session.execute(
                sa.select(Option.id).join(Option.question.and_(
                    Question.form_id == self._form_instance.id
                ))
            ).scalars()
        ) - form_option_ids

    def _delete_questions(self, form_question_ids: set):
        question_ids_to_delete = self._get_question_ids_to_delete(form_question_ids)

        questions = db.session.execute(
            sa.select(Question).filter(Question.id.in_(question_ids_to_delete))
        ).scalars()

        for question in questions:
            db.session.delete(question)

        db.session.commit()

    def _get_question_ids_to_delete(self, form_question_ids: set):
        return set(
            db.session.execute(
                sa.select(Question.id).filter(Question.form_id == self._form_instance.id)
            ).scalars()
        ) - form_question_ids

    def _update(self):
        self._question_creation_service.create_question_forms()
        self._question_update_service.call()
        self._validate()

        if not self._errors:
            self._question_creation_service.save_questions(self._form_instance)