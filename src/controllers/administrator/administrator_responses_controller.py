from flask import Blueprint, render_template
from src.lib import role_constraint
from src.queries.shared import ResponsesQuery


administrator_responses_blueprint = Blueprint('administrator_responses_controller', 
                                              __name__)
templates_context = 'views/administrator/responses'


@administrator_responses_blueprint.get('/administrator/responses')
@role_constraint('administrator')
def index():
    responses = ResponsesQuery({'order_by': 'created_at', 'order': 'desc' }).get_responses()

    return render_template(f"{templates_context}/index.jinja")


@administrator_responses_blueprint.get('/administrator/responses/<int:response_id>')
@role_constraint('administrator')
def show(response_id: int):
    pass