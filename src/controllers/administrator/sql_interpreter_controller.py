from flask import Blueprint
from src.lib import role_constraint


sql_interpreter_blueprint = Blueprint('export_files_controller', __name__)


@sql_interpreter_blueprint.get('/sql/upload')
@role_constraint('administrator')
def new():
    
