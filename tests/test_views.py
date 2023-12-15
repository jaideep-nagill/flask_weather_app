
def test_get_weather_data(client):
    res = client.get('/api/weather')

    assert res.status_code == 200


def test_get_weather_stats(client):
    res = client.get('/api/weather')

    assert res.status_code == 200
