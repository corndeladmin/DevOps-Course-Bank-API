from bank_api.bank import Bank


class BankReporter:
    def __init__(self, bank: Bank):
        self._bank = bank

    def get_balance(self, name) -> int:
        account = self._bank.get_account(name)
        return sum(t.amount for t in self._bank.transactions if t.account == account)
