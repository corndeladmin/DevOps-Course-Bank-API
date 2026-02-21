"""Unit tests for bank.py"""

import pytest

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

# --- add_funds() tests ---

def test_add_funds_creates_transaction(bank: Bank):
    bank.create_account('Alice')
    bank.add_funds('Alice', 1000)

    assert len(bank.transactions) == 1

def test_add_funds_transaction_has_correct_amount(bank: Bank):
    bank.create_account('Alice')
    bank.add_funds('Alice', 500)

    assert bank.transactions[0].amount == 500

def test_add_funds_raises_error_if_account_not_found(bank: Bank):
    with pytest.raises(ValueError):
        bank.add_funds('Nobody', 100)

def test_add_funds_raises_error_if_amount_is_negative(bank: Bank):
    bank.create_account('Alice')

    with pytest.raises(ValueError):
        bank.add_funds('Alice', -50)

def test_add_funds_raises_error_if_amount_is_zero(bank: Bank):
    bank.create_account('Alice')

    with pytest.raises(ValueError):
        bank.add_funds('Alice', 0)

