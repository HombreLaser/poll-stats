import pytest
import secrets
import multiprocessing
from flask import Flask
from src.database import clear_data
from src.database import db as database
import src


@pytest.fixture(scope='session')
def app():
    src.app.config['TESTING'] = True
    # Usaremos otro secret key.
    src.app.config['SECRET_KEY'] = secrets.token_hex(32)

    with src.app.app_context():
        yield src.app

    clear_data(src.app)


@pytest.fixture(scope='session')
def server(app):
    def worker(app, host, port):
            app.run(host=host, port=port, use_reloader=False, threaded=True)

    process = multiprocessing.Process(
        target=worker, args=(app, 'localhost', '8888')
    )
    process.daemon = True
    process.start()

    yield process

    process.terminate()


@pytest.fixture
def db(app):
    return database
