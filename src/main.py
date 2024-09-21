import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import networkx as nx  # Для построения графа переходов

class MarkovApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование Марковского процесса")
        self.root.geometry("900x700")  # Изменение размера окна для лучшего отображения

        # Создание вкладок
        self.tabs = ttk.Notebook(self.root)
        self.main_tab = tk.Frame(self.tabs)
        self.data_tab = tk.Frame(self.tabs)
        self.manual_data_tab = tk.Frame(self.tabs)  # Новая вкладка для ручного ввода
        self.tabs.add(self.main_tab, text="Главная")
        self.tabs.add(self.data_tab, text="Данные")
        self.tabs.add(self.manual_data_tab, text="Ручной ввод")  # Добавление вкладки для ручного ввода
        self.tabs.pack(expand=1, fill="both")

        # Заблокировать вкладки "Ручной ввод" и "Данные"
        self.tabs.tab(self.manual_data_tab, state='disabled')
        self.tabs.tab(self.data_tab, state='disabled')

        # Инициализация переменных
        self.size = tk.IntVar()
        self.tacts = tk.IntVar()

        # Окно ввода
        self.input_frame = tk.Frame(self.main_tab)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Размерность матрицы:", font=("Arial", 14)).grid(row=0, column=0)
        self.size_entry = tk.Entry(self.input_frame, textvariable=self.size, font=("Arial", 14), width=5)
        self.size_entry.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Количество тактов:", font=("Arial", 14)).grid(row=1, column=0)
        self.tacts_entry = tk.Entry(self.input_frame, textvariable=self.tacts, font=("Arial", 14), width=5)
        self.tacts_entry.grid(row=1, column=1)

        # Кнопка генерации
        self.generate_button = tk.Button(self.input_frame, text="Сгенерировать случайные данные", font=("Arial", 14),
                                         command=self.generate_random)
        self.generate_button.grid(row=2, columnspan=2)

        # Кнопка для тестовых данных
        self.test_button = tk.Button(self.input_frame, text="Тестовые данные", font=("Arial", 14),
                                     command=self.generate_test_data)
        self.test_button.grid(row=3, columnspan=2)

        # Кнопка для ручного ввода данных
        self.manual_input_button = tk.Button(self.input_frame, text="Ручной ввод данных", font=("Arial", 14),
                                             command=self.show_manual_input)
        self.manual_input_button.grid(row=4, columnspan=2)

        # Сообщение об ошибке
        self.error_message = tk.Label(self.main_tab, text="", fg="red", font=("Arial", 14))
        self.error_message.pack()

        # Кнопка расчета (обновлено)
        self.calculate_button = tk.Button(self.main_tab, text="Вычислить вероятности", font=("Arial", 14),
                                          command=self.calculate, state=tk.DISABLED)
        self.calculate_button.pack(pady=10)

        # Новая кнопка для отображения графа переходов
        self.show_graph_button = tk.Button(self.main_tab, text="Показать граф переходов", font=("Arial", 14),
                                           command=self.show_transition_graph, state=tk.DISABLED)
        self.show_graph_button.pack(pady=10)

        # Сообщение об ошибке на вкладке "Ручной ввод"
        self.manual_error_message = tk.Label(self.manual_data_tab, text="", fg="red", font=("Arial", 14))
        self.manual_error_message.pack()

        # Инициализация данных
        self.initial_prob_vector = None
        self.transition_matrix = None
        self.cost_vector = None

    def show_manual_input(self):
        """Переход на вкладку ручного ввода данных"""
        size = self.size.get()
        if size <= 0:
            self.error_message.config(text="Размерность матрицы должна быть больше 0.")
            return

        # Разблокировать вкладку ручного ввода
        self.tabs.tab(self.manual_data_tab, state='normal')

        # Очищаем предыдущие виджеты на вкладке для ручного ввода
        for widget in self.manual_data_tab.winfo_children():
            widget.destroy()

        self.manual_input_frame = tk.Frame(self.manual_data_tab)
        self.manual_input_frame.pack(pady=10)

        # Ввод начальных вероятностей
        tk.Label(self.manual_input_frame, text="Начальный вектор вероятностей:", font=("Arial", 14)).grid(row=0, column=0, columnspan=size)
        self.manual_prob_entries = []
        for i in range(size):
            entry = tk.Entry(self.manual_input_frame, font=("Arial", 14), width=5)
            entry.insert(0, '0')  # Инициализация значением 0
            entry.grid(row=1, column=i)
            entry.bind("<Return>", self.focus_next_widget)  # Привязка события Enter
            self.manual_prob_entries.append(entry)

        # Ввод матрицы переходов
        tk.Label(self.manual_input_frame, text="Матрица переходов:", font=("Arial", 14)).grid(row=2, column=0, columnspan=size)
        self.manual_transition_entries = []
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.manual_input_frame, font=("Arial", 14), width=5)
                entry.insert(0, '0')  # Инициализация значением 0
                entry.grid(row=i+3, column=j)
                entry.bind("<Return>", self.focus_next_widget)  # Привязка события Enter
                row_entries.append(entry)
            self.manual_transition_entries.append(row_entries)

        # Ввод вектора трудоемкостей
        tk.Label(self.manual_input_frame, text="Вектор трудоемкости:", font=("Arial", 14)).grid(row=size+3, column=0, columnspan=size)
        self.manual_cost_entries = []
        for i in range(size):
            entry = tk.Entry(self.manual_input_frame, font=("Arial", 14), width=5)
            entry.insert(0, '0')  # Инициализация значением 0
            entry.grid(row=size+4, column=i)
            entry.bind("<Return>", self.focus_next_widget)  # Привязка события Enter
            self.manual_cost_entries.append(entry)

        # Кнопка подтверждения ввода
        self.submit_button = tk.Button(self.manual_input_frame, text="Подтвердить ввод", font=("Arial", 14),
                                       command=self.process_manual_input)
        self.submit_button.grid(row=size+5, columnspan=size)

        # Сообщение об ошибке на вкладке "Ручной ввод"
        self.manual_error_message = tk.Label(self.manual_data_tab, text="", fg="red", font=("Arial", 14))
        self.manual_error_message.pack()

        # Переключаемся на вкладку "Ручной ввод"
        self.tabs.select(self.manual_data_tab)

    def focus_next_widget(self, event):
        """Переход к следующему виджету при нажатии Enter"""
        event.widget.tk_focusNext().focus()
        return "break"

    def validate_entry(self, entry):
        """Проверка правильности ввода и подсветка ошибок в полях"""
        try:
            value = float(entry.get())
            if value < 0:
                entry.config(bg='red')
                return False
            else:
                entry.config(bg='white')  # Возвращаем исходный цвет, если всё правильно
                return True
        except ValueError:
            entry.config(bg='red')
            return False

    def process_manual_input(self):
        """Обработка введённых вручную данных"""
        size = self.size.get()

        try:
            # Проверка и считывание начальных вероятностей
            self.initial_prob_vector = np.array([float(entry.get()) for entry in self.manual_prob_entries if self.validate_entry(entry)])
            if not np.isclose(self.initial_prob_vector.sum(), 1.0):
                raise ValueError("Сумма начальных вероятностей должна быть равна 1.")

            # Проверка и считывание матрицы переходов
            self.transition_matrix = np.array([[float(entry.get()) for entry in row if self.validate_entry(entry)] for row in self.manual_transition_entries])
            for row in self.transition_matrix:
                if not np.isclose(row.sum(), 1.0):
                    raise ValueError("Сумма каждой строки матрицы переходов должна быть равна 1.")

            # Проверка и считывание вектора трудоемкостей
            self.cost_vector = np.array([float(entry.get()) for entry in self.manual_cost_entries if self.validate_entry(entry)])

            self.show_data(size)
            self.calculate_button.config(state=tk.NORMAL)
            self.show_graph_button.config(state=tk.NORMAL)
            self.error_message.config(text="")
            self.manual_error_message.config(text="")  # Очищаем ошибку на вкладке ручного ввода
            self.tabs.tab(self.data_tab, state='normal')  # Разблокируем вкладку "Данные"
            self.tabs.select(self.data_tab)

        except ValueError as e:
            # Сообщение об ошибке на главной странице
            self.error_message.config(text=f"Ошибка ввода: {str(e)}")
            # Сообщение об ошибке на вкладке "Ручной ввод"
            self.manual_error_message.config(text=f"Ошибка ввода: {str(e)}")
            self.calculate_button.config(state=tk.DISABLED)
            self.show_graph_button.config(state=tk.DISABLED)

    def generate_random(self):
        """Генерация случайных начальных вероятностей, матрицы переходов и вектора трудоемкостей"""
        try:
            size = self.size.get()
            if size <= 0:
                raise ValueError("Размерность матрицы должна быть больше 0.")

            # Генерация случайного вектора начальных вероятностей
            self.initial_prob_vector = self.generate_probabilities(size)

            # Генерация случайной матрицы переходов
            self.transition_matrix = np.array([self.generate_probabilities(size) for _ in range(size)])

            # Генерация вектора трудоемкостей
            self.cost_vector = np.random.choice([100, 200, 300, 250, 150], size=size)

            self.show_data(size)
            self.calculate_button.config(state=tk.NORMAL)
            self.show_graph_button.config(state=tk.NORMAL)  # Активируем кнопку графа переходов
            self.error_message.config(text="")
            self.tabs.tab(self.data_tab, state='normal')  # Разблокируем вкладку "Данные"
            self.tabs.select(self.data_tab)  # Переключаемся на вкладку "Данные" после генерации

        except ValueError as e:
            self.error_message.config(text=str(e))
            self.calculate_button.config(state=tk.DISABLED)

    def generate_test_data(self):
        """Генерация тестовых данных"""
        size = self.size.get()  # Берем введенное пользователем значение
        tacts = self.tacts.get()  # Берем введенное пользователем количество тактов

        if size <= 0 or tacts <= 0:
            self.error_message.config(text="Размер матрицы и количество тактов должны быть больше 0.")
            return

        # Вектор начальных вероятностей для тестовых данных (размер вектора = размерность)
        self.initial_prob_vector = np.array([0.5, 0.5, 0.0, 0.0, 0.0])

        # Тестовая матрица переходов
        self.transition_matrix = np.array([
            [0.3, 0.2, 0.1, 0.2, 0.2],
            [0.1, 0.6, 0.1, 0.1, 0.1],
            [0.2, 0.4, 0.2, 0.1, 0.1],
            [0.25, 0.15, 0.2, 0.2, 0.2],
            [0.0, 0.0, 0.0, 0.0, 1.0]
        ])

        # Вектор трудоемкости (размер = размерность)
        self.cost_vector = np.array([100, 200, 300, 250, 150])

        self.show_data(size)
        self.calculate_button.config(state=tk.NORMAL)
        self.show_graph_button.config(state=tk.NORMAL)
        self.error_message.config(text="")
        self.tabs.tab(self.data_tab, state='normal')  # Разблокируем вкладку "Данные"
        self.tabs.select(self.data_tab)

    def generate_probabilities(self, size):
        """Генерация вектора с числами от 0 до 1, нормализованных так, чтобы сумма была равна 1"""
        values = np.random.choice(np.arange(0.0, 1.1, 0.1), size=size, replace=True)
        values = np.round(values, 2)
        return values / values.sum()  # Нормализация до суммы 1

    def show_data(self, size):
        """Отображение данных на вкладке с выравниванием чисел"""
        # Очистим вкладку с данными, если она уже заполнена
        for widget in self.data_tab.winfo_children():
            widget.destroy()

        # Начальный вектор вероятностей
        tk.Label(self.data_tab, text="Начальный вектор вероятностей X0:", font=("Arial", 14)).pack(pady=10)
        for i, prob in enumerate(self.initial_prob_vector):
            tk.Label(self.data_tab, text=f"P{i + 1}: {self.format_number(prob)}", font=("Arial", 14)).pack()

        # Разделитель
        tk.Label(self.data_tab, text="-"*50, font=("Arial", 14)).pack(pady=10)

        # Заголовок над матрицей переходов
        tk.Label(self.data_tab, text="Матрица переходов:", font=("Arial", 14)).pack(pady=10)

        # Используем Text для выравнивания чисел матрицы
        text_widget = tk.Text(self.data_tab, height=10, width=70, font=("Arial", 12))  # Увеличена ширина для корректного отображения
        text_widget.pack()

        # Форматирование строк матрицы
        for row in self.transition_matrix:
            formatted_row = " | ".join([self.format_number(elem) for elem in row]) + "\n"
            text_widget.insert(tk.END, formatted_row)

        text_widget.config(state=tk.DISABLED)  # Отключаем редактирование

        # Разделитель
        tk.Label(self.data_tab, text="-"*50, font=("Arial", 14)).pack(pady=10)

        # Вектор трудоемкости
        tk.Label(self.data_tab, text="Вектор трудоемкости:", font=("Arial", 14)).pack()
        tk.Label(self.data_tab, text=f"{self.format_cost_vector(self.cost_vector)}", font=("Arial", 14)).pack()

    def format_number(self, num):
        """Форматирование числа: если оно целое, оставить без десятичных знаков; если нет, оставить две значимые цифры"""
        if num.is_integer():
            return str(int(num))  # Возвращаем целое число без точки
        else:
            return f"{num:.2f}".rstrip('0').rstrip('.')

    def format_cost_vector(self, vector):
        """Форматирование вектора трудоемкости"""
        return " | ".join([str(int(x)) if x.is_integer() else str(x) for x in vector])

    def kolmogorov_system(self, t, P):
        """Система уравнений Колмогорова"""
        return np.dot(P, self.transition_matrix)

    def calculate(self):
        """Выполнение симуляции Марковской цепи и отображение графика вероятностей"""
        if self.initial_prob_vector is None or self.transition_matrix is None or self.cost_vector is None:
            self.error_message.config(text="Данные не сгенерированы.")
            return

        size = self.size.get()
        tacts = self.tacts.get()

        if tacts <= 0:
            self.error_message.config(text="Количество тактов должно быть больше 0.")
            return

        # Решение системы уравнений Колмогорова методом solve_ivp
        t_span = (0, tacts)
        t_eval = np.linspace(0, tacts, num=50)  # Плавные промежутки для оценки
        solution = solve_ivp(self.kolmogorov_system, t_span, self.initial_prob_vector, t_eval=t_eval)

        # Вероятности на каждом такте
        history = solution.y.T

        # Отобразить результаты
        self.plot_results(history)

    def plot_results(self, history):
        """Построение графика вероятностей по времени"""
        tacts = np.linspace(0, history.shape[0] - 1, history.shape[0])
        plt.figure(figsize=(10, 6))

        # График вероятностей
        for i in range(history.shape[1]):
            plt.plot(tacts, history[:, i], label=f"Состояние {i + 1}")

        plt.title("Симуляция Марковского процесса")
        plt.xlabel("Время (такты)")
        plt.ylabel("Вероятность")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig("markov_process_probabilities.png")  # Сохранение графика
        plt.show()

    def show_transition_graph(self):
        """Построение графа переходов между состояниями"""
        if self.transition_matrix is None:
            self.error_message.config(text="Матрица переходов не сгенерирована.")
            return

        size = self.size.get()

        # Создаем граф с помощью NetworkX
        G = nx.DiGraph()

        # Добавляем узлы
        for i in range(size):
            G.add_node(f"S{i + 1}")

        # Добавляем ребра на основе матрицы переходов
        for i in range(size):
            for j in range(size):
                if self.transition_matrix[i, j] > 0:  # Только если вероятность перехода > 0
                    G.add_edge(f"S{i + 1}", f"S{j + 1}", weight=self.transition_matrix[i, j])

        # Рисуем граф
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold',
                arrows=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.title("Граф переходов между состояниями")
        plt.show()


# Основная программа для запуска приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()
