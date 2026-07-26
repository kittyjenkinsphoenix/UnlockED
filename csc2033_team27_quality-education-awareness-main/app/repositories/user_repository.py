"""User repository helpers."""

from app import db
from app.models import User


def get_user_by_username(username):
    """Return the user matching the supplied username."""
    return User.query.filter_by(username=username).first()


def get_user_by_id(user_id):
    """Return the user with the given identifier."""
    return User.query.get(int(user_id))


def get_all_users():
    """Return all users ordered by identifier."""
    return User.query.order_by(User.id.asc()).all()


def get_users_with_scores():
    """Return users who have at least one recorded quiz score."""
    return User.query.filter(User.quiz_score.isnot(None)).all()


def save_user(user):
    """Persist a user instance to the database."""
    db.session.add(user)
    db.session.commit()
    return user
