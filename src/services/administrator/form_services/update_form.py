from src.database.models import Form
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
        self._update()

    def _update(self):
        self._question_creation_service.create_question_forms()
        self._question_update_service.call()
        self._validate()

        if not self._errors:
            self._question_creation_service.save_questions(self._form_instance)