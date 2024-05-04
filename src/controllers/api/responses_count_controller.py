from flask import Blueprint, request, session
from src.queries.shared.responses_query import ResponsesOfTheWeek
from src.lib.constraints import role_constraint


responses_count_blueprint = Blueprint('responses_count_controller', __name__)


@responses_count_blueprint.get('/api/responses_count')
@role_constraint('master', 'administrator')
def index():
    type = request.args.get('type')

    query = ResponsesOfTheWeek(session)

    return query.responses_count_by_day()
