import tkinter as tk
from tkinter import ttk, messagebox
from src.models.patient import Patient
from src.gui.patient_form import PatientForm
from src.gui.statistics_window import StatisticsWindow
from PIL import Image, ImageTk

APP_ICON_FILENAME = "icon.png"


def create_placeholder_image(size=(16, 16), color="#FFFFFF"):
    """Создает изображение-заглушку заданного размера и цвета.

    Используется когда оригинальная иконка не может быть загружена.

    Args:
        size: Кортеж (ширина, высота) в пикселях. По умолчанию (16, 16).
        color: Цвет изображения в формате HEX. По умолчанию "#FFFFFF" (белый).

    Returns:
        ImageTk.PhotoImage: Объект изображения, готовый для использования в tkinter.
    """
    img = Image.new('RGB', size, color=color)
    return ImageTk.PhotoImage(img)


def load_app_icon(get_path_func):
    """Загружает иконку приложения из файла или создает заглушку при ошибке.

    Args:
        get_path_func: Функция для получения абсолютного пути к файлу.

    Returns:
        ImageTk.PhotoImage: Загруженная иконка или изображение-заглушка.
    """
    try:
        icon_path = get_path_func(f"resources/icons/{APP_ICON_FILENAME}")
        img = Image.open(icon_path)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки иконки приложения '{APP_ICON_FILENAME}': {e}. Используется заглушка.")
        return create_placeholder_image(size=(32, 32), color="#44944A")


