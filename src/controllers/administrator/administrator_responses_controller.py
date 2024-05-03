import flask
from src.database import db
from src.database.models import Response
from src.lib import role_constraint
from src.queries.shared import ResponsesQuery


administrator_responses_blueprint = flask.Blueprint(
    'administrator_responses_controller', __name__
)
templates_context = 'views/administrator/responses'


@administrator_responses_blueprint.get('/administrator/responses')
@role_constraint('administrator')
def index():
    responses = ResponsesQuery(
        flask.request.args, flask.session.get('user_id')
    ).get_responses()

    return flask.render_template(f"{templates_context}/index.jinja",
                                 responses=responses)


@administrator_responses_blueprint.get(
    '/administrator/responses/<int:response_id>')
@role_constraint('administrator')
def show(response_id: int):
    response = db.session.get(Response, response_id)

    if response is None:
        flask.flash('No se encontró la respuesta a la que desea acceder.',
                    'error')

        return flask.redirect_to(
            flask.url_for('administrator_responses_controller.index'))

    return flask.render_template(f"{templates_context}/show.jinja",
                                 response=response)
