import tkinter as tk
from tkinter import ttk
import numpy as np  # Для работы с данными


class MarkovApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование Марковского процесса")
        self.root.geometry("700x600")

        # Создание вкладок
        self.tabs = ttk.Notebook(self.root)
        self.main_tab = tk.Frame(self.tabs)
        self.data_tab = tk.Frame(self.tabs)
        self.manual_data_tab = tk.Frame(self.tabs)
        self.tabs.add(self.main_tab, text="Главная")
        self.tabs.add(self.data_tab, text="Данные")
        self.tabs.add(self.manual_data_tab, text="Ручной ввод")
        self.tabs.pack(expand=1, fill="both")

        # Окно ввода на вкладке "Главная"
        self.input_frame = tk.Frame(self.main_tab)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Размерность матрицы:", font=("Arial", 14)).grid(row=0, column=0)
        self.size_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=5)
        self.size_entry.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Количество тактов:", font=("Arial", 14)).grid(row=1, column=0)
        self.tacts_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=5)
        self.tacts_entry.grid(row=1, column=1)

        # Кнопка генерации случайных данных
        self.generate_button = tk.Button(self.input_frame, text="Сгенерировать случайные данные", font=("Arial", 14),
                                         command=self.generate_random)
        self.generate_button.grid(row=2, columnspan=2)

        # Кнопка для ручного ввода данных
        self.manual_input_button = tk.Button(self.input_frame, text="Ручной ввод данных", font=("Arial", 14),
                                             command=self.show_manual_input)
        self.manual_input_button.grid(row=3, columnspan=2)

        # Поле для вывода данных
        self.result_frame = tk.Frame(self.data_tab)
        self.result_frame.pack(pady=10)

    def generate_random(self):
        """Функция для генерации случайных данных"""
        size = int(self.size_entry.get())
        if size <= 0:
            return

        # Генерация случайного вектора начальных вероятностей
        initial_prob_vector = self.generate_probabilities(size)

        # Генерация случайной матрицы переходов
        transition_matrix = np.array([self.generate_probabilities(size) for _ in range(size)])

        # Генерация вектора трудоемкостей
        cost_vector = np.random.choice([100, 200, 300, 250, 150], size=size)

        # Отображаем сгенерированные данные на вкладке "Данные"
        self.display_generated_data(initial_prob_vector, transition_matrix, cost_vector)

    def generate_probabilities(self, size):
        """Генерация нормализованных вероятностей"""
        values = np.random.choice(np.arange(0.0, 1.1, 0.1), size=size, replace=True)
        values = np.round(values, 2)
        return values / values.sum()

    def display_generated_data(self, initial_prob, transition_matrix, cost_vector):
        """Отображение сгенерированных данных на вкладке 'Данные'"""

        # Очищаем результат предыдущих данных
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Начальные вероятности
        tk.Label(self.result_frame, text="Начальный вектор вероятностей:", font=("Arial", 14)).pack()
        for i, prob in enumerate(initial_prob):
            tk.Label(self.result_frame, text=f"P{i+1}: {prob:.2f}", font=("Arial", 12)).pack()

        # Матрица переходов
        tk.Label(self.result_frame, text="Матрица переходов:", font=("Arial", 14)).pack()
        for row in transition_matrix:
            row_text = " ".join(f"{val:.2f}" for val in row)
            tk.Label(self.result_frame, text=row_text, font=("Arial", 12)).pack()

        # Вектор трудоемкостей
        tk.Label(self.result_frame, text="Вектор трудоемкости:", font=("Arial", 14)).pack()
        cost_text = " ".join(f"{cost}" for cost in cost_vector)
        tk.Label(self.result_frame, text=cost_text, font=("Arial", 12)).pack()

        self.tabs.select(self.data_tab)  # Переход на вкладку "Данные"

    def show_manual_input(self):
        """Переход на вкладку 'Ручной ввод данных'"""
        size = int(self.size_entry.get())
        if size <= 0:
            return

        # Очищаем вкладку "Ручной ввод" перед добавлением новых элементов
        for widget in self.manual_data_tab.winfo_children():
            widget.destroy()

        self.manual_input_frame = tk.Frame(self.manual_data_tab)
        self.manual_input_frame.pack(pady=10)

        # Ввод начальных вероятностей
        tk.Label(self.manual_input_frame, text="Начальный вектор вероятностей:", font=("Arial", 14)).grid(row=0, column=0, columnspan=size)
        self.manual_prob_entries = []
        for i in range(size):
            entry = tk.Entry(self.manual_input_frame, font=("Arial", 14), width=5)
            entry.grid(row=1, column=i)
            self.manual_prob_entries.append(entry)

        # Ввод матрицы переходов
        tk.Label(self.manual_input_frame, text="Матрица переходов:", font=("Arial", 14)).grid(row=2, column=0, columnspan=size)
        self.manual_transition_entries = []
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.manual_input_frame, font=("Arial", 14), width=5)
                entry.grid(row=i+3, column=j)
                row_entries.append(entry)
            self.manual_transition_entries.append(row_entries)

        # Ввод вектора трудоемкостей
        tk.Label(self.manual_input_frame, text="Вектор трудоемкости:", font=("Arial", 14)).grid(row=size+3, column=0, columnspan=size)
        self.manual_cost_entries = []
        for i in range(size):
            entry = tk.Entry(self.manual_input_frame, font=("Arial", 14), width=5)
            entry.grid(row=size+4, column=i)
            self.manual_cost_entries.append(entry)

        # Кнопка подтверждения ввода
        self.submit_button = tk.Button(self.manual_input_frame, text="Подтвердить ввод", font=("Arial", 14),
                                       command=self.process_manual_input)
        self.submit_button.grid(row=size+5, columnspan=size)

        # Переход на вкладку "Ручной ввод"
        self.tabs.select(self.manual_data_tab)

    def process_manual_input(self):
        """Обработка введённых вручную данных"""
        size = int(self.size_entry.get())

        try:
            # Считывание начальных вероятностей
            initial_prob_vector = np.array([float(entry.get()) for entry in self.manual_prob_entries])
            if not np.isclose(initial_prob_vector.sum(), 1.0):
                raise ValueError("Сумма начальных вероятностей должна быть равна 1.")

            # Считывание матрицы переходов
            transition_matrix = np.array([[float(entry.get()) for entry in row] for row in self.manual_transition_entries])
            for row in transition_matrix:
                if not np.isclose(row.sum(), 1.0):
                    raise ValueError("Сумма каждой строки матрицы переходов должна быть равна 1.")

            # Считывание вектора трудоемкостей
            cost_vector = np.array([float(entry.get()) for entry in self.manual_cost_entries])

            print("Данные успешно введены!")
            print(f"Начальные вероятности: {initial_prob_vector}")
            print(f"Матрица переходов: \n{transition_matrix}")
            print(f"Вектор трудоемкости: {cost_vector}")

        except ValueError as e:
            print(f"Ошибка ввода: {str(e)}")


# Основная программа для запуска приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()
