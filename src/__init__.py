from flask import Flask
from flask_wtf.csrf import CSRFProtect
import sqlalchemy
import tomllib
import re
import src.database as database
import src.database.models as models
import src.controllers as app_controllers


csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    load_config(app)
    database.init_db(app)
    initialize_blueprints(app)
    csrf.init_app(app)

    return app


def initialize_blueprints(app):
    controller_regex = re.compile('_controller$')
    controllers = [definition for definition in dir(app_controllers)
                   if controller_regex.search(definition) is not None]
    register_blueprints(controllers, app)


def register_blueprints(controllers: list, app):
    for controller in controllers:
        controller_name = controller.removesuffix('_controller')
        blueprint = getattr(getattr(app_controllers, controller),
                            f"{controller_name}_blueprint")
        app.register_blueprint(blueprint)


def load_config(app):
    with open('config.toml', 'rb') as config_file:
        config = tomllib.load(config_file)
        app.config.update(
            SQLALCHEMY_DATABASE_URI = connection_string(config, app),
            SECRET_KEY = config['flask']['SECRET_KEY'],
            APPLICATION_ROOT = config['flask']['APPLICATION_ROOT'],
            SESSION_COOKIE_PATH = '/'
        )


def connection_string(config, app):
    connection = (f"mysql+pymysql://{config['database']['user']}:"
                  f"{config['database']['password']}@localhost/")

    if app.testing:
        return connection + 'test_poll_stats'
    else:
        return connection + 'poll_stats'


app = create_app()


@app.shell_context_processor
def shell():
    return {
        "models": models,
        "db": database.db,
        "sa": sqlalchemy
    }