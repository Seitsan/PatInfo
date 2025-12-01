import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, datetime

# Константы для валидации
MIN_HEIGHT_CM = 50  # Минимальный рост в сантиметрах
MAX_HEIGHT_CM = 250  # Максимальный рост в сантиметрах
MIN_WEIGHT_KG = 1  # Минимальный вес в килограммах
MAX_WEIGHT_KG = 300  # Максимальный вес в килограммах
MIN_AGE_YEARS = 1  # Минимальный возраст в годах
MAX_AGE_YEARS = 130  # Максимальный возраст в годах


class PatientForm(tk.Toplevel):
    """Модальное окно формы для добавления или редактирования пациента.

    Окно содержит поля для ввода данных пациента с валидацией:
    - Фамилия, имя, отчество
    - Пол
    - Дата рождения
    - Рост и вес
    Все поля проходят проверку на корректность значений.

    Attributes:
        on_save_callback: Функция обратного вызова, вызываемая при сохранении.
        patient: Объект Patient для редактирования или None для создания нового.
        entry_last_name: Поле ввода для фамилии.
        entry_first_name: Поле ввода для имени.
        entry_middle_name: Поле ввода для отчества.
        combo_gender: Выпадающий список для выбора пола.
        date_entry: Виджет выбора даты рождения.
        spin_height: Счетчик для ввода роста.
        spin_weight: Счетчик для ввода веса.
    """

    def __init__(self, parent, on_save_callback, app_icon_photo, patient=None):
        """Инициализирует форму пациента.

        Args:
            parent: Родительское окно.
            on_save_callback: Функция, вызываемая при нажатии кнопки "Сохранить".
                Принимает два аргумента: данные пациента и объект пациента (если редактирование).
            app_icon_photo: Иконка приложения для отображения в заголовке окна.
            patient: Объект Patient для редактирования существующего пациента.
                Если None, создается форма для добавления нового пациента.
        """
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.patient = patient

        self.iconphoto(True, app_icon_photo)

        self.title("Patinfo - Редактирование пациента" if patient else "PatInfo - Добавить пациента")
        self.geometry("450x550")
        self.configure(bg="#F5F5F5")

        self.create_form()

    def create_form(self):
        """Создает и размещает все виджеты формы.

        Создает поля ввода для всех данных пациента, организует их в логические
        группы и устанавливает начальные значения при редактировании существующего пациента.
        """
        padding = {'padx': 20, 'pady': 10}
        label_font = ("Montserrat", 12)

        # Фамилия
        tk.Label(self, text="Фамилия:", bg="#F5F5F5", font=label_font).pack(anchor='w', **padding)
        self.entry_last_name = ttk.Entry(self, font=label_font)
        self.entry_last_name.pack(fill='x', padx=20)

        # Имя
        tk.Label(self, text="Имя:", bg="#F5F5F5", font=label_font).pack(anchor='w', **padding)
        self.entry_first_name = ttk.Entry(self, font=label_font)
        self.entry_first_name.pack(fill='x', padx=20)

        # Отчество
        tk.Label(self, text="Отчество:", bg="#F5F5F5", font=label_font).pack(anchor='w', **padding)
        self.entry_middle_name = ttk.Entry(self, font=label_font)
        self.entry_middle_name.pack(fill='x', padx=20)

        # Пол
        tk.Label(self, text="Пол:", bg="#F5F5F5", font=label_font).pack(anchor='w', **padding)
        self.combo_gender = ttk.Combobox(self, values=["М", "Ж"], state="readonly", font=label_font)
        self.combo_gender.pack(fill='x', padx=20)

        # Дата рождения
        tk.Label(self, text="Дата рождения:", bg="#F5F5F5", font=label_font).pack(anchor='w', **padding)
        self.date_entry = DateEntry(self, width=12, background='#44944A',
                                    foreground='white', borderwidth=2, date_pattern='dd.mm.yyyy', font=label_font)
        self.date_entry.pack(fill='x', padx=20)

        # Рост и Вес (в одной строке для компактности)
        frame_metrics = tk.Frame(self, bg="#F5F5F5")
        frame_metrics.pack(fill='x', padx=20, pady=10)

        tk.Label(frame_metrics, text="Рост (см):", bg="#F5F5F5", font=label_font).grid(row=0, column=0, sticky='w')
        self.spin_height = tk.Spinbox(frame_metrics, from_=50, to=250, font=label_font, width=5)
        self.spin_height.grid(row=0, column=1, padx=10)

        tk.Label(frame_metrics, text="Вес (кг):", bg="#F5F5F5", font=label_font).grid(row=0, column=2, sticky='w')
        self.spin_weight = tk.Spinbox(frame_metrics, from_=1, to=300, font=label_font, width=5)
        self.spin_weight.grid(row=0, column=3, padx=10)

        # Кнопки
        btn_frame = tk.Frame(self, bg="#F5F5F5")
        btn_frame.pack(pady=30)

        ttk.Button(btn_frame, text="Сохранить", command=self.save).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side='left', padx=10)

        # Заполнение полей если редактирование
        if self.patient:
            self.fill_existing_patient_data()

    def fill_existing_patient_data(self):
        """Заполняет поля формы данными существующего пациента.

        Вызывается при редактировании пациента. Загружает все данные из объекта
        Patient в соответствующие поля формы.
        """
        self.entry_last_name.insert(0, self.patient.last_name)
        self.entry_first_name.insert(0, self.patient.first_name)
        self.entry_middle_name.insert(0, self.patient.middle_name)
        self.combo_gender.set(self.patient.gender)
        self.date_entry.set_date(self.patient.birth_date)
        self.spin_height.delete(0, "end")
        self.spin_height.insert(0, int(self.patient.height))
        self.spin_weight.delete(0, "end")
        self.spin_weight.insert(0, int(self.patient.weight))

    def save(self):
        """Сохраняет данные пациента после валидации.

        Выполняет валидацию всех полей формы:
        1. Проверяет обязательные поля
        2. Проверяет корректность числовых значений (рост, вес)
        3. Проверяет диапазоны роста и веса
        4. Проверяет корректность даты рождения и возраст

        При успешной валидации собирает данные в словарь и вызывает
        callback-функцию, переданную в конструктор.

        Raises:
            Показывает диалоговые окна с ошибками при невалидных данных.
        """
        # Валидация обязательных полей
        if not all([self.entry_last_name.get(), self.entry_first_name.get(), self.combo_gender.get()]):
            messagebox.showerror("Ошибка", "Заполните обязательные поля (Фамилия, Имя, Пол)")
            return

        # Валидация роста и веса
        height = self._validate_height()
        weight = self._validate_weight()

        if height is None or weight is None:
            return

        # Валидация возраста
        birth_date_obj = self._validate_birth_date()
        if birth_date_obj is None:
            return

        # Расчет и валидация возраста
        age = self._calculate_age(birth_date_obj)
        if not self._validate_age(age):
            return

        # Сбор данных и вызов callback
        self._collect_and_save_data(height, weight, birth_date_obj)

    def _validate_height(self):
        """Проверяет корректность введенного роста.

        Returns:
            float: Корректное значение роста или None при ошибке.
        """
        try:
            height = float(self.spin_height.get())
            if not (MIN_HEIGHT_CM <= height <= MAX_HEIGHT_CM):
                messagebox.showerror("Ошибка ввода",
                                     f"Рост ({height} см) выходит за биологические пределы "
                                     f"({MIN_HEIGHT_CM}-{MAX_HEIGHT_CM} см).")
                return None
            return height
        except ValueError:
            messagebox.showerror("Ошибка", "Рост должен быть числом")
            return None

    def _validate_weight(self):
        """Проверяет корректность введенного веса.

        Returns:
            float: Корректное значение веса или None при ошибке.
        """
        try:
            weight = float(self.spin_weight.get())
            if not (MIN_WEIGHT_KG <= weight <= MAX_WEIGHT_KG):
                messagebox.showerror("Ошибка ввода",
                                     f"Вес ({weight} кг) выходит за биологические пределы "
                                     f"({MIN_WEIGHT_KG}-{MAX_WEIGHT_KG} кг).")
                return None
            return weight
        except ValueError:
            messagebox.showerror("Ошибка", "Вес должен быть числом")
            return None

    def _validate_birth_date(self):
        """Проверяет корректность введенной даты рождения.

        Returns:
            datetime.date: Объект даты рождения или None при ошибке.
        """
        try:
            birth_date_obj = self.date_entry.get_date()
            today = date.today()

            # Проверяем, что дата рождения не в будущем
            if birth_date_obj > today:
                messagebox.showerror("Ошибка ввода",
                                     "Дата рождения не может быть в будущем.")
                return None
            return birth_date_obj
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Некорректная дата рождения.")
            return None

    def _calculate_age(self, birth_date):
        """Вычисляет возраст пациента по дате рождения.

        Args:
            birth_date: Дата рождения пациента как datetime.date объект.

        Returns:
            int: Возраст пациента в годах.
        """
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def _validate_age(self, age):
        """Проверяет корректность возраста пациента.

        Args:
            age: Возраст пациента в годах.

        Returns:
            bool: True если возраст корректен, False иначе.
        """
        if not (MIN_AGE_YEARS <= age <= MAX_AGE_YEARS):
            messagebox.showerror("Ошибка ввода",
                                 f"Возраст пациента ({age} лет) выходит за биологические пределы "
                                 f"({MIN_AGE_YEARS}-{MAX_AGE_YEARS} лет).")
            return False
        return True

    def _collect_and_save_data(self, height, weight, birth_date):
        """Собирает данные из формы и вызывает callback.

        Args:
            height: Рост пациента в сантиметрах.
            weight: Вес пациента в килограммах.
            birth_date: Дата рождения пациента.
        """
        data = {
            "last_name": self.entry_last_name.get(),
            "first_name": self.entry_first_name.get(),
            "middle_name": self.entry_middle_name.get(),
            "gender": self.combo_gender.get(),
            "birth_date": birth_date,
            "height": height,
            "weight": weight
        }

        self.on_save_callback(data, self.patient)
        self.destroy()