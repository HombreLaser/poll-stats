from flask import Blueprint, render_template, session
import sqlalchemy as sa
import sqlalchemy.orm as orm
from src.database import db
from src.database.models import Response, Form
from src.lib.constraints import role_constraint


administrator_dashboards_blueprint = Blueprint(
    'administrator_dashboards_controller', __name__
)


@administrator_dashboards_blueprint.get('/administrator')
@role_constraint('administrator')
def index():
    query = sa.select(Response).options(orm.joinedload(Response.form)) \
                               .filter(
                                   Form.user_account_id == session['user_id']
                               ).limit(10)
    responses = db.session.execute(query).scalars()

    return render_template('views/administrator/dashboards/index.jinja',
                           responses=responses)
