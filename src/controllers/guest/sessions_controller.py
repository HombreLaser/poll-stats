from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy import select
from src.lib.constraints import redirect_if_logged_in
from src.services.sessions import Login
from src.forms import LoginForm
from src.database import db
from src.database.models import UserAccount

sessions_blueprint = Blueprint('sessions_controller', __name__)


@sessions_blueprint.get('/login')
@redirect_if_logged_in
def new():
    form = LoginForm()

    return render_template('views/sessions/new.jinja', form=form)


@sessions_blueprint.post('/login')
def create():
    form = Login().__call__(LoginForm())

    if form.validate() and not form.form_errors:
        return redirect(url_for('master_dashboards_controller.index'))
    else:
        return render_template('views/sessions/new.jinja', form=form)


@sessions_blueprint.delete('/logout')
def destroy():
    if 'user_id' in session:
        del session['user_id']

    return redirect(url_for('sessions_controller.new'))