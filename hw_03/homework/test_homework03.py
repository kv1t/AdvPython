import re
from unittest.mock import patch

from homework03 import random_key


def test_random_key():
    test_keys = [f() for f in [random_key]*10]
    assert len(set(test_keys)) == len(test_keys), 'Keys should be different'
    for key in test_keys:
        assert len(key) > 4, 'Key should be at least 5 characters long'
        assert re.match(r'[\d\w]+', key),\
            'Key should consist of alphanumeric characters'


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_shorten_redirect(client):
    test_key = 'dummy'
    test_url = 'http://www.python.org/'

    with patch('homework03.random_key', lambda: test_key):
        response = client.post('/', {'url': test_url})
        assert response.status_code == 200
        assert test_key in response.content.decode()

        response = client.get('/' + test_key)
        assert response.status_code == 302
        assert response.url == test_url

        response = client.get('/{}/stats'.format(test_key))
        assert response.status_code == 200
        assert '1' in response.content.decode()


def test_is_not_valid_scheme(client):
    response = client.post('/', {'url': 'mailto:admin@itea.ua'})
    assert response.status_code == 200
    body = response.content.decode()
    assert all(map(body.__contains__, ('http', 'https', 'ftp')))


def test_redirect_nonexistent(client):
    response = client.get('/randomnonsense')
    assert response.status_code == 302
    assert response.url == '/'