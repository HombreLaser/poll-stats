# Funciones globales para plantillas jinja
from flask import current_app, session
import sqlalchemy as sa
from src.lib.constraints import session_present
from src.database import db
from src.database.models import UserAccount
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


@current_app.template_global()
def current_user():
    if not session_present():
        return

    return db.session.execute(
        sa.select(UserAccount)
          .filter(UserAccount.id == session.get('user_id'))
          .filter(UserAccount.role == session.get('user_role'))
    ).scalar()