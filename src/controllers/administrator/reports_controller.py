from flask import Blueprint, render_template
from src.database.models import Response
from src.database import db


reports_blueprint = Blueprint('reports_controller', __name__)
templates_context = 'views/administrator/reports'


@reports_blueprint.get('/administrator/reports/<int:form_id>')
def show(form_id: int):
    return render_template(f"{templates_context}/show.jinja")
