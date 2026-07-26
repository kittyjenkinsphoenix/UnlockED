import pytest
from itsdangerous import URLSafeSerializer


# Disable CSRF for take action tests
@pytest.fixture
def take_action_app(app):
    app.config["WTF_CSRF_ENABLED"] = False
    return app


# Tests loading the page
def test_take_action_loads(client):
    response = client.get("/take-action")
    assert response.status_code == 200


# Tests signing a new email up
def test_take_action_signup(client, take_action_app):
    response = client.post("/take-action", data={"email": "test@email.com", "check": "y"}, follow_redirects=True)
    assert response.status_code == 200


# Tests signing up existing email
def test_take_action_duplicate(client, take_action_app):
    client.post("/take-action", data={"email": "test@email.com", "check": "y"}, follow_redirects=True)

    response = client.post("/take-action", data={"email": "test@email.com", "check": "y"}, follow_redirects=True)

    assert b"already signed up" in response.data


# Tests unsubscribing with a valid token
def test_unsubscribe_valid(client, app):
    s = URLSafeSerializer(app.config["SECRET_KEY"], salt="unsubscribe")
    token = s.dumps("test@example.com")
    response = client.get(f"/unsubscribe/{token}", follow_redirects=True)
    assert response.status_code == 200


# Test unsubscribing with an invalid token
def test_unsubscribe_invalid(client):
    response = client.get("/unsubscribe/token", follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid or expired token" in response.data


# Tests if calendar api returns json
def test_calendar_api_json(client):
    response = client.get("/api/calendar")
    assert response.status_code == 200
    assert response.is_json


# Tests if calendar api json is in correct format
def test_calendar_api_structure(client):
    response = client.get("/api/calendar")
    calendar = response.get_json()
    assert isinstance(calendar, list)
    if calendar:
        assert "title" in calendar[0]
        assert "start" in calendar[0]
        assert "end" in calendar[0]
