"""Admin routes."""

from flask import render_template
from flask_login import login_required

from app.services.admin_service import build_admin_dashboard_context
from app.utils.decorators import role_required

from . import main


@main.route("/admin")
@login_required
@role_required("admin")
def admin_dashboard():
    """Render the admin dashboard with user and log summaries."""
    context = build_admin_dashboard_context()
    return render_template("admin.html", **context)