class MainWindow(tk.Tk):
    """Главное окно приложения PatInfo.

    Отвечает за отображение списка пациентов и предоставление основных
    функций управления: добавление, редактирование, удаление и просмотр статистики.

    Attributes:
        data_manager: Объект для управления данными пациентов.
        patients: Список объектов Patient.
        get_path: Функция для получения абсолютных путей к ресурсам.
        app_icon_photo: Загруженная иконка приложения.
        tree: Виджет Treeview для отображения таблицы пациентов.
    """

    def __init__(self, data_manager, patients, get_path_func):
        """Инициализирует главное окно приложения.

        Args:
            data_manager: Объект для сохранения/загрузки данных пациентов.
            patients: Список объектов Patient для отображения.
            get_path_func: Функция для получения абсолютных путей к ресурсам.
        """
        super().__init__()
        self.data_manager = data_manager
        self.patients = patients
        self.get_path = get_path_func

        self.app_icon_photo = load_app_icon(self.get_path)
        self.iconphoto(True, self.app_icon_photo)

        self.title("PatInfo - Система управления пациентами")
        self.geometry("1200x700")
        self.configure(bg="#F5F5F5")

        self.setup_styles()
        self.create_widgets()
        self.update_table()

    def setup_styles(self):
        """Настраивает визуальные стили для виджетов приложения.

        Определяет цвета, шрифты и внешний вид элементов интерфейса
        в соответствии с дизайн-системой приложения.
        """
        style = ttk.Style()
        style.theme_use("clam")

        # Настройка цветов и шрифтов
        bg_color = "#F5F5F5"
        accent_color = "#44944A"

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        font=("Montserrat", 11))

        style.configure("Treeview.Heading",
                        background=accent_color,
                        foreground="white",
                        font=("Montserrat", 12, "bold"))

        style.map("Treeview", background=[('selected', accent_color)])

        style.configure("TButton", font=("Montserrat", 12), padding=10)

    def create_widgets(self):
        """Создает и размещает все виджеты в главном окне.

        Разделяет интерфейс на левую панель с кнопками управления
        и правую панель с таблицей пациентов.
        """
        # Левая панель с кнопками
        left_frame = tk.Frame(self, bg="#E0E0E0", width=250)
        left_frame.pack(side="left", fill="y")

        # Заголовок
        tk.Label(left_frame, text="PatInfo", bg="#E0E0E0", fg="#44944A",
                 font=("Montserrat", 24, "bold")).pack(pady=40)

        # Кнопки управления
        btn_add = tk.Button(left_frame, text="Добавить пациента",
                            bg="#44944A", fg="white", font=("Montserrat", 12),
                            command=self.open_add_patient_form, relief="flat", pady=10)
        btn_add.pack(fill="x", padx=20, pady=10)

        btn_stats = tk.Button(left_frame, text="Статистика",
                              bg="#333333", fg="white", font=("Montserrat", 12),
                              command=self.open_statistics, relief="flat", pady=10)
        btn_stats.pack(fill="x", padx=20, pady=10)

        btn_delete = tk.Button(left_frame, text="Удалить пациента",
                               bg="#d9534f", fg="white", font=("Montserrat", 12),
                               command=self.delete_patient, relief="flat", pady=10)
        btn_delete.pack(fill="x", padx=20, pady=(250, 10))

        # Правая панель с таблицей
        right_frame = tk.Frame(self, bg="#F5F5F5")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Заголовок таблицы
        tk.Label(right_frame, text="Список пациентов", bg="#F5F5F5",
                 font=("Montserrat", 18)).pack(anchor="w", pady=(0, 10))

        # Таблица
        columns = ("lastname", "firstname", "middlename", "gender", "age", "height", "weight", "bmi", "category")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings")

        # Настройка колонок
        headers = ["Фамилия", "Имя", "Отчество", "Пол", "Возраст", "Рост", "Вес", "ИМТ", "Категория"]
        widths = [150, 120, 120, 50, 80, 80, 80, 80, 150]

        for col, header, width in zip(columns, headers, widths):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Привязка двойного клика для редактирования
        self.tree.bind("<Double-1>", self.on_double_click)

    def update_table(self):
        """Обновляет содержимое таблицы пациентов.

        Полностью очищает текущее содержимое таблицы и заполняет его
        актуальными данными из списка patients.
        """
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение данными
        for p in self.patients:
            self.tree.insert("", "end", values=(
                p.last_name, p.first_name, p.middle_name, p.gender,
                p.age, int(p.height), int(p.weight), p.bmi, p.bmi_category
            ), tags=(p.id,))

    def open_add_patient_form(self):
        """Открывает форму для добавления нового пациента.

        Создает модальное окно с формой ввода данных о пациенте.
        """
        PatientForm(self, self.on_patient_save, self.app_icon_photo)

    def open_statistics(self):
        """Открывает окно со статистикой по пациентам.

        Если список пациентов пуст, показывает информационное сообщение.
        """
        if not self.patients:
            messagebox.showinfo("Инфо", "Нет данных для статистики")
            return
        StatisticsWindow(self, self.patients, self.app_icon_photo)

    def on_patient_save(self, data, existing_patient=None):
        """Обрабатывает сохранение данных пациента.

        Вызывается после подтверждения ввода в форме пациента.
        Обновляет существующего пациента или создает нового,
        сохраняет изменения и обновляет таблицу.

        Args:
            data: Словарь с данными пациента.
            existing_patient: Существующий объект Patient для обновления.
                Если None, создается новый пациент.
        """
        if existing_patient:
            # Обновление существующего
            existing_patient.last_name = data['last_name']
            existing_patient.first_name = data['first_name']
            existing_patient.middle_name = data['middle_name']
            existing_patient.gender = data['gender']
            existing_patient.birth_date = data['birth_date']
            existing_patient.height = data['height']
            existing_patient.weight = data['weight']
        else:
            # Создание нового
            new_patient = Patient(**data)
            self.patients.append(new_patient)

        # Сохранение и обновление UI
        self.data_manager.save_patients(self.patients)
        self.update_table()

    def delete_patient(self):
        """Удаляет выбранного пациента из списка.

        Запрашивает подтверждение перед удалением. Если пациент выбран,
        удаляет его из списка patients, сохраняет изменения и обновляет таблицу.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите пациента для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить пациента?"):
            # Получаем значения выделенной строки
            vals = self.tree.item(selected_item, "values")
            # Находим пациента
            patient_id = self.tree.item(selected_item, "tags")[0]

            self.patients = [p for p in self.patients if p.id != patient_id]
            self.data_manager.save_patients(self.patients)
            self.update_table()

    def on_double_click(self, event):
        """Обрабатывает двойной клик по строке таблицы.

        Открывает форму редактирования для выбранного пациента.

        Args:
            event: Событие мыши от tkinter.
        """
        item = self.tree.selection()
        if not item:
            return

        patient_id = self.tree.item(item, "tags")[0]
        patient = next((p for p in self.patients if p.id == patient_id), None)

        if patient:
            PatientForm(self, self.on_patient_save, self.app_icon_photo, patient=patient)
