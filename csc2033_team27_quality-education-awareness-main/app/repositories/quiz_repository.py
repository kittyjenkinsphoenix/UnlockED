"""Quiz repository helpers."""

from app import db
from app.models import QuizResult


def save_quiz_result(user_id, score, total_questions=6):
    """Persist a quiz result row to the database."""
    result = QuizResult(user_id=user_id, score=score, total_questions=total_questions)
    db.session.add(result)
    db.session.commit()
    return result


def save_user(user):
    """Persist a user after quiz-related score updates."""
    db.session.add(user)
    db.session.commit()
    return user


def get_recent_results(user_id, limit=5):
    """Return the most recent quiz attempts for a user."""
    return QuizResult.query.filter_by(user_id=user_id).order_by(QuizResult.created_at.desc()).limit(limit).all()
