from werkzeug.datastructures import MultiDict
from src.lib.data_structures import RegexMultiDict, dict_to_multidict


class FormParser:
    def parse(self, form):
        self._form = RegexMultiDict(mapping=form)
        self._questions = []
        self._get_open_questions()
        self._get_selection_questions()

        return MultiDict([('name', self._form.get('name')), ('questions', self._questions)])

    def _get_open_questions(self):
        pattern = 'open\[content\]\[\d\]'

        for key, value in self._form.items_regex(pattern):
            self._questions.append(dict_to_multidict(type='open', content=value))

    def _get_selection_questions(self):
        pattern = 'selection\[content\]\[(?P<id>\d)\]'

        for match, value in self._form.items_regex(pattern, yield_match=True):
            options = self._get_question_options(match['id'])
            self._questions.append(dict_to_multidict(type='selection', content=value,
                                                     options=options))

    def _get_question_options(self, question_id):
        pattern = f"option\[(?P<option_id>\d)\]\[selection\]\[{question_id}\]\[(?P<field>content|score)\]"
        options = []

        for match, value in self._form.items_regex(pattern, yield_match=True):
            if self._form.get(match.group(0)) is None:
                continue
        
            if match['field'] == 'content':
                content = value
                score = self._get_option_attribute(match['option_id'], question_id, 'score')
            else:
                score = value
                content = self._get_option_attribute(match['option_id'], question_id, 'content')

            self._form.pop(match.group(0))
            options.append(dict_to_multidict(content=content, score=score))

        return options

    def _get_option_attribute(self, option_id, question_id, attr):
        pattern = f"option\[{option_id}\]\[selection\]\[{question_id}\]\[{attr}\]"
        key, value = self._form.item_regex(pattern)
        self._form.pop(key)

        return value