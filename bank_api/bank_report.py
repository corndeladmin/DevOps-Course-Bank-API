from bank_api.bank import Bank


class BankReport:
    def __init__(self, bank: Bank):
        self.bank = bank

    def get_balance(self, name: str) -> int:
        account = self.bank.get_account(name)
        return sum(t.amount for t in self.bank.transactions if t.account == account)
