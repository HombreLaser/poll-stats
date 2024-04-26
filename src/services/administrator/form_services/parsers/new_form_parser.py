from src.services.administrator.form_services.parsers import FormParser


class NewFormParser(FormParser):
    def __init__(self):
        self._open_question_pattern = 'open\[content\]\[\d\]'
        self._selection_question_pattern = 'selection\[content\]\[(?P<id>\d)\]'

    def parse(self, form):
        self._form = RegexMultiDict(mapping=form)
        self._questions = []
        self._get_open_questions()
        self._get_selection_questions()

        return MultiDict([('name', self._form.get('name')), ('questions', self._questions)])

    def _option_pattern(self, question_id):
        return f"option\[(?P<option_id>\d)\]\[selection\]\[{question_id}\]\[(?P<field>content|score)\]"
