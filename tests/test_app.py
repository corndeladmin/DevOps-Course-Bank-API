"""Integration tests for app.py"""
from typing import Type
from flask.testing import FlaskClient
from flask.wrappers import Response
import json

import pytest

from bank_api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


def test_create_account(client: FlaskClient):
    """I should be able to create, then query an account"""
    response_creation = client.post('/accounts/test')
    response_query = client.get('/accounts/test')

    assert response_creation.status_code == 200
    assert response_query.status_code == 200

    data = json.loads(response_query.data)
    assert data['name'] == 'test'


def test_get_invalid_account_fails_with_404(client: FlaskClient):
    """Querying a non-existant account returns 404 (Not Found)"""
    response_query = client.get('/accounts/nothere')
    assert response_query.status_code == 404
