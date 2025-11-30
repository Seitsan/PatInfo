import tkinter as tk
from tkinter import ttk, messagebox
from src.models.patient import Patient
from src.gui.patient_form import PatientForm
from src.gui.statistics_window import StatisticsWindow
from PIL import Image, ImageTk

APP_ICON_FILENAME = "icon.ico"

def create_placeholder_image(size=(16, 16), color="#FFFFFF"):
    """Создает небольшое белое изображение-заглушку."""
    img = Image.new('RGB', size, color=color)
    return ImageTk.PhotoImage(img)

def load_app_icon(get_path_func):
    """Загружает иконку приложения или использует заглушку."""
    try:
        icon_path = get_path_func(f"resources/icons/{APP_ICON_FILENAME}")
        img = Image.open(icon_path)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки иконки приложения '{APP_ICON_FILENAME}': {e}. Используется заглушка.")
        return create_placeholder_image(size=(32, 32), color="#44944A")

class MainWindow(tk.Tk):
    """
    Главное окно приложения.
    """

    def __init__(self, data_manager, patients, get_path_func):
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
        PatientForm(self, self.on_patient_save, self.app_icon_photo)

    def open_statistics(self):
        if not self.patients:
            messagebox.showinfo("Инфо", "Нет данных для статистики")
            return
        StatisticsWindow(self, self.patients, self.app_icon_photo)

    def on_patient_save(self, data, existing_patient=None):
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
        item = self.tree.selection()
        if not item:
            return

        patient_id = self.tree.item(item, "tags")[0]
        patient = next((p for p in self.patients if p.id == patient_id), None)

        if patient:
            PatientForm(self, self.on_patient_save, self.app_icon_photo, patient=patient)
