from flask import Blueprint, session, request, render_template, redirect, \
    url_for
from src.forms import CSVExportForm
from src.services.administrator.exporters import begin_export_to_sqlite
from src.queries.administrator import ExportsQuery
from src.lib.constraints import role_constraint


sqlite_exports_blueprint = Blueprint('sqlite_exports_controller', __name__)
templates_context = 'views/administrator/sqlite_exports'


@sqlite_exports_blueprint.get('/administrator/exports/sqlite')
@role_constraint('administrator')
def index():
    query = ExportsQuery(request.args, session.get('user_id'))
    form = CSVExportForm()

    return render_template(f"{templates_context}/index.jinja", form=form,
                           exports=query.get_exports('sqlite'))


@sqlite_exports_blueprint.post('/administrator/exports/sqlite')
@role_constraint('administrator')
def create():
    begin_export_to_sqlite(session.get('user_id'))

    return redirect(url_for('sqlite_exports_controller.index'))
