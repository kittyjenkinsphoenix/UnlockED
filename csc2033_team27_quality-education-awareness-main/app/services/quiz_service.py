"""Quiz scoring and quiz dashboard services."""

from app.repositories import quiz_repository

QUIZ_ANSWER_KEY = {
    "q1": "86.3%",
    "q2": "Denmark",
    "q3": "South Korea",
    "q4": "272 million",
    "q5": "754 million",
    "q6": "74%",
}


def calculate_quiz_score(form):
    """Return the number of correct answers on the submitted quiz form."""
    return sum(1 for field_name, answer in QUIZ_ANSWER_KEY.items() if getattr(form, field_name).data == answer)


def score_quiz_submission(user, form):
    """Record a quiz submission and update the user's score fields."""
    score = calculate_quiz_score(form)

    if user.first_score is None:
        user.first_score = score

    user.quiz_score = score
    user.quiz_count = (user.quiz_count or 0) + 1

    new_high_score = False
    if user.high_score is None or score > user.high_score:
        user.high_score = score
        new_high_score = True

    quiz_repository.save_quiz_result(user.id, score, total_questions=len(QUIZ_ANSWER_KEY))
    quiz_repository.save_user(user)
    return new_high_score


def build_quiz_dashboard_context(user):
    """Build the context for the quiz summary page."""
    return {
        "score": user.quiz_score,
        "high_score": user.high_score,
        "first_score": user.first_score,
    }
