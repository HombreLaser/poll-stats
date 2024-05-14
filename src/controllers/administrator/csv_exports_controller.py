from flask import Blueprint, session, request, render_template
from src.database import db
from src.database.models import Form
from src.forms import CSVExportForm, choices
from src.queries.administrator import ExportsQuery
from src.lib.constraints import role_constraint


csv_exports_blueprint = Blueprint('csv_exports_controller', __name__)
templates_context = 'views/administrator/csv_exports'


@csv_exports_blueprint.get('/administrator/exports/csv')
@role_constraint('administrator')
def index():
    query = ExportsQuery(request.args, session.get('user_id'))
    form = CSVExportForm()
    form.form_id.query = choices(session.get('user_id'))

    return render_template(f"{templates_context}/index.jinja",
                           exports=query.get_exports('csv'),
                           form=form)


@csv_exports_blueprint.post('/administrator/exports/csv')
@role_constraint('administrator')
def create():
    form_id = int(request.form.get('form_id'))
    form = db.session.get(Form, form_id)
