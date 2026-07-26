def login(client):
    return client.post("/login", data={"username": "user1@email.com", "password": "Userpass!23"}, follow_redirects=True)


def test_quiz_requires_login(client):
    response = client.get("/quiz")
    assert response.status_code == 302


def test_quiz_access_logged_in(client):
    login(client)
    response = client.get("/quiz", follow_redirects=True)
    assert response.status_code == 200
