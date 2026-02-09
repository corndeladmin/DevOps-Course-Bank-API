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
    # Use the client to make requests to the Flask app.
    # response = client.get('/example/route')
    # Or use client.post to make a POST request
    # https://flask.palletsprojects.com/en/1.1.x/testing/
    post_response = client.post("/accounts/IntegrationTest1")
    created_name = post_response.json["name"]

    assert post_response.status_code == 200
    assert created_name == "IntegrationTest1"

    get_response = client.get("/accounts/IntegrationTest1")
    assert get_response.status_code == 200
    assert get_response.json["name"] == "IntegrationTest1"

def test_add_money(client: FlaskClient):
    post_response = client.post("/accounts/IntegrationTest1")

    add_money_response = client.post("/money", data={'name': 'IntegrationTest1', 'amount': 100})    
    assert add_money_response.status_code == 200