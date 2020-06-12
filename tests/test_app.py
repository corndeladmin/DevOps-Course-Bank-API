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
    ))
    after = client.get(f'/accounts/{account_name}')

    assert create.status_code == 200
    assert before.status_code == 200
    assert move.status_code == 200
    assert after.status_code == 200

    balance_before = json.loads(before.data)['balance']
    balance_after = json.loads(after.data)['balance']

    assert balance_before == 0
    assert balance_after == 50


def test_move_funds(client):
    client.post('/accounts/SendsMoney')
    client.post('/accounts/ReceivesMoney')
    client.post('/money', json={
        'name': 'SendsMoney',
        'amount': 50
    })
    move = client.post('/money/move', json=dict(
        name_from='SendsMoney',
        name_to='ReceivesMoney',
        amount=20
    ))

    assert move.status_code == 200

    sender_response = client.get('/accounts/SendsMoney')
    receiver_response = client.get('/accounts/ReceivesMoney')

    sender_balance = json.loads(sender_response.data)['balance']
    receiver_balance = json.loads(receiver_response.data)['balance']

    assert sender_balance == 30
    assert receiver_balance == 20


def test_overdrawn(client):
    client.post('/accounts/GoingOverdrawn')
    response = client.post('/money', json=dict(
        name='GoingOverdrawn',
        amount=-10
    ))

    assert response.status_code == 403


def test_overdrawn_movement(client):
    client.post('/accounts/OverdrawnSender')
    client.post('/accounts/ReceivesMoney')
    response = client.post('/money/move', json=dict(
        name_from='OverdrawnSender',
        name_to='ReceivesMoney',
        amount=20
    ))

    assert response.status_code == 403
