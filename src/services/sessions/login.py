import sqlalchemy as sql
from flask import session
from src.database import db
from src.database.models import UserAccount
from src.forms import LoginForm


def set_session(user):
    session['user_id'] = user.id
    session['user_role'] = user.role


class Login:
    def __call__(self, form: LoginForm):
        self.form = form
        user = self._find_user()

        if user is not None:
            if user.verify_password(self.form.data['password']):
                set_session(user)

                return self.form

        self.form.form_errors.append('Contraseña o correo inválidos.')

        return self.form 

    def _sql_statement(self):
        return sql.select(UserAccount).filter_by(email=self.form.data['email'])

    def _find_user(self):
        return db.session.execute(self._sql_statement()).scalar()