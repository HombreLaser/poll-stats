from flask import Blueprint, request, flash, url_for, redirect, render_template
from src.lib import role_constraint
from src.database import db
from src.database.models import InterpreterUpload
from src.services.administrator import SQLInterpreter


sql_interpreter_blueprint = Blueprint('sql_interpreter_controller', __name__)


@sql_interpreter_blueprint.post('/sql/uploads/<int:upload_id>')
@role_constraint('administrator')
def create(upload_id: int):
    upload = db.session.get(InterpreterUpload, upload_id)

    if upload is None:
        flash('La base de datos no existe', 'error')

        return redirect(url_for('sql_interpreter_uploads_controller.index'))

    with SQLInterpreter(upload, request.form.get('sql')) as (results, error):
        if error:
            flash('Revise su sentencia SQL', 'error')

            return redirect(
                url_for('sql_interpreter_uploads_controller.show',
                        upload_id=upload_id)
            )

        return render_template(
            'views/administrator/sql_interpreter_uploads/show.jinja',
            upload=upload, results=results
        )
