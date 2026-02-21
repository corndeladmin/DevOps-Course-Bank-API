"""Unit tests for bank_report.py"""

import pytest

from bank_api.bank import Bank
from bank_api.bank_report import BankReport


@pytest.fixture
def bank() -> Bank:
    return Bank()


def test_balance_is_zero_for_new_account(bank: Bank):
    bank_report = BankReport(bank)
    bank.create_account('Alice')

    assert bank_report.get_balance('Alice') == 0


def test_balance_sums_multiple_transactions(bank: Bank):
    bank_report = BankReport(bank)
    bank.create_account('Alice')
    bank.add_funds('Alice', 500)
    bank.add_funds('Alice', 300)

    assert bank_report.get_balance('Alice') == 800


def test_balance_only_counts_own_transactions(bank: Bank):
    bank_report = BankReport(bank)
    bank.create_account('Alice')
    bank.create_account('Bob')
    bank.add_funds('Alice', 1000)
    bank.add_funds('Bob', 200)

    assert bank_report.get_balance('Alice') == 1000
