"""View decorators for authentication and authorisation."""

from functools import wraps

from flask import abort, current_app, redirect, request, url_for
from flask_login import current_user


def role_required(required_role):
    """Restrict a view to a specific role, allowing admins through."""

    def decorator(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("main.login"))
            if current_user.role != required_role and current_user.role != "admin":
                current_app.logger.warning(
                    "Unauthorized access attempt by %s to %s",
                    current_user.username,
                    request.path,
                )
                abort(403)
            return view_function(*args, **kwargs)

        return decorated_function

    return decorator
