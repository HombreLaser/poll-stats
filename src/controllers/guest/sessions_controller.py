from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy import select
from src.lib.constraints import redirect_if_logged_in, session_present
from src.services.sessions import Login
from src.forms import LoginForm
from src.database import db
from src.database.models import UserAccount

sessions_blueprint = Blueprint('sessions_controller', __name__)


@sessions_blueprint.get('/login')
@redirect_if_logged_in
def new():
    form = LoginForm()

    return render_template('views/guest/sessions/new.jinja', form=form)


@sessions_blueprint.post('/login')
def create():
    form = Login().__call__(LoginForm())

    if form.validate() and not form.form_errors:
        return redirect(url_for(f"{session.get('user_role')}_dashboards_controller.index"))
    else:
        return render_template('views/guest/sessions/new.jinja', form=form)


@sessions_blueprint.delete('/logout')
def destroy():
    if session_present():
        del session['user_id']
        del session['user_role']

    return redirect(url_for('sessions_controller.new'), code=303)