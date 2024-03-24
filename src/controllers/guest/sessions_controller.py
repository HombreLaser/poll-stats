from flask import Blueprint, render_template

sessions_blueprint = Blueprint('sessions_controller', __name__)


@sessions_blueprint.get('/login')
def new():
    return 'GET LOGIN'


@sessions_blueprint.post('/login')
def create():
    pass


