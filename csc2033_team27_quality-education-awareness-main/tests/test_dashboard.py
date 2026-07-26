from app import db
from app.models import User

# Tests for the user dashboard page when the user is logged in. It creates a test user, logs them in, and checks if the dashboard page is accessible.


def test_user_dashboard_logged_in(client, app):
    with app.app_context():
        user = User(username="test@email.com", name="Test", role="user")  # User Login Credentials
        user.set_password("test123")

        db.session.add(user)
        db.session.commit()

        user_id = user.id

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)
        sess["_fresh"] = True

    response = client.get("/user-dashboard")
    assert response.status_code == 200


# Tests if a user with a "user" role can access the admin dashboard.
def test_user_cant_access_admin_dashboard(client, app):
    with app.app_context():
        user = User(username="test@email.com", name="Test", role="user")
        user.set_password("test123")

        db.session.add(user)
        db.session.commit()

        user_id = user.id

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)
        sess["_fresh"] = True

    response = client.get("/admin")
    assert response.status_code == 403


# Tests that unauthenticated users are redirected when accessing user dashboard
def test_user_dashboard_requires_login(client):
    response = client.get("/user-dashboard")
    assert response.status_code == 302


# Tests that unauthenticated users are redirected when accessing admin dashboard
def test_admin_dashboard_requires_login(client):
    response = client.get("/admin")
    assert response.status_code == 302
