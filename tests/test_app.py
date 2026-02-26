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
    assert get_response.get_json() == {"name": "Alice", "balance": 0}


def test_get_account_returns_404_if_not_found(client: FlaskClient):
    response = client.get('/accounts/Nobody')

    assert response.status_code == 404


def test_get_account_includes_balance(client: FlaskClient):
    client.post('/accounts/Alice')
    client.post('/money', json={'name': 'Alice', 'amount': 1000})

    response = client.get('/accounts/Alice')

    assert response.status_code == 200
    assert response.get_json()['balance'] == 1000
