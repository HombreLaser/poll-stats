from flask_wtf.csrf import CSRFProtect
import tomllib
import re
import src.database as database
import src.controllers as app_controllers


csrf = CSRFProtect()


def init_app(app):
    # load_config(app)
    # database.init_db(app)
    app.config['SECRET_KEY'] = 'test'
    initialize_blueprints(app)
    csrf.init_app(app)


def initialize_blueprints(app):
    controller_regex = re.compile('_controller$')
    controllers = [definition for definition in dir(app_controllers)
                   if controller_regex.search(definition) is not None]
    register_blueprints(app)


def register_blueprints(app):
    from src.controllers.guest.sessions_controller import sessions_blueprint
    app.register_blueprint(sessions_blueprint)


def load_config(app):
    with open('config.toml', 'rb') as config_file:
        config = tomllib.load(config_file)
        app.config.update(
            SQLALCHEMY_DATABASE_URI = connection_string(config, app),
            SECRET_KEY = config['flask']['SECRET_KEY']
        )


def connection_string(config, app):
    connection = (f"mysql+pymysql://{config['database']['user']}:"
                  f"{config['database']['password']}@localhost/")

    if app.testing:
        return connection + 'test_poll_stats'
    else:
        return connection + 'poll_stats'