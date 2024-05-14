from flask import Blueprint
from src.lib import role_constraint


sql_interpreter_blueprint = Blueprint('export_files_controller', __name__)


@sql_interpreter_blueprint.get('/sql/uploads')
@role_constraint('administrator')
def index():
    pass


@sql_interpreter_blueprint.get('/sql/uploads/<int:upload_id>')
@role_constraint('administrator')
def show(upload_id: int):
    pass


@sql_interpreter_blueprint.post('/sql/uploads/<int:upload_id>/queries')
@role_constraint('administrator')
def show(upload_id: int):
    pass
