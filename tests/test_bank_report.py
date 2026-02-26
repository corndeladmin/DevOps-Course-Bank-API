"""Unit tests for bank_report.py"""

from datetime import datetime

import pytest

from bank_api.bank import Account, Bank, Transaction
from bank_api.bank_report import BankReport


@pytest.fixture
def bank() -> Bank:
    return Bank()


def test_balance_is_zero_with_no_transactions(bank: Bank, monkeypatch):
    bank_report = BankReport(bank)
    account = Account('Alice')
    monkeypatch.setattr(bank, 'get_account', lambda name: account)
    monkeypatch.setattr(bank, 'transactions', [])

    assert bank_report.get_balance('Alice') == 0


def test_balance_sums_transactions(bank: Bank, monkeypatch):
    bank_report = BankReport(bank)
    account = Account('Alice')
    monkeypatch.setattr(bank, 'get_account', lambda name: account)
    monkeypatch.setattr(bank, 'transactions', [
        Transaction(account, datetime.now(), 500),
        Transaction(account, datetime.now(), 300),
    ])

    assert bank_report.get_balance('Alice') == 800


def test_balance_ignores_other_accounts_transactions(bank: Bank, monkeypatch):
    bank_report = BankReport(bank)
    alice = Account('Alice')
    bob = Account('Bob')
    monkeypatch.setattr(bank, 'get_account', lambda name: alice)
    monkeypatch.setattr(bank, 'transactions', [
        Transaction(alice, datetime.now(), 1000),
        Transaction(bob, datetime.now(), 200),
    ])

    assert bank_report.get_balance('Alice') == 1000
