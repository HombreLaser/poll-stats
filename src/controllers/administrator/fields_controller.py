from flask import Blueprint, render_template, request
from src.lib.constraints import role_constraint
from src.forms import QuestionForm, OptionForm
import secrets


fields_blueprint = Blueprint('fields_controller', __name__)
templates_context = 'views/administrator/fields'


@fields_blueprint.get('/administrator/fields')
@role_constraint('administrator')
def index():
    field_type = request.args.get('field_type')
    form = QuestionForm()

    return render_template(f"{templates_context}/{field_type}.jinja", form=form, button_id=secrets.token_hex(4))


@fields_blueprint.get('/administrator/fields/selection/option')
@role_constraint('administrator')
def option():
    form = OptionForm()

    return render_template(f"{templates_context}/option.jinja", form=form, button_id=secrets.token_hex(4))