import tkinter as tk
from tkinter import ttk
from jsonrw import JsonRW

class CreateTransaction():
    # Конструктор класу, ініціалізує основні елементи інтерфейсу
    def __init__(self, root, update_balance_callback, wallet_filename):
        super().__init__()
        self.root = root
        self.update_balance_callback = update_balance_callback
        self.dataRW = JsonRW(wallet_filename)

    # Функція для відкриття нового вікна для введення транзакції
    def open_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.geometry("250x250")

        self.var = tk.StringVar(value="expense")

        self.frame = tk.Frame(self.new_window)
        self.frame.pack(fill=tk.X, padx=3, pady=1)

        # Радіокнопки для вибору між доходом і витратами
        tk.Radiobutton(self.frame, text="Дохід", variable=self.var, value="income", command=self.update_options).pack(
            side="left")
        tk.Radiobutton(self.frame, text="Розхід", variable=self.var, value="expense", command=self.update_options).pack(
            side="right")

        tk.Label(self.new_window, text="Введіть суму:").pack()
        self.entry = tk.Entry(self.new_window)
        self.entry.pack()

        tk.Label(self.new_window, text="Виберіть причину:").pack()
        self.combobox = ttk.Combobox(self.new_window, state="readonly")
        self.combobox.pack(pady=(0, 10))

        self.update_options()  # Оновлення доступних причин залежно від типу транзакції (дохід чи витрата)

        # Кнопка для підтвердження і додавання транзакції
        tk.Button(self.new_window, text="Додати", command=self.add_to_main_screen).pack(pady=(10, 0))

    # Оновлення варіантів причин для комбо-боксу в залежності від вибраного типу транзакції
    def update_options(self):
        if self.var.get() == "income":
            self.combobox["values"] = ["ЗП", "Подарунки", "Кредити", "Інше"]  # Список причин для доходу
        else:  # Якщо вибрано "Розхід"
            self.combobox["values"] = ["Комунальні послуги", "Продукти", "Подарунки", "Побут", "Розваги", "Розвиток", "Інше"]  # Список причин для витрат
        self.combobox.current(0)

    # Функція для додавання транзакції на головний екран та збереження її в файл
    def add_to_main_screen(self):
        amount_str = self.entry.get().strip()  # Отримуємо введену суму як рядок

        if self.var.get().strip() == "expense":
            amount_str = "-" + amount_str

        reason = self.combobox.get()  # Отримуємо вибрану причину

        # Перевірка, чи є введена сума числом і чи обрана причина
        if not amount_str.replace("-", "").isdigit() or reason == "":
            return

        amount = int(amount_str)

        # Визначаємо знак залежно від типу транзакції (дохід або витрата)
        sign = "+" if self.var.get().strip() == "income" else "-"

        data = {
            "amount": amount,
            "sign": sign,
            "reason": reason
        }

        # Зберігаємо транзакцію за допомогою методу save_transaction класу JsonRW
        self.dataRW.save_transaction(data)

        # Оновлюємо баланс після збереження транзакції
        self.update_balance_callback()

        # Закриваємо вікно додавання транзакції
        self.new_window.destroy()
