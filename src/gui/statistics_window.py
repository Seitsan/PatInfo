import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class StatisticsWindow(tk.Toplevel):
    """Окно для визуализации статистических данных о пациентах.

    Окно предоставляет интерактивный интерфейс для просмотра различных
    статистических графиков на основе данных о пациентах. Поддерживает
    четыре типа визуализаций с возможностью переключения между ними.

    Attributes:
        patients: Список объектов Patient для анализа.
        current_canvas: Текущий отображаемый объект FigureCanvasTkAgg.
        right_frame: Фрейм для отображения графиков.
    """

    def __init__(self, parent, patients, app_icon_photo):
        """Инициализирует окно статистики.

        Args:
            parent: Родительское окно.
            patients: Список объектов Patient для статистического анализа.
            app_icon_photo: Иконка приложения для отображения в заголовке.
        """
        super().__init__(parent)
        self.patients = patients

        self.iconphoto(True, app_icon_photo)

        self.title("PatInfo - Сводная статистика")
        self.geometry("1000x700")
        self.configure(bg="#F5F5F5")

        self.current_canvas = None
        self.create_widgets()
        # По умолчанию показываем первый график
        self.show_gender_distribution()

    def create_widgets(self):
        """Создает и размещает виджеты окна статистики.

        Разделяет окно на две основные области:
        - Левая панель: Меню с кнопками выбора типа статистики
        - Правая панель: Область для отображения графиков
        """
        # Левая панель меню
        left_frame = tk.Frame(self, bg="#44944A", width=250)
        left_frame.pack(side="left", fill="y")

        # Заголовок меню
        tk.Label(left_frame, text="Статистика", bg="#44944A", fg="white",
                 font=("Montserrat", 18, "bold")).pack(pady=20)

        # Стиль кнопок меню
        btn_style = {"bg": "#44944A", "fg": "white", "font": ("Montserrat", 12),
                     "activebackground": "#357a3b", "bd": 0, "pady": 10, "anchor": "w", "padx": 20}

        tk.Button(left_frame, text="Распределение по полу",
                  command=self.show_gender_distribution, **btn_style).pack(fill="x")
        tk.Button(left_frame, text="Распределение по возрасту",
                  command=self.show_age_distribution, **btn_style).pack(fill="x")
        tk.Button(left_frame, text="Распределение ИМТ от пола",
                  command=self.show_bmi_by_gender, **btn_style).pack(fill="x")
        tk.Button(left_frame, text="Распределение ИМТ от возраста",
                  command=self.show_bmi_vs_age, **btn_style).pack(fill="x")

        tk.Frame(left_frame, bg="#44944A", height=50).pack()  # Spacer
        tk.Button(left_frame, text="Назад", command=self.destroy,
                  **btn_style).pack(fill="x", side="bottom", pady=20)

        # Правая панель для графиков
        self.right_frame = tk.Frame(self, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def _clear_canvas(self):
        """Очищает текущий график и освобождает ресурсы matplotlib.

        Уничтожает текущий холст tkinter и закрывает все фигуры matplotlib
        для предотвращения утечек памяти и наложения графиков.
        """
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            plt.close('all')

    def _draw_figure(self, fig):
        """Отображает фигуру matplotlib в правой панели окна.

        Args:
            fig: Объект matplotlib.figure.Figure для отображения.
        """
        self._clear_canvas()
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_gender_distribution(self):
        """Отображает круговую диаграмму распределения пациентов по полу.

        Создает pie chart, показывающий соотношение мужчин и женщин
        среди пациентов. Процентное соотношение отображается с точностью
        до одного десятичного знака.

        График включает:
        - Разделение на мужчин и женщин
        - Цветовую дифференциацию (синий для мужчин, розовый для женщин)
        - Процентные значения
        """
        males = len([p for p in self.patients if p.gender == 'М'])
        females = len([p for p in self.patients if p.gender == 'Ж'])

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie([males, females], labels=['Мужчины', 'Женщины'], autopct='%1.1f%%',
               colors=['#66b3ff', '#ff9999'], startangle=90, textprops={'fontsize': 12})
        ax.set_title("Распределение пациентов по полу", fontsize=16)
        self._draw_figure(fig)

    def show_age_distribution(self):
        """Отображает гистограмму распределения пациентов по возрасту.

        Создает гистограмму с 10 интервалами (bin), показывающую
        частотное распределение возрастов пациентов.

        График включает:
        - Гистограмму с заливкой основным цветом приложения
        - Заголовок и подписи осей
        - Сетку для удобства чтения значений
        """
        ages = [p.age for p in self.patients]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(ages, bins=10, color='#44944A', edgecolor='black', alpha=0.7)
        ax.set_title("Гистограмма распределения по возрасту", fontsize=16)
        ax.set_xlabel("Возраст (лет)", fontsize=12)
        ax.set_ylabel("Количество пациентов", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        self._draw_figure(fig)

    def show_bmi_by_gender(self):
        """Отображает box plot распределения ИМТ в зависимости от пола.

        Создает диаграмму "ящик с усами" для визуализации статистических
        характеристик ИМТ отдельно для мужчин и женщин.

        График показывает:
        - Медиану
        - Квартили (25% и 75%)
        - Выбросы (если есть)
        - Минимальные и максимальные значения

        Returns:
            Если нет пациентов обоих полов, график может быть неполным.
        """
        bmi_m = [p.bmi for p in self.patients if p.gender == 'М']
        bmi_f = [p.bmi for p in self.patients if p.gender == 'Ж']

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.boxplot([bmi_m, bmi_f], labels=['Мужчины', 'Женщины'], patch_artist=True,
                   boxprops=dict(facecolor='#44944A', color='black'))
        ax.set_title("Распределение ИМТ по полу", fontsize=16)
        ax.set_ylabel("Индекс Массы Тела", fontsize=12)
        ax.grid(linestyle='--', alpha=0.7)
        self._draw_figure(fig)

    def show_bmi_vs_age(self):
        """Отображает диаграмму рассеяния зависимости ИМТ от возраста.

        Создает scatter plot для визуализации взаимосвязи между возрастом
        и индексом массы тела. При наличии достаточного количества данных
        добавляет линию линейного тренда.

        График включает:
        - Точечную диаграмму с прозрачностью для лучшей визуализации
        - Линию линейной регрессии (если данных достаточно)
        - Заголовок и подписи осей
        - Сетку для удобства чтения
        """
        ages = [p.age for p in self.patients]
        bmis = [p.bmi for p in self.patients]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(ages, bmis, color='#44944A', alpha=0.6, edgecolors='black')

        # Линия тренда
        if len(ages) > 1:
            z = np.polyfit(ages, bmis, 1)
            p = np.poly1d(z)
            ax.plot(ages, p(ages), "r--", alpha=0.8, label="Тренд")
            ax.legend()

        ax.set_title("Зависимость ИМТ от возраста", fontsize=16)
        ax.set_xlabel("Возраст (лет)", fontsize=12)
        ax.set_ylabel("Индекс Массы Тела", fontsize=12)
        ax.grid(linestyle='--', alpha=0.7)
        self._draw_figure(fig)