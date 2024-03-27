from flask import Blueprint, render_template
from src.lib.constraints import role_constraint


administrator_dashboards_blueprint = Blueprint('administrator_dashboards_controller', __name__)


@administrator_dashboards_blueprint.get('/administrator')
@role_constraint('administrator')
def index():
    return render_template('views/administrator/dashboards/index.jinja')