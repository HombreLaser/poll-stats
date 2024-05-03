from flask import Blueprint, request, render_template, flash, redirect, url_for
import sqlalchemy
import sqlalchemy.orm as orm
from src.database import db
from src.queries.shared import FormsQuery, preloaded_form
from src.database.models import Form
from src.lib.constraints import role_constraint


master_forms_blueprint = Blueprint('master_forms_controller', __name__)
templates_context = 'views/master/forms'


@master_forms_blueprint.get('/master/forms')
@role_constraint('master')
def index():
    scope = sqlalchemy.select(Form).options(orm.joinedload(Form.author))
    query = FormsQuery(request.args)
    forms = query.get_forms(scope)

    return render_template(f"{templates_context}/index.jinja", forms=forms)


@master_forms_blueprint.get('/master/forms/<int:form_id>')
@role_constraint('master')
def show(form_id):
    form = db.session.execute(preloaded_form().filter(Form.id == form_id)) \
                     .scalar()

    if form is None:
        flash('No se encontró el formulario al que desea acceder', 'error')

        return redirect(url_for('master_forms_controller.index'))

    return render_template(f"{templates_context}/show.jinja", form=form)
