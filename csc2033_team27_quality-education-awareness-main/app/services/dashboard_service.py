"""Dashboard calculation services."""

from app.repositories import quiz_repository, user_repository


def dashboard_redirect_endpoint(role):
    """Return the dashboard endpoint name for a role."""
    if role == "admin":
        return "main.admin_dashboard"
    if role == "moderator":
        return "main.moderator_dashboard"
    return "main.user_dashboard"


def _to_percentage(score, total_questions):
    if score is None:
        return 0
    return round((score / total_questions) * 100, 1)


def build_user_dashboard_context(user):
    """Build the data required by the user dashboard template."""
    total_questions = 6
    users_with_scores = user_repository.get_users_with_scores()
    if users_with_scores:
        avg_raw_score = sum(item.quiz_score for item in users_with_scores) / len(users_with_scores)
        avg_score = round((avg_raw_score / total_questions) * 100)
    else:
        avg_score = 0

    quiz_count = user.quiz_count or 0
    recommendation = (
        "Take another quiz to improve your score and visit the Take Action page to get involved."
        if quiz_count >= 1
        else "Take the quiz to see how much you know about global education and get personalised recommendations."
    )

    return {
        "bio": user.get_bio(),
        "user_score": _to_percentage(user.quiz_score, total_questions),
        "high_score": _to_percentage(user.high_score, total_questions),
        "avg_score": avg_score,
        "quiz_count": quiz_count,
        "new_high_score": False,
        "recent_results": quiz_repository.get_recent_results(user.id),
        "recommendation": recommendation,
    }
