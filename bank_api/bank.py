from dataclasses import dataclass
from datetime import datetime
from typing import Set

@dataclass(frozen=True)
class Account:
    name: str

    def to_dict(self) -> dict:
        return { 'name': self.name }

@dataclass(frozen=True)
class Transaction:
    account: Account
    date: datetime
    amount: int

class OverdrawnError(ValueError):
    pass


class TransactionSet(set):
    def add(self, new: Transaction):
        """Override parent add method to include balance check"""
        if (
                new.amount < 0 and
                new.amount + sum(t.amount for t in self if t.account == new.account) < 0
        ):
            raise OverdrawnError
        else:
            return super().add(new)


class Bank:
    def __init__(self):
        self._accounts: Set[Account] = set()
        self._transactions: TransactionSet[Transaction] = TransactionSet()

    @property
    def accounts(self) -> Set[Account]:
        """Get a copy of the bank's accounts"""
        return self._accounts.copy()

    @property
    def transactions(self) -> Set[Transaction]:
        """Get a copy of the bank's transactions"""
        return self._transactions.copy()

    def create_account(self, name: str) -> Account:
        """Creates a new account with the name provided"""
        if not name:
            raise ValueError("Account name cannot be None or empty")

        account = Account(name)
        self._accounts.add(account)
        return account

    def get_account(self, name: str) -> Account:
        """Gets the named account, if it exists"""
        for account in self._accounts:
            if account.name == name:
                return account
        raise ValueError('Account not found')

    def add_funds(self, name: str, amount: int) -> None:
        """Add funds to the named account"""
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer.')
        account = self.get_account(name)

        now = datetime.now()
        self._transactions.add(Transaction(account, now, amount))

    def move_funds(self, name_from: str, name_to: str, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer.')

        account_from = self.get_account(name_from)
        account_to = self.get_account(name_to)

        now = datetime.now()

        self._transactions.add(Transaction(account_from, now, -1 * amount))
        self._transactions.add(Transaction(account_to, now, amount))
