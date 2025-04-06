import tkinter as tk
import json

from jsonrw import JsonRW
from create_transaction import CreateTransaction
from wallets_json import WalletsJson


class Transactions():
    #ініціалізація
    def __init__(self, wallet_id):
        self.wallet_id = wallet_id
        self.wallet_file = f"wallet_{wallet_id}.json"
        self.json_rw = JsonRW(self.wallet_file)
        self.wallet_manager = WalletsJson()


        self.root = tk.Tk()
        self.root.title("Гаманець")
        self.root.geometry("275x400")


        self.balance = 0

        self.setup_ui()
        self.load_transactions_from_json()

        self.root.mainloop()

    #створення об'єтів у вікні
    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(frame, text="додати", width=8, height=1, command=self.open_create_transaction_window).pack()

        transactions_frame = tk.Frame(self.root)
        transactions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.transactions_text = tk.Text(transactions_frame, width=30, height=10, wrap=tk.WORD)
        self.transactions_text.pack(side="left", fill=tk.BOTH, expand=True)
        self.transactions_text.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(transactions_frame, orient="vertical", command=self.transactions_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.transactions_text.config(yscrollcommand=scrollbar.set)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(bottom_frame, text="Гаманці", command=lambda: self.open_main_window(self.root)).pack(side="left")
        self.balance_label = tk.Label(bottom_frame, text=f"Загальний баланс: {self.balance}")
        self.balance_label.pack(side="right")

    def open_main_window(self, root):
        root.destroy()
        from wallets import Wallets
        Wallets()

    def open_create_transaction_window(self):
        CreateTransaction(self.root, self.load_transactions_from_json, self.wallet_file).open_window()

    #вивдення на вікно інформацію з json
    def load_transactions_from_json(self):
        self.balance = 0
        transactions = self.json_rw.load_transactions()

        self.transactions_text.config(state=tk.NORMAL)
        self.transactions_text.delete(1.0, tk.END)
        for transaction in transactions:
            amount = transaction["amount"]
            sign = transaction["sign"]
            reason = transaction["reason"]
            transaction_text = f"{sign} {amount}: {reason}\n"

            self.balance += amount

            tag = "income" if sign == "+" else "expense"
            self.transactions_text.insert(tk.END, transaction_text, tag)

        self.transactions_text.tag_configure("income", foreground="black", background="lightgreen", justify="center")
        self.transactions_text.tag_configure("expense", foreground="black", background="lightcoral", justify="center")
        self.transactions_text.config(state=tk.DISABLED)

        self.balance_label.config(text=f"Загальний баланс: {self.balance}")



if __name__ == "__main__":
    Transactions(1)
