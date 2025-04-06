import json
from balance import Balance
class JsonRW():
    #ініціалізація
    def __init__(self, filename):
        self.filename = filename

    #збереження транзакції у json файл
    def save_transaction(self, data):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                transactions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            transactions = []

        transactions.append(data)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=4)

        with open("wallets.json", "r", encoding="utf-8") as f:
            num_files = json.load(f)
        Balance(len(num_files)).update_wallet_balances()

    #завантаження для виведення інформації в json файлі
    def load_transactions(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                transactions = json.load(f)
                if not isinstance(transactions, list):
                    return []
                return transactions
        except (FileNotFoundError, json.JSONDecodeError):
            return []
