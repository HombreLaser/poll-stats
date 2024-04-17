from flask import Blueprint, render_template, request, redirect, url_for
from src.lib.constraints import role_constraint
from src.forms import CustomForm
from src.queries.shared import FormsQuery


administrator_forms_blueprint = Blueprint('administrator_forms_controller', __name__)
templates_context = 'views/administrator/forms'


@administrator_forms_blueprint.get('/administrator/forms')
@role_constraint('administrator')
def index():
    query = FormsQuery(request.args)
    forms = query.get_forms()

    return render_template(f"{templates_context}/index.jinja", forms=forms)


@administrator_forms_blueprint.get('/administrator/forms/new')
@role_constraint('administrator')
def new():
    form = CustomForm()

    return render_template(f"{templates_context}/new.jinja", form=form)


@administrator_forms_blueprint.post('/administrator/forms')
@role_constraint('administrator')
def create():
    form = request

    return redirect(url_for('administrator_forms_controller.index'))