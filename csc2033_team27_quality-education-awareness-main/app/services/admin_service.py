"""Admin dashboard services."""

from app.repositories import log_repository, user_repository


def build_admin_dashboard_context():
    """Build the data required by the admin dashboard template."""
    logs = log_repository.list_logs()
    return {
        "users": user_repository.get_all_users(),
        "logs": logs,
        "contents": log_repository.load_logs(logs),
    }
