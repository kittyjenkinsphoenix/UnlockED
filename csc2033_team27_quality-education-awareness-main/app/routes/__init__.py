"""Route package for the UnlockED Flask application."""

from flask import Blueprint

main = Blueprint("main", __name__)


from . import admin_routes, auth_routes, content_routes, dashboard_routes, quiz_routes  # noqa: E402,F401
