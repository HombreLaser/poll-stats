from flask import current_app
import secrets


@current_app.template_global()
def random_hex(bytes=4):
    secrets.token_hex(bytes)
# Funciones globales para plantillas jinja