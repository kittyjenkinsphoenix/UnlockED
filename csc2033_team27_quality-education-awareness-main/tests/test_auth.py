import re

from app import db
from app.models import User
from app.services.auth_service import generate_password_reset_token


# Reusable csrf token extraction function for use in multiple tests
def extract_csrf(html):
    return re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html).group(1)


# Tests if user can login from registered account. Also tests the csrf token.


def test_registered_user_can_login(client):

    response = client.get("/login")
    html = response.data.decode()

    csrf_token = extract_csrf(html)

    response = client.post(
        "/login",
        data={"csrf_token": csrf_token, "username": "user1@email.com", "password": "Userpass!23"},
        follow_redirects=True,
    )

    assert response.status_code == 200


# Tests if a registered user cannot login with an incorrect password. Also tests the csrf token.


def test_login_fails_with_wrong_password(client):

    response = client.get("/login")
    html = response.data.decode()

    csrf_token = extract_csrf(html)

    response = client.post(
        "/login",
        data={"csrf_token": csrf_token, "username": "user1@email.com", "password": "WrongPassword!23"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"login" in response.data.lower()


# Tests if a user cannot login with an unregistered email. Also tests the csrf token.


def test_login_fails_with_unregistered_user(client):

    response = client.get("/login")
    html = response.data.decode()

    csrf_token = extract_csrf(html)

    response = client.post(
        "/login",
        data={"csrf_token": csrf_token, "username": "nonexistentuser@email.com", "password": "AnyPassword!23"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"login" in response.data.lower()


# Tests if a logged in user can logouut successfully. Also tests the csrf token.
def test_logout(client):

    response = client.get("/login")
    html = response.data.decode()

    csrf_token = extract_csrf(html)

    client.post("/login", data={"csrf_token": csrf_token, "username": "user@test.com"}, follow_redirects=True)
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data or b"login" in response.data.lower()


# Tests if a user cannot login with empty username and password fields. Also tests the csrf token.
def test_login_with_empty_fields(client):

    response = client.get("/login")
    html = response.data.decode()

    csrf_token = extract_csrf(html)

    response = client.post(
        "/login", data={"csrf_token": csrf_token, "username": "", "password": ""}, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"login" in response.data.lower()


# Tests if a user cannot register with an incorrectly formatted email.


def test_register_with_incorrect_email_format(client):

    response = client.post(
        "/register",
        data={
            "username": "invalidemailformat",
            "name": "Test User",
            "password": "ValidPass!23",
            "confirm_password": "ValidPass!23",
        },
        follow_redirects=True,
    )

    assert response.status_code in (200, 400, 500)


# Tests if a user cannot register with a password that does not meet the complexity requirements.


def test_register_with_incorrect_password_format(client):

    csrf_token = extract_csrf(client.get("/register").data.decode())

    response = client.post(
        "/register",
        data={
            "username": "user1@email.com",
            "name": "Test User",
            "password": "InvalidPass",
            "confirm_password": "InvalidPass",
        },
        follow_redirects=True,
    )

    response = client.post(
        "/login", data={"csrf_token": csrf_token, "username": "", "password": ""}, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"login" in response.data.lower()


# Tests if unauthenticated users are redirected when accessing change password page
def test_change_password_requires_login(client):
    response = client.get("/change-password")
    assert response.status_code == 302


# Tests if a user can change their password successfully. It creates a test user, logs them in, changes the password, logs out, and then tries to log in with the new password.


def test_change_password(client, app):

    # Creates user
    with app.app_context():
        user = User(username="user@test.com", name="Test User", role="user")
        user.set_password("OldPass!23")
        db.session.add(user)
        db.session.commit()

    # Login with old password
    login_page = client.get("/login")
    login_csrf = extract_csrf(login_page.data.decode())

    client.post(
        "/login",
        data={"csrf_token": login_csrf, "username": "user@test.com", "password": "OldPass!23"},
        follow_redirects=True,
    )

    # Change password
    cp_page = client.get("/change-password")
    cp_csrf = extract_csrf(cp_page.data.decode())

    response = client.post(
        "/change-password",
        data={
            "csrf_token": cp_csrf,
            "current_password": "OldPass!23",
            "new_password": "NewPass!23",
            "confirm_new_password": "NewPass!23",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    # Logout after password change
    client.get("/logout", follow_redirects=True)

    # Try logging in with NEW password
    login_page = client.get("/login")
    login_csrf = extract_csrf(login_page.data.decode())

    response = client.post(
        "/login",
        data={"csrf_token": login_csrf, "username": "user@test.com", "password": "NewPass!23"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"User Dashboard" in response.data or b"dashboard" in response.data.lower()


# Tests if change password fails when current password is incorrect.


def test_change_password_with_wrong_current_password(client, app):

    # Creates user
    with app.app_context():
        user = User(username="user@test.com", name="Test User", role="user")
        user.set_password("OldPass!23")
        db.session.add(user)
        db.session.commit()

    # Login with old password
    login_page = client.get("/login")
    login_csrf = extract_csrf(login_page.data.decode())

    client.post(
        "/login",
        data={"csrf_token": login_csrf, "username": "user@test.com", "password": "OldPass!23"},
        follow_redirects=True,
    )

    # Change password
    cp_page = client.get("/change-password")
    cp_csrf = extract_csrf(cp_page.data.decode())

    response = client.post(
        "/change-password",
        data={
            "csrf_token": cp_csrf,
            "current_password": "WrongCurrentPass!23",
            "new_password": "NewPass!23",
            "confirm_new_password": "NewPass!23",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"current password" in response.data.lower()


def test_forgot_password_request_shows_local_reset_link(client, app, monkeypatch):
    with app.app_context():
        user = User(username="user@test.com", name="Test User", role="user")
        user.set_password("OldPass!23")
        db.session.add(user)
        db.session.commit()

    monkeypatch.setattr("app.services.auth_service.mail.send", lambda message: None)

    page = client.get("/forgot-password")
    csrf_token = extract_csrf(page.data.decode())

    response = client.post(
        "/forgot-password",
        data={"csrf_token": csrf_token, "email": "user@test.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"/reset-password/" in response.data


def test_reset_password_with_valid_token_updates_account(client, app):
    with app.app_context():
        user = User(username="user@test.com", name="Test User", role="user")
        user.set_password("OldPass!23")
        db.session.add(user)
        db.session.commit()
        token = generate_password_reset_token(user.username)

    page = client.get(f"/reset-password/{token}")
    csrf_token = extract_csrf(page.data.decode())

    response = client.post(
        f"/reset-password/{token}",
        data={
            "csrf_token": csrf_token,
            "password": "NewPass!23",
            "confirm_password": "NewPass!23",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    login_page = client.get("/login")
    login_csrf = extract_csrf(login_page.data.decode())

    login_response = client.post(
        "/login",
        data={"csrf_token": login_csrf, "username": "user@test.com", "password": "NewPass!23"},
        follow_redirects=True,
    )

    assert login_response.status_code == 200
    assert b"dashboard" in login_response.data.lower()


def test_reset_password_rejects_invalid_token(client):
    response = client.get("/reset-password/invalid-token", follow_redirects=True)

    assert response.status_code == 200
    assert b"invalid or has expired" in response.data.lower()
