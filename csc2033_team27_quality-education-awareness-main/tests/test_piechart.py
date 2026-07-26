# Tests for the pie chart on the home page. It sends a GET request to the home page and checks if the response contains the expected data for the pie chart, specifically the labels "High-income" and "Low-income".


def test_chart_data_present(client):
    response = client.get("/")
    assert b"High-income" in response.data
    assert b"Low-income" in response.data
