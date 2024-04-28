from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from src.forms import CustomForm
from src.database.models import Form
from src.services.guest import SaveResponse
from src.queries.shared import get_form_by_public_key


guest_responses_blueprint = Blueprint('guest_responses_controller', __name__)
templates_context = 'views/guest/responses/'


@guest_responses_blueprint.get('/forms/<form_public_key>/responses/new')
def new(form_public_key):
    form = get_form_by_public_key(form_public_key)

    if form is None:
        flash('No se encontró la encuesta a la que quiere acceder o esta ha sido cerrada', 'error')
        return redirect(url_for('sessions_controller.new'))
    
    csrf_token = CustomForm(name=form.name).csrf_token
    
    return render_template(f"{templates_context}/new.jinja", form=form, csrf_token=csrf_token)
  


@guest_responses_blueprint.post('/forms/<form_public_key>/responses')
def create(form_public_key):
    form = get_form_by_public_key(form_public_key)

    if form is None:
        abort(404)

    service = SaveResponse(form, request.form)
    service.call()
    flash('Gracias por su respuesta.', 'success')

    return redirect(url_for('sessions_controller.new'))