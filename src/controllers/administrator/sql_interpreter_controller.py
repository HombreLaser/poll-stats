from flask import Blueprint
from src.lib import role_constraint


sql_interpreter_blueprint = Blueprint('sql_interpreter_controller', __name__)


@sql_interpreter_blueprint.post('/sql/uploads<int:upload_id>')
@role_constraint('administrator')
def create(upload_id: int):
    pass
