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

# TODO: Add unit tests for bank.add_funds()

def test_add_funds_successful(bank: Bank):
    bank.create_account("TestName 1")

    bank.add_funds("TestName 1", 100)
    
    assert len(bank.transactions) == 1

def test_add_funds_raises_error_if_no_account_matches(bank: Bank):
    bank.create_account("TestName 1")

    with pytest.raises(ValueError):
        bank.add_funds("TestName 2", 100)

def test_add_funds_string_amount_does_not_add_transaction(bank: Bank):
    bank.create_account("TestName 1")

    bank.add_funds("TestName 1", "100")
    
    assert len(bank.transactions) == 0

def test_add_funds_decimal_value_does_not_add_transaction(bank: Bank):
    bank.create_account("TestName 1")

    bank.add_funds("TestName 1", 100.50)
    
    assert len(bank.transactions) == 0

def test_add_funds_does_not_add_for_negative_amount(bank: Bank):
    bank.create_account("TestName 1")

    bank.add_funds("TestName 1", -1)
    
    assert len(bank.transactions) == 0

def test_add_funds_does_not_add_for_zero_amount(bank: Bank):
    bank.create_account("TestName 1")

    bank.add_funds("TestName 1", 0)
    
    assert len(bank.transactions) == 0
