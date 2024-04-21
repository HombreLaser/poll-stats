from werkzeug.datastructures import MultiDict
import re


def dict_to_multidict(**kwargs):
    return MultiDict(kwargs)


class RegexMultiDict(MultiDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_key_pool()

    # Regresa un iterador con todos los key-values que cumplen
    # con la expresión regular.
    def items_regex(self, pattern, yield_match=False):
        regex = re.compile(pattern)

        for match in regex.finditer(self._pool):
            value = self.get(match.group(0))

            if yield_match:
                yield match, value
            else:
                yield match.group(0), value

    # Regresa un solo valor relacionado a la expresión regular.
    def item_regex(self, pattern):
        regex = re.compile(pattern)
        key = regex.search(self._pool).group(0)

        return key, self.get(key)

    # Una cadena con todas las keys de un formulario.
    def _init_key_pool(self):
        self._pool = ''

        for key in self.keys():
            self._pool += key + ' '

        self._pool.removesuffix(' ')