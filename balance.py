import json
import os
import requests

class Balance:
    #ініціалізація
    def __init__(self, num_files, wallets_file="wallets.json"):
        self.num_files = num_files
        self.wallets_file = wallets_file
        self.exchange_rates = self.get_exchange_rates()

    #отримання поточних курсів валют
    def get_exchange_rates(self):
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        try:
            response = requests.get(url)
            data = response.json()
            return {item["cc"]: item["rate"] for item in data}
        except Exception as e:
            print(f"Помилка отримання курсу валют: {e}")
            return {}

    #оновлює баланси гаманців
    def update_wallet_balances(self):
        try:
            with open(self.wallets_file, 'r', encoding='utf-8') as file:
                wallets_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Помилка при зчитуванні файлу wallets.json.")
            return

        for wallet in wallets_data:
            wallet_id = wallet["id"]
            wallet_currency = wallet["currency"]
            total_amount = 0

            wallet_file = f"wallet_{wallet_id}.json"
            if os.path.exists(wallet_file):
                with open(wallet_file, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                        total_amount = sum(entry.get("amount", 0) for entry in data)
                    except json.JSONDecodeError:
                        print(f"Помилка при зчитуванні файлу {wallet_file}.")
                        continue
            else:
                print(f"Файл {wallet_file} не знайдено.")

            wallet["balance"] = total_amount

        try:
            with open(self.wallets_file, 'w', encoding='utf-8') as file:
                json.dump(wallets_data, file, ensure_ascii=False, indent=4)
            print(f"Баланс для кожного гаманця успішно оновлено.")
        except IOError:
            print("Помилка при збереженні wallets.json.")

    #оновлює загальий баланс
    def sum_all_balances(self):
        try:
            with open(self.wallets_file, 'r', encoding='utf-8') as file:
                wallets_data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Помилка при зчитуванні файлу wallets.json.")
            return 0

        total_balance_uah = 0
        for wallet in wallets_data:
            balance = wallet["balance"]
            currency = wallet["currency"]

            #якщо валюта = гривні то просто дається, а якщо ні то переводить у гривні і додає
            if currency == "UAH":
                total_balance_uah += balance
            elif currency in self.exchange_rates:
                total_balance_uah += balance * self.exchange_rates[currency]
            else:
                print(f"Немає курсу для {currency}, баланс не враховано.")

        return round(total_balance_uah, 2)

