from flask import Blueprint, redirect, url_for
from src.lib.constraints import role_constraint


master_dashboards_blueprint = Blueprint('master_dashboards_controller',
                                        __name__)


@master_dashboards_blueprint.get('/master')
@role_constraint('master')
def index():
    return redirect(url_for('users_controller.index'))
