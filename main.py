from flask import Flask
from src.database.models import UserAccount
import tomllib
import initializer


app = Flask(__name__)
app.config.from_file('config.toml', load=tomllib.load, text=False)
initializer.init_app(app)