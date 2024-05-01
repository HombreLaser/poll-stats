from flask import Blueprint, request, render_template
import sqlalchemy
import sqlalchemy.orm as orm
from src.queries.shared import FormsQuery
from src.database.models import Form
from src.lib.constraints import role_constraint


master_forms_blueprint = Blueprint('master_forms_controller', __name__)
templates_context = 'views/master/forms'


@master_forms_blueprint.get('/master/forms')
@role_constraint('master')
def index():
    scope = sqlalchemy.select(Form).options(orm.joinedload(Form.author))
    query = FormsQuery(request.args)
    forms = query.get_forms(scope)

    return render_template(f"{templates_context}/index.jinja", forms=forms)
