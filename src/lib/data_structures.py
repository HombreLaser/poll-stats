from werkzeug.datastructures import MultiDict


def dict_to_multidict(**kwargs):
    return MultiDict(kwargs)