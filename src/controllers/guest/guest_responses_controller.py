from flask import Blueprint, render_template
from src.database.models import Form
from src.queries.shared import get_form_by_public_key


guest_responses_blueprint = Blueprint('guest_responses_controller', __name__)


@guest_responses_blueprint.get('/forms/<form_public_key>/responses/new')
def new(form_public_key):
    form = get_form_by_public_key(form_public_key)

    if form is not None:
        return form.public_key
    else:
        return 'not found'