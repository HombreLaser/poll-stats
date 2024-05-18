from flask import Blueprint, render_template, request, redirect, url_for, \
    session, flash, abort
import sqlalchemy
import sqlalchemy.orm as orm
from src.lib.constraints import role_constraint
from src.database.models import Form, Question
from src.database import db
from src.forms import CustomForm
from src.services.administrator.form_services import CreateForm, UpdateForm
from src.queries.shared import FormsQuery


administrator_forms_blueprint = Blueprint('administrator_forms_controller',
                                          __name__)
templates_context = 'views/administrator/forms'


@administrator_forms_blueprint.get('/administrator/forms')
@role_constraint('administrator')
def index():
    scope = sqlalchemy.select(Form) \
                      .filter(Form.user_account_id == session.get('user_id'))
    query = FormsQuery(request.args)
    forms = query.get_forms(scope)

    return render_template(f"{templates_context}/index.jinja", forms=forms)


@administrator_forms_blueprint.get('/administrator/forms/new')
@role_constraint('administrator')
def new():
    form = CustomForm()

    return render_template(f"{templates_context}/new.jinja", form=form)


@administrator_forms_blueprint.get('/administrator/forms/<int:form_id>/edit')
@role_constraint('administrator')
def edit(form_id):
    stmt = (
        sqlalchemy.select(Form)
                  .options(orm.joinedload(Form.questions)
                           .joinedload(Question.options))
                  .filter(Form.id == form_id)
    )
    form = db.session.execute(stmt).scalar()

    if form is not None:
        service = CreateForm({})
        custom_form = service.create_form_from_instance(form)

        return render_template(f"{templates_context}/edit.jinja",
                               form=custom_form, form_instance=form)

    return redirect(url_for('administrator_forms_controller.index'))


@administrator_forms_blueprint.put('/administrator/forms/<int:form_id>')
@role_constraint('administrator')
def update(form_id):
    form = db.get_or_404(Form, form_id)
    update_service = UpdateForm(form, request.form)
    update_service.call()

    if update_service.errors:
        return update_service.errors, 422

    return redirect(url_for('administrator_forms_controller.edit',
                            form_id=form.id)), 303


@administrator_forms_blueprint.post('/administrator/forms')
@role_constraint('administrator')
def create():
    form_creation_service = CreateForm(request.form)
    form = form_creation_service.call()

    if form_creation_service.errors:
        return form_creation_service.errors, 422

    flash('El formulario se ha creado con éxito', 'success')

    return redirect(url_for('administrator_forms_controller.edit',
                            form_id=form.id))


@administrator_forms_blueprint.post('/administrator/forms/<int:form_id>/publish')
@role_constraint('administrator')
def publish(form_id: int):
    form = db.session.get(Form, form_id)

    if form is None or form.status == 'open':
        abort(404)

    form.status = 'open'
    db.session.commit()

    return redirect(url_for('administrator_forms_controller.index'))


@administrator_forms_blueprint.post('/administrator/forms/<int:form_id>/close')
@role_constraint('administrator')
def close(form_id: int):
    form = db.session.get(Form, form_id)

    if form is None or form.status == 'review':
        abort(404)

    form.status = 'closed'
    db.session.commit()
    flash('El formulario ha sido cerrado con éxito', 'success')

    return redirect(url_for('administrator_forms_controller.index'))
