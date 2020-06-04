"""Unit tests for bank.py"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats

from bank_api.bank import Bank


@pytest.fixture
def bank() -> Bank:
    return Bank()

def test_create_account_raises_error_if_name_blank(bank: Bank):
    # This means: assert an exception is raised during the following block
    with pytest.raises(Exception):
        bank.create_account('')

def test_bank_creates_empty(bank: Bank):
    assert len(bank.accounts) == 0
    assert len(bank.transactions) == 0

def test_can_create_and_get_account(bank: Bank):
    bank.create_account('Test')
    account = bank.get_account('Test')

    assert len(bank.accounts) == 1
    assert account.name == 'Test'

def test_get_account_raises_error_if_no_account_matches(bank: Bank):
    bank.create_account('Name 1')

    # This means: assert an exception is raised during the following block
    with pytest.raises(ValueError):
        bank.get_account('Name 2')

@given(amount=integers())
def test_add_funds(amount):
    bank = Bank()
    bank.create_account('Test')
    bank.add_funds('Test', amount)
    transactions = bank.transactions

    assert len(transactions) == 1
    assert transactions.pop().amount == amount


def test_add_funds_no_account(bank):
    with pytest.raises(ValueError):
        bank.add_funds('no-account', 3)


def test_add_multiple_funds(bank):
    bank.create_account('Test')
    bank.add_funds('Test', 50)
    bank.add_funds('Test', 25)

    transactions = bank.transactions
    assert len(transactions) == 2
    assert {t.amount for t in transactions} == {25, 50}


@given(amount=floats())
def test_add_fractional_funds(amount):
    bank = Bank()
    bank.create_account('Test')
    with pytest.raises(TypeError):
        bank.add_funds('Test', amount)
