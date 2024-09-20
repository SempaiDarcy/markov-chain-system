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
        self.manual_data_tab = tk.Frame(self.tabs)  # Новая вкладка для ручного ввода
        self.tabs.add(self.main_tab, text="Главная")
        self.tabs.add(self.data_tab, text="Данные")
        self.tabs.add(self.manual_data_tab, text="Ручной ввод")  # Добавление вкладки для ручного ввода
        self.tabs.pack(expand=1, fill="both")

        # Окно ввода
        self.input_frame = tk.Frame(self.main_tab)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Размерность матрицы:", font=("Arial", 14)).grid(row=0, column=0)
        self.size_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=5)
        self.size_entry.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Количество тактов:", font=("Arial", 14)).grid(row=1, column=0)
        self.tacts_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=5)
        self.tacts_entry.grid(row=1, column=1)

        # Кнопка для ручного ввода данных
        self.manual_input_button = tk.Button(self.input_frame, text="Ручной ввод данных", font=("Arial", 14),
                                             command=self.show_manual_input)
        self.manual_input_button.grid(row=2, columnspan=2)

    def show_manual_input(self):
        """Переход на вкладку ручного ввода данных"""
        self.tabs.select(self.manual_data_tab)

# Основная программа для запуска приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()
