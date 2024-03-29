import pytest
import secrets
from flask import Flask
from src.database import clear_data
import src.initializer as initializer


@pytest.fixture(scope='session')
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    initializer.init_app(app)
    # Usaremos otro secret key.
    app.config['SECRET_KEY'] = secrets.token_hex(32)

    with app.app_context():
        yield app

    clear_data(app)


@pytest.fixture()
def db(app):
    from src.database import db

    return db
