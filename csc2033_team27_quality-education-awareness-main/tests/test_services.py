"""Service-layer and edge-case tests."""

from types import SimpleNamespace

from app import db
from app.models import User
from app.services.dashboard_service import dashboard_redirect_endpoint
from app.services.quiz_service import calculate_quiz_score


def extract_csrf(html):
    """Extract a CSRF token from rendered form HTML."""
    import re

    return re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html).group(1)


def test_blacklisted_password_is_rejected(client):
    """Registration should reject passwords on the blacklist."""
    page = client.get("/register")
    csrf_token = extract_csrf(page.data.decode())

    response = client.post(
        "/register",
        data={
            "csrf_token": csrf_token,
            "username": "blocked@email.com",
            "name": "Blocked",
            "password": "Password123$",
            "confirm_password": "Password123$",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"too common" in response.data


def test_dashboard_redirect_endpoint_maps_roles():
    """Role names should map to the expected dashboard endpoints."""
    assert dashboard_redirect_endpoint("user") == "main.user_dashboard"
    assert dashboard_redirect_endpoint("moderator") == "main.moderator_dashboard"
    assert dashboard_redirect_endpoint("admin") == "main.admin_dashboard"


def test_quiz_service_scores_answers():
    """Quiz scoring should count only the correct answers."""
    form = SimpleNamespace(
        q1=SimpleNamespace(data="86.3%"),
        q2=SimpleNamespace(data="Denmark"),
        q3=SimpleNamespace(data="South Korea"),
        q4=SimpleNamespace(data="272 million"),
        q5=SimpleNamespace(data="754 million"),
        q6=SimpleNamespace(data="74%"),
    )
    assert calculate_quiz_score(form) == 6

    partial_form = SimpleNamespace(
        q1=SimpleNamespace(data="67.3%"),
        q2=SimpleNamespace(data="Denmark"),
        q3=SimpleNamespace(data="Japan"),
        q4=SimpleNamespace(data="272 million"),
        q5=SimpleNamespace(data="543 million"),
        q6=SimpleNamespace(data="65%"),
    )
    assert calculate_quiz_score(partial_form) == 2


def test_calendar_endpoint_falls_back_without_configuration(client, app):
    """The calendar API should return an empty list when config is missing."""
    app.config["GOOGLE_API_KEY"] = None
    app.config["GOOGLE_CALENDAR_ID"] = None

    response = client.get("/api/calendar")

    assert response.status_code == 200
    assert response.get_json() == []


def test_admin_can_access_user_dashboard(client, app):
    """Admins should be allowed through role-protected user routes."""
    with app.app_context():
        user = User(username="admin@test.com", name="Admin", role="admin")
        user.set_password("AdminPass!23")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with client.session_transaction() as session_data:
        session_data["_user_id"] = str(user_id)
        session_data["_fresh"] = True

    response = client.get("/user-dashboard")
    assert response.status_code == 200
