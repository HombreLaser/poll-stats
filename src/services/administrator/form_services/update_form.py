from src.database.models import Form


class UpdateForm:
    def __init__(form_instance, submitted_form):
        self._operations = self._build_operations_hash()

    def _build_operations_hash(self):
        pass

    def _get_new_questions(self):
        pass