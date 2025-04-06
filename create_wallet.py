import tkinter as tk

class CreateWallet:
    #ініціалізація
    def __init__(self):
        self.selected_currency = None


    #функція для створення вікна
    def currency_window(self):
        #створення вікна
        self.root = tk.Tk()
        self.root.title("Choose currency")
        self.root.geometry("200x200")

        label = tk.Label(self.root, text="Please enter a currency", font=("Arial", 10))
        label.pack(pady=10)

        #вибір валюти
        options = ["USD", "EUR", "UAH"]
        self.dropdown_var = tk.StringVar(value=options[0])

        dropdown = tk.OptionMenu(self.root, self.dropdown_var, *options)
        dropdown.pack(pady=10, padx=25, fill=tk.X)


        ok_button = tk.Button(self.root, text="OK", command=self.on_ok)
        ok_button.pack(pady=10)

        self.root.wait_window()
        return self.selected_currency

    def on_ok(self):
        self.selected_currency = self.dropdown_var.get()
        self.root.destroy()