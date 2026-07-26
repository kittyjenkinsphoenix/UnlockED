"""Authentication and account services."""

from flask import current_app, render_template
from flask_mail import Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app import mail
from app.models import User
from app.repositories import user_repository
from app.utils.security import is_blacklisted_password

PASSWORD_RESET_SALT = "password-reset"
PASSWORD_RESET_MAX_AGE = 3600


def register_user(username, name, password, bio):
    """Create a user account if the password policy and uniqueness checks pass."""
    if is_blacklisted_password(password):
        return {"ok": False, "category": "danger", "message": "That password is too common, please choose another one"}

    if user_repository.get_user_by_username(username):
        return {"ok": False, "category": "warning", "message": "Email already registered"}

    user = User(username=username, name=name, role="user")
    user.set_password(password)
    user.set_bio(bio)
    user_repository.save_user(user)
    return {"ok": True, "category": "success", "message": "Registration success, please login"}


def authenticate_user(username, password):
    """Return the matching user when the supplied credentials are valid."""
    user = user_repository.get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None


def change_password(user, current_password, new_password):
    """Update the user's password when the current password is correct."""
    if not user.check_password(current_password):
        return {"ok": False, "category": "danger", "message": "Incorrect current password"}

    if is_blacklisted_password(new_password):
        return {"ok": False, "category": "danger", "message": "Password in blacklist, choose a secure one"}

    user.set_password(new_password)
    user_repository.save_user(user)
    return {"ok": True, "category": "success", "message": "Your password has been updated"}


def _get_reset_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def generate_password_reset_token(email):
    """Create a signed password reset token for the supplied email address."""
    return _get_reset_serializer().dumps(email, salt=PASSWORD_RESET_SALT)


def verify_password_reset_token(token, max_age=PASSWORD_RESET_MAX_AGE):
    """Return the email stored in the token if it is still valid."""
    serializer = _get_reset_serializer()
    try:
        return serializer.loads(token, salt=PASSWORD_RESET_SALT, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


def request_password_reset(email):
    """Generate a reset token and send a password reset email when possible."""
    user = user_repository.get_user_by_username(email)
    message_text = "If an account exists for that email, a reset link has been sent."

    if not user:
        return {"ok": True, "category": "info", "message": message_text, "token": None}

    token = generate_password_reset_token(user.username)
    message = Message(subject="Reset your password", recipients=[user.username])
    message.body = (
        "To reset your password, open the reset link in the HTML version of this email. "
        "If you did not request a password reset, you can ignore this message."
    )
    message.html = render_template("email/reset_password_email.html", user=user, token=token)

    token_for_display = token if current_app.debug or current_app.testing else None
    try:
        mail.send(message)
    except Exception as exc:  # pragma: no cover - defensive fallback for local/dev mail failures
        current_app.logger.warning("Password reset email could not be sent: %s", exc)

    return {"ok": True, "category": "info", "message": message_text, "token": token_for_display}


def reset_password_from_token(token, new_password):
    """Update the stored password if the reset token is valid."""
    email = verify_password_reset_token(token)
    if not email:
        return {"ok": False, "category": "danger", "message": "The password reset link is invalid or has expired."}

    user = user_repository.get_user_by_username(email)
    if not user:
        return {"ok": False, "category": "danger", "message": "The password reset link is invalid or has expired."}

    if is_blacklisted_password(new_password):
        return {"ok": False, "category": "danger", "message": "That password is too common. Choose a stronger password."}

    user.set_password(new_password)
    user_repository.save_user(user)
    return {"ok": True, "category": "success", "message": "Your password has been reset successfully."}
