from werkzeug.datastructures import MultiDict
from src.lib.data_structures import RegexMultiDict, dict_to_multidict


class FormParser:
    def get_question_ids(self, question_type):
        pattern = f"{question_type}\[content\]\[(?P<question_id>\d+)\]"

        return { match['question_id'] for match, _value in self._form.items_regex(pattern, yield_match=True) }

    def _init_update_patterns(self):
        pass

    def _get_open_questions(self):
        for key, value in self._form.items_regex(self._open_question_pattern):
            self._questions.append(dict_to_multidict(type='open', content=value))

    def _get_selection_questions(self):
        for match, value in self._form.items_regex(self._selection_question_pattern, yield_match=True):
            options = self._get_question_options(match['id'])
            self._questions.append(dict_to_multidict(type='selection', content=value,
                                                     options=options))

    def _get_question_options(self, question_id):
        options = []

        for match, value in self._form.items_regex(self._option_pattern(question_id), yield_match=True):
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
        pattern = self._option_attribute_pattern(option_id, question_id, attr)
        key, value = self._form.item_regex(pattern)
        self._form.pop(key)

        return value

    def _option_attribute_pattern(self, option_id, question_id, attr):
        pass