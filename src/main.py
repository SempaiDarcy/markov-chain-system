import tkinter as tk
from tkinter import ttk  # Импортируем ttk для вкладок

class MarkovApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование Марковского процесса")
        self.root.geometry("700x600")  # Размер окна приложения

        # Создание вкладок
        self.tabs = ttk.Notebook(self.root)
        self.main_tab = tk.Frame(self.tabs)
        self.data_tab = tk.Frame(self.tabs)  # Вкладка для отображения данных
        self.tabs.add(self.main_tab, text="Главная")
        self.tabs.add(self.data_tab, text="Данные")
        self.tabs.pack(expand=1, fill="both")

# Основная программа для запуска приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()
