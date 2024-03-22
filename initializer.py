import tomllib
import src.database as database


with open('config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

connection_string = (f"mysql+pymysql://{config['database']['user']}:"
                     f"{config['database']['password']}@localhost/poll_stats")

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    database.init_db(app)