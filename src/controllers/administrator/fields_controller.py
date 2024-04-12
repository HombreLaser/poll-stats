from flask import Blueprint, render_template, request
from src.lib.constraints import role_constraint
from src.forms import OpenQuestionForm


fields_blueprint = Blueprint('fields_controller', __name__)


@fields_blueprint.get('/administrator/fields')
@role_constraint('administrator')
def show():
    field_type = request.args.get('field_type')
    forms = { 'open': OpenQuestionForm() }

    return render_template(f"views/administrator/fields/{field_type}.jinja", form=forms[field_type])