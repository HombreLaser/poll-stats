from flask import Flask
from src.database import db
import src.database.models as models
import tomllib
import src.initializer as initializer


app = Flask(__name__)
app.config.from_prefixed_env()
initializer.init_app(app)


@app.shell_context_processor
def shell():
    return {
        "models": models,
        "db": db
    }