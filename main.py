from flask import Flask
import src.database.models as models
import tomllib
import initializer


app = Flask(__name__)
app.config.from_file('config.toml', load=tomllib.load, text=False)
initializer.init_app(app)


@app.shell_context_processor
def shell():
    return {
        "models": models,
        "db": db
    }