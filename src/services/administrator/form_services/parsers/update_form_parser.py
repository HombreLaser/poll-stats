from src.services.administrator.form_services.parsers import FormParser


class UpdateFormParser(FormParser):
    def __init__(self):
        self._open_question_pattern = 'new_open\[content\]\[\d\]'
        self._selection_question_pattern = 'new_selection\[content\]\[(?P<id>\d)\]'

    def parse(self, form):
        self._form = RegexMultiDict(mapping=form)
        self._get_open_questions()   

    def _option_pattern(self, question_id):
        return f"new_option\[(?P<option_id>\d)\]\[selection\]\[{question_id}\]\[(?P<field>content|score)\]"