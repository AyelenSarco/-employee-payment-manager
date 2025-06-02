from functools import wraps
from flask import abort, redirect, session, url_for
from src.core.service.service_user import search_user_by_email,get_permissions


def is_authenticated(session):
    return session.get("email") is not None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if (not is_authenticated(session)):
            return redirect(url_for('auth.login'))
        return f(*args,**kwargs)
    return wrapper

def have_permission(session, permission):
    email = session.get("email")
    user = search_user_by_email(email)
    if user:
        if user.sys_admin:
            return True
        permissions = get_permissions(user.id)

        return permission in permissions
    return None

def check(permission):
    def permission_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if (not have_permission(session, permission)):
                return abort(403)
            return f(*args, **kwargs)
        return wrapper
    return permission_decorator
    