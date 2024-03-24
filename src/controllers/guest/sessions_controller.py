from flask import Blueprint, render_template

sessions_blueprint = Blueprint('sessions_controller', __name__)


@sessions_blueprint.get('/login')
def new():
    return render_template('views/sessions/new.jinja')


@sessions_blueprint.post('/login')
def create():
    pass


