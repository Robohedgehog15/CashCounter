import json
import os

class WalletsJson:
    def __init__(self, filename="wallets.json"):
        self.filename = filename


    #читання json файла
    def load_wallets(self):
        if os.path.exists(self.filename):
            with open(self.filename) as file_json:
                try:
                    data = json.load(file_json)
                    return data
                except json.JSONDecodeError:
                    return []
        return []

    #створення нового гаманця (нового об'єкту) у json
    def create_wallet(self, currency):
        wallet_id = len(self.load_wallets()) + 1
        new_wallet = {"id": wallet_id, "currency": currency, "balance": 0}

        existing_data = self.load_wallets()

        existing_data.append(new_wallet)

        with open(self.filename, 'w', encoding="utf-8") as file_json:
            json.dump(existing_data, file_json, indent=4)

        return wallet_id
