"""Integration tests for app.py"""
from typing import Type
from flask.testing import FlaskClient
from flask.wrappers import Response
import pytest

from bank_api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


def test_account_creation(client: FlaskClient):
    post_response = client.post('/accounts/Alice')

    assert post_response.status_code == 200
    assert post_response.get_json() == {"name": "Alice"}

    get_response = client.get('/accounts/Alice')

    assert get_response.status_code == 200
    assert get_response.get_json() == {"name": "Alice"}


def test_get_account_returns_404_if_not_found(client: FlaskClient):
    response = client.get('/accounts/Nobody')

    assert response.status_code == 404
