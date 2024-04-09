from flask import Blueprint, render_template, request, redirect, url_for
from src.queries.master import UsersQuery
from src.lib.constraints import role_constraint
from src.queries.master import UsersQuery
from src.services.master import create_user
from src.forms import UserAccountForm


users_blueprint = Blueprint('users_controller', __name__)
templates_context = 'views/master/users'


@users_blueprint.get('/master/users')
@role_constraint('master')
def index():
    users = UsersQuery(request.args).get_administrators()

    return render_template(f"{templates_context}/index.jinja", users=users)


@users_blueprint.get('/master/users/new')
@role_constraint('master')
def new():
    form = UserAccountForm()

    return render_template(f"{templates_context}/new.jinja", form=form)


@users_blueprint.post('/master/users')
@role_constraint('master')
def create():
    form = UserAccountForm(request.form)

    if form.validate():
        user = create_user(form)

        return redirect(url_for('users_controller.index'))
    else:
        return render_template(f"{templates_context}/new.jinja", form=form, status=422)