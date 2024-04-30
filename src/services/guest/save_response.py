import json
from werkzeug.datastructures import MultiDict
from src.database import db
from src.database.models import Response


class SaveResponse:
    def __init__(self, form, form_response):
        self._form = form
        self._form_response = form_response

    def call(self):
        responses_json = self._parse_form()
        response = Response(form=self._form, data=responses_json)
        db.session.add(response)
        db.session.commit()

    def _parse_form(self):
        keys = [key for key in self._form_response.keys() if key != 'csrf_token']
        responses = []

        for key in keys:
            response = { 'question': self._form_response.getlist(key)[0], 'type': key }

            if 'selection' in key:
                response['response'] = json.loads(self._form_response.getlist(key)[1])
            else:
                response['response'] = self._form_response.getlist(key)[1]

            responses.append(response)
        
        return responses
