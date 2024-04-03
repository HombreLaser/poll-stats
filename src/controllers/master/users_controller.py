from flask import Blueprint
from src.lib.constraints import role_constraint


users_blueprint = Blueprint('users_controller', __name__)


@users_blueprint.get('/master/users')
@role_constraint('master')
def index():
    return 'Hello'