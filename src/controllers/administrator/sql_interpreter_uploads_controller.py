from flask import Blueprint, render_template, request, session, \
    flash, redirect, url_for
from src.database import db
from src.database.models import InterpreterUpload
from src.queries.administrator import InterpreterUploadsQuery
from src.forms import InterpreterUploadForm
from src.lib import role_constraint
from src.services.administrator import create_upload


sql_interpreter_uploads_blueprint = Blueprint(
    'sql_interpreter_uploads_controller', __name__
)
templates_context = 'views/administrator/sql_interpreter_uploads'


@sql_interpreter_uploads_blueprint.get('/sql/uploads')
@role_constraint('administrator')
def index():
    query = InterpreterUploadsQuery(request.args, session.get('user_id'))
    form = InterpreterUploadForm()

    return render_template(f"{templates_context}/index.jinja",
                           uploads=query.get_uploads(),
                           form=form)


@sql_interpreter_uploads_blueprint.post('/sql/uploads')
@role_constraint('administrator')
def create():
    form = InterpreterUploadForm()

    if not form.validate():
        flash(form.errors[0], 'error')

        return redirect(url_for('sql_interpreter_uploads_controller.index'))
    create_upload(session.get('user_id'), form)

    return redirect(url_for('sql_interpreter_uploads_controller.index'))


@sql_interpreter_uploads_blueprint.get('/sql/uploads/<int:upload_id>')
@role_constraint('administrator')
def show(upload_id: int):
    upload = db.get_or_404(InterpreterUpload, upload_id)

    return render_template(f"{templates_context}/show.jinja", upload=upload)
