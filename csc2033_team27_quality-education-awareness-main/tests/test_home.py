# Tests for the home page of the application. It sends a GET request to the home page and checks if the response status code is 200 (OK).


def test_home_page(client):
    response = client.get("/")
    print(response.status_code)
    print(response.data)
    assert response.status_code == 200
