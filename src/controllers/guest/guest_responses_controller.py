from flask import Blueprint, render_template
from src.database.models import Form
from src.queries.shared import get_form_by_public_key


guest_responses_blueprint = Blueprint('guest_responses_controller', __name__)
templates_context = 'views/guest/responses/'


@guest_responses_blueprint.get('/forms/<form_public_key>/responses/new')
def new(form_public_key):
    form = get_form_by_public_key(form_public_key)

    if form is not None:
        return render_template(f"{templates_context}/new.jinja", form=form)
    else:
        abort(404)


@guest_responses_blueprint.post('/forms/<form_public_key>/responses/new')
def create(form_public_key):
    return 'Created'