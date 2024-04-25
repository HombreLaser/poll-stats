# Funciones globales para plantillas jinja
from flask import current_app
import secrets


@current_app.template_global()
def random_hex(bytes=4):
    return secrets.token_hex(bytes)


@current_app.template_global()
def field_class(field_type, form):
    if form.id.data:
        return f"{field_type}_{form.id.data}"
    else:
        return field_type

@current_app.template_global()
def status(form):
     match form.status:
        case 'review':
            return 'En reseña'
        case 'open':
            return 'Recibiendo respuestas'
        case 'closed':
            return 'Cerrado'