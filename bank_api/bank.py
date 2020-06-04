from datetime import datetime
from typing import Set, List

class Account:
    name: str

    def __init__(self, name: str):
        self.name = name

    def to_dict(self) -> dict: 
        return {
            "name": self.name
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Account):
            return self.name == other.name

        return False
    
    def __hash__(self) -> int:
        return self.name.__hash__()

class Transaction:
    account: Account
    date: datetime
    amount: int
    
    def __init__(self, account: Account, date: datetime, amount: int):
        self.account = account
        self.date = date
        self.amount = amount

class Bank:
    def __init__(self):
        self.accounts: Set[Account] = set()
        self.transactions: List[Transaction] = []

    def create_account(self, name: str) -> Account:
        """Creates a new account with the name provided"""
        if not name:
            raise ValueError("Account name cannot be None or empty")

        account = Account(name)
        self.accounts.add(account)
        return account

    def get_account(self, name: str) -> Account:
        """Gets the named account, if it exists"""
        for account in self.accounts:
            if account.name == name:
                return account
        raise ValueError('Account not found')

    def add_funds(self, name: str, amount: int) -> None:
        """Add funds to the named account"""
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer.')
        account = self.get_account(name)
        now = datetime.now()
        self.transactions.append(Transaction(account, now, amount))

    def move_funds(self, name_from: str, name_to: str, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError('Amount must be an integer.')
        account_from = self.get_account(name_from)
        account_to = self.get_account(name_to)

        now = datetime.now()

        self.transactions.append(Transaction(account_from, now, -1 * amount))
        self.transactions.append(Transaction(account_to, now, amount))

