"""Dashboard routes."""

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.services.dashboard_service import build_user_dashboard_context, dashboard_redirect_endpoint
from app.utils.decorators import role_required

from . import main


@main.route("/dashboard")
@login_required
def dashboard():
    """Send the current user to the dashboard that matches their role."""
    return redirect(url_for(dashboard_redirect_endpoint(current_user.role)))


@main.route("/user-dashboard")
@login_required
@role_required("user")
def user_dashboard():
    """Render the user dashboard with quiz performance data."""
    context = build_user_dashboard_context(current_user)
    return render_template("user_dashboard.html", **context)


@main.route("/moderator")
@login_required
@role_required("moderator")
def moderator_dashboard():
    """Render the moderator dashboard placeholder page."""
    return render_template("moderator.html")
