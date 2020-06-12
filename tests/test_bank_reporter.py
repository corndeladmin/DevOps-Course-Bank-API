from datetime import datetime

import pytest

from bank_api.bank import Bank, Account, Transaction
from bank_api.bank_reporter import BankReporter

@pytest.fixture
def mocked_bank(monkeypatch):
    """Provides a Bank instance with a mocked get_account method"""

    def mock_account(name):
        return Account('mock')

    bank = Bank()
    monkeypatch.setattr(bank, 'get_account', mock_account)
    return bank


def test_get_balance_no_transactions(mocked_bank, monkeypatch):
    monkeypatch.setattr(mocked_bank, '_transactions', {})

    bank_reporter = BankReporter(mocked_bank)
    balance = bank_reporter.get_balance('mock')
    assert balance == 0


def test_get_balance(mocked_bank, monkeypatch):

    monkeypatch.setattr(mocked_bank, '_transactions', {
        Transaction(Account('mock'), datetime.now(), 25),
        Transaction(Account('mock'), datetime.now(), 50),
        Transaction(Account('other'), datetime.now(), 100)
    })

    bank_reporter = BankReporter(mocked_bank)
    balance = bank_reporter.get_balance('mock')
    assert balance == 75
