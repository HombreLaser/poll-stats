from flask import Blueprint, redirect, url_for, render_template, request
import sqlalchemy
from src.database.models import UserAccount
from src.queries.shared import get_user_by_invite_code
from src.forms import RegistrationForm
from src.lib.constraints import redirect_if_logged_in
from src.services.shared import activate_user
from src.services.sessions import set_session
from src.database import db


registrations_blueprint = Blueprint('registrations_controller', __name__)
templates_context = 'views/guest/registrations'


@registrations_blueprint.get('/register/<invite_code>')
@redirect_if_logged_in
def new(invite_code):
    user = get_user_by_invite_code(invite_code)
    form = RegistrationForm()

    if user is None:
        return redirect(url_for('sessions_controller.new'))
    
    return render_template('views/guest/registrations/new.jinja', form=form, invite_code=invite_code)


@registrations_blueprint.post('/register/<invite_code>')
def create(invite_code):
    user = get_user_by_invite_code(invite_code)

    if user is None:
        return redirect(url_for('sessions_controller.new'))

    form = RegistrationForm(request.form)

    if form.validate():
        activate_user(user, form)
        set_session(user)

        return redirect(url_for('administrator_dashboards_controller.index'))
    
    return render_template(f"{templates_context}/new.jinja", form=form, invite_code=invite_code)
