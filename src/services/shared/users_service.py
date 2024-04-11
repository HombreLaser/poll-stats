from src.database.models import UserAccount
from src.forms import RegistrationForm, UserAccountForm
from src.database import db
import secrets


def create_user(form: UserAccountForm):
    user = UserAccount(email=form.email.data, first_name=form.first_name.data,
                       last_name=form.last_name.data)
    user.invite_code = secrets.token_hex(16)
    db.session.add(user)
    db.session.commit()


def activate_user(user: UserAccount, form: RegistrationForm):
    user.activated = True
    user.password = form.password.data
    db.session.commit()