
def test_get_weather_data(client):
    res = client.get('/api/weather')
    # import ipdb
    # ipdb.set_trace()
    assert res.headers.get('Content-Type') == 'application/json'
    assert res.status_code == 200
    assert eval(res.data)['payload'] is not None


def test_get_weather_stats(client):
    res = client.get('/api/weather/stats/')
    # import ipdb
    # ipdb.set_trace()
    assert res.headers.get('Content-Type') == 'application/json'
    assert res.status_code == 200
    assert eval(res.data)['payload'] is not None


def test_index(client):
    res = client.get('/api/')
    assert res.status_code == 200
