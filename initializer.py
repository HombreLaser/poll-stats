import tomllib
import re
import src.database as database
import src.controllers as app_controllers


with open('config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

connection_string = (f"mysql+pymysql://{config['database']['user']}:"
                     f"{config['database']['password']}@localhost/poll_stats")


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    database.init_db(app)
    initialize_blueprints(app)


def initialize_blueprints(app):
    controller_regex = re.compile('_controller$')
    controllers = [definition for definition in dir(app_controllers)
                   if controller_regex.search(definition) is not None]
    register_blueprints(controllers, app)


def register_blueprints(controllers: list, app):
    for controller in controllers:
        controller_name = controller.split('_')[0]
        blueprint = getattr(getattr(app_controllers, controller),
                            f"{controller_name}_blueprint")
        app.register_blueprint(blueprint)