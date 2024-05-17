from flask import Blueprint, render_template, flash, url_for, redirect
from src.database.models import Response, Form
from src.database import db
from src.services.administrator import response_score_count


reports_blueprint = Blueprint('reports_controller', __name__)
templates_context = 'views/administrator/reports'


@reports_blueprint.get('/administrator/reports/<int:form_id>')
def show(form_id: int):
    form = db.session.get(Form, form_id)
    score_counts = response_score_count(form.responses)

    if form is None:
        flash('No se encontró el formulario al que quiso acceder', 'error')

        return redirect(url_for('administrator_forms_controller.index'))

    return render_template(f"{templates_context}/show.jinja", form=form,
                           score_counts=score_counts)
