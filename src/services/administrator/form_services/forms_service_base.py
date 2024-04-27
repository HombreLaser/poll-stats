class FormsServiceBase:
    def __init__(self, submitted_form):
        self._form = None
        self._question_creation_service = None
        self._question_update_service = None
        self._submitted_form = submitted_form
        self._errors = {}

    @property
    def errors(self):
        return self._errors

    def _validate(self):
        self._errors |= self._question_creation_service.errors if self._question_creation_service is not None else {}
        self._errors |= self._question_update_service.errors if self._question_update_service is not None else {} 

        if self._form and not self._form.validate():
            self._errors['form'] = self._form.errors