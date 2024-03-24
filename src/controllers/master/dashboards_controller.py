from flask import Blueprint, render_template

dashboards_blueprint = Blueprint('dashboards_controller', __name__)

@dashboards_blueprint.get('/master')
def index():
    return render_template('views/master/dashboards/index.jinja')