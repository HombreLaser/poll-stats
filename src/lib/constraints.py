from functools import wraps
from flask import session, redirect, url_for


def role_constraint(*roles):
    def constraint(function):
        @wraps(function)
        def decorated_view(*args, **kwargs):
            if session_present() and session.get('user_role') in roles:
                return function(*args, **kwargs)

            return redirect(url_for('sessions_controller.new'))

        return decorated_view

    return constraint


def redirect_if_logged_in(function):
    @wraps(function)
    def decorated_view(*args, **kwargs):
        if session_present():
            return redirect(url_for(f"{session.get('user_role')}_dashboards_controller.index"))

        return function(*args, **kwargs)

    return decorated_view


def session_present():
    return session.get('user_id') is not None and session.get('user_role') is not None
