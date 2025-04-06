import tkinter as tk
import json

from create_wallet import CreateWallet
from wallets_json import WalletsJson
from transactions import Transactions
from balance import Balance

class Wallets:

    # ініціалізація головного вікна і налаштування віджетів
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x400")
        self.root.title("Гривні")
        self.wallet_manager = WalletsJson()
        self.filename = "wallets.json"

        # Фрейм внизу вікна для кнопок
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", pady=10, fill="x")

        # Кнопка для додавання нового гаманця
        self.plus_button = tk.Button(self.bottom_frame, text="+", width=4, height=2, command=self.open_currency_window)
        self.plus_button.pack(side="left", padx=10)

        # Лейбл для відображення суми всіх балансів
        self.value = 0
        self.label = tk.Label(self.bottom_frame, text=str(self.sum()), font=("Arial", 16))
        self.label.pack(side="right", padx=10)

        # Фрейм для відображення всіх гаманців
        self.wallets_frame = tk.Frame(self.root)
        self.wallets_frame.pack(pady=10, fill="both", expand=True)

        self.load_wallet()
        self.root.mainloop()

    # Відкриває вікно для створення нового гаманця
    def open_currency_window(self):
        currency = CreateWallet().currency_window()

        # Якщо користувач вибрав валюту, створюємо гаманець і додаємо його на екран
        if currency:
            wallet_id = self.wallet_manager.create_wallet(currency)
            self.add_wallet(wallet_id, currency, 0)

    # Додає новий гаманець на екран
    def add_wallet(self, wallet_id, currency, balance):
        wallet_frame = tk.Frame(self.wallets_frame, bg="#e0e0e0", padx=10, pady=5)  # Створення фрейму для гаманця
        wallet_frame.pack(fill="x", pady=5, padx=10)

        # Лейбл для відображення балансу гаманця
        account_label = tk.Label(wallet_frame, text=f"Баланс: {balance}", bg="#e0e0e0")
        account_label.pack(side="left")

        # Кнопка для відкриття головного вікна для цього гаманця
        currency_button = tk.Button(wallet_frame, text=currency, command=lambda: self.open_main_window(wallet_id))
        currency_button.pack(side="right")

    # Відкриває головне вікно для конкретного гаманця
    def open_main_window(self, wallet_id):
        self.root.destroy()
        Transactions(wallet_id)

    # Завантажує всі гаманці з файлу і додає їх на екран
    def load_wallet(self):
        wallets = self.wallet_manager.load_wallets()
        for wallet in wallets:
            self.add_wallet(wallet["id"], wallet["currency"], wallet["balance"])  # Додає кожен гаманець

    # Підсумовує всі баланси гаманців
    def sum(self):
        num_files = 0
        return Balance(num_files).sum_all_balances()  # Підсумовує баланси всіх гаманців

# Запуск програми
if __name__ == "__main__":
    Wallets()
