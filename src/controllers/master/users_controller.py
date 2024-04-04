from flask import Blueprint, render_template, request
from src.queries.master import UsersQuery
from src.lib.constraints import role_constraint
from src.queries.master import UsersQuery


users_blueprint = Blueprint('users_controller', __name__)
templates_context = 'views/master/users'


@users_blueprint.get('/master/users')
@role_constraint('master')
def index():
    users = UsersQuery(request.args).get_administrators()

    return render_template(f"{templates_context}/index.jinja", users=users, context=templates_context)