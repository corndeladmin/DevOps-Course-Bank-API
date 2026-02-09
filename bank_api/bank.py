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

        # check if amount is a non negative int
        # greater than zero before adding funds
        if isinstance(amount, int) and amount > 0:
            account = self.get_account(name)
            now = datetime.now()
            self.transactions.append(Transaction(account, now, amount))        
