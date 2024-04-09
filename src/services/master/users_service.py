from src.database.models import UserAccount
import secrets


def create_user(form):
    user = UserAccount(email=form.email.data, first_name=form.first_name.data,
                       last_name=form.last_name.data)
    user.invite_code = secrets.token_hex(16)

    return user
                    