from flask import Blueprint, render_template
from src.lib.constraints import role_constraint


master_dashboards_blueprint = Blueprint('master_dashboards_controller', __name__)


@master_dashboards_blueprint.get('/master')
@role_constraint('master')
def index():
    return render_template('views/master/dashboards/index.jinja')