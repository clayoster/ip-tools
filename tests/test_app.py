import re

# Confirm that an ipv4 address is in the response for 'ip'
def test_ip_route(app, client):
    res = client.get(
        '/',
        headers={'Host': 'ip.example.com'})
    assert re.search('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', str(res.data))
    assert res.status_code == 200

# Confirm that 'localhost' is in the response for 'ptr'
def test_ptr_route(app, client):
    res = client.get(
        '/',
        headers={'Host': 'ptr.example.com'})
    assert b'localhost' in res.data
    assert res.status_code == 200

# Confirm that a 10 digit number is in the response for 'epoch'
def test_epoch_route(app, client):
    res = client.get(
        '/',
        headers={'Host': 'epoch.example.com'})
    assert re.search('[0-9]{10}', str(res.data))
    assert res.status_code == 200

# Confirm that '"Host": "headers.example.com"' is in the response for 'ptr'
# and that the response is JSON
def test_headers_route(app, client):
    res = client.get(
        '/',
        headers={'Host': 'headers.example.com'})
    assert b'"Host": "headers.example.com"' in res.data
    assert res.is_json, "Response was not JSON"
    assert res.status_code == 200

# Confirm proxy-headers route works when enabled. This will have an empty response in tests
def test_proxy_headers_route_enabled(app, client):
    res = client.get(
        '/',
        headers={'Host': 'proxy-headers.example.com'})
    import os
    assert os.getenv("ENABLE_PROXY_HEADERS") == "true"
    assert b'' in res.data
    assert res.status_code == 204

# Confirm that heathcheck is successful
def test_robots_route(app, client):
    res = client.get('/robots.txt')
    assert b'User-agent: *' in res.data
    assert b'Disallow: /' in res.data
    assert res.status_code == 200

# Confirm that heathcheck is successful
def test_healthcheck(app, client):
    res = client.get('/health')
    assert b'healthy' in res.data
    assert res.status_code == 200
