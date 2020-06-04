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


def test_get_balance(client):
    account_name = 'balance_test'
    create = client.post(f'/accounts/{account_name}')
    before = client.get(f'/accounts/{account_name}')
    move = client.post('/money', json=dict(
        name=account_name,
        amount=50
    ),
    headers={'Content-Type': 'application/json'})
    after = client.get(f'/accounts/{account_name}')

    assert create.status_code == 200
    assert before.status_code == 200
    assert move.status_code == 200
    assert after.status_code == 200

    balance_before = json.loads(before.data)['balance']
    balance_after = json.loads(after.data)['balance']

    assert balance_before == 0
    assert balance_after == 50
