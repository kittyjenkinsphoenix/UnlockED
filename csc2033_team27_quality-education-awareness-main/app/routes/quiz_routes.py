"""Quiz routes."""

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.forms import QuizForm
from app.services.quiz_service import build_quiz_dashboard_context, score_quiz_submission

from . import main


@main.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    """Show the quiz form and record submitted quiz attempts."""
    form = QuizForm()
    if form.validate_on_submit():
        score_quiz_submission(current_user, form)
        return redirect(url_for("main.user_dashboard"))
    return render_template("quiz.html", form=form)


@main.route("/quiz_dash", methods=["GET"])
@login_required
def quiz_dash():
    """Display the user's latest quiz summary."""
    context = build_quiz_dashboard_context(current_user)
    return render_template("quiz_dash.html", **context)
