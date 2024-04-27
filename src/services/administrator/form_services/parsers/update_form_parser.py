from werkzeug.datastructures import MultiDict
from src.lib.data_structures import RegexMultiDict
from src.lib.data_structures import dict_to_multidict
from src.forms import OptionForm
from src.services.administrator.form_services.parsers import FormParser


class UpdateFormParser(FormParser):
    def __init__(self):
        self._questions = []
        self._options = {}
        self._open_question_pattern = 'new_open\[content\]\[\d+\]'
        self._selection_question_pattern = 'new_selection\[content\]\[(?P<id>\d+)\]'

    def parse(self, form):
        self._form = RegexMultiDict(mapping=form)
        self._get_open_questions()
        self._get_selection_questions()
        self._get_new_options()

        return self._questions, self._options

    def _option_pattern(self, question_id):
        return f"new_option\[(?P<option_id>\d+)\]\[new_selection\]\[{question_id}\]\[(?P<field>content|score)\]"

    def _option_attribute_pattern(self, option_id, question_id, attr):
        return f"new_option\[{option_id}\]\[new_selection\]\[{question_id}\]\[{attr}\]"

    def _get_new_options(self):
        question_ids = self.get_question_ids('selection')
        options = {}

        for question_id in question_ids:
            pattern = f"new_option\[(?P<option_id>\d)\]\[selection\]\[{question_id}\]\[(?P<field>content|score)\]"
            question_options = {}

            for match, value in self._form.items_regex(pattern, yield_match=True):
                if match['option_id'] in question_options:
                    question_options[match['option_id']] |= { match['field']: value }
                    continue

                question_options[match['option_id']] = { match['field']: value}
            
            if question_options:
                options[question_id] = [
                    OptionForm(dict_to_multidict(**new_options)) for _option_id, new_options in question_options.items() 
                    if question_options[_option_id]
                ]

        self._options = options