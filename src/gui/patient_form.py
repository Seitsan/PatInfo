import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, datetime

MIN_HEIGHT_CM = 50
MAX_HEIGHT_CM = 250
MIN_WEIGHT_KG = 1
MAX_WEIGHT_KG = 300
MIN_AGE_YEARS = 1
MAX_AGE_YEARS = 130

class PatientForm(tk.Toplevel):
    """
    Окно формы добавления или редактирования пациента.
    """

    def __init__(self, parent, on_save_callback, app_icon_photo, patient=None):
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.patient = patient

        self.iconphoto(True, app_icon_photo)

        self.title("Редактирование пациента" if patient else "Добавить пациента")
        self.geometry("450x550")
        self.configure(bg="#F5F5F5")

        self.create_form()


    def create_form(self):
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
        # Валидация обязательных полей
        if not all([self.entry_last_name.get(), self.entry_first_name.get(), self.combo_gender.get()]):
            messagebox.showerror("Ошибка", "Заполните обязательные поля (Фамилия, Имя, Пол)")
            return

        # Валидация роста и веса
        try:
            height = float(self.spin_height.get())
            weight = float(self.spin_weight.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Рост и вес должны быть числами")
            return

        if not (MIN_HEIGHT_CM <= height <= MAX_HEIGHT_CM):
            messagebox.showerror("Ошибка ввода",
                                 f"Рост ({height} см) выходит за биологические пределы "
                                 f"({MIN_HEIGHT_CM}-{MAX_HEIGHT_CM} см).")
            return

        if not (MIN_WEIGHT_KG <= weight <= MAX_WEIGHT_KG):
            messagebox.showerror("Ошибка ввода",
                                 f"Вес ({weight} кг) выходит за биологические пределы "
                                 f"({MIN_WEIGHT_KG}-{MAX_WEIGHT_KG} кг).")
            return

        # Валидация возраста
        try:
            birth_date_obj = self.date_entry.get_date()
        except ValueError:
            messagebox.showerror("Ошибка ввода",
                                 "Некорректная дата рождения.")
            return

        today = date.today()

        # Проверяем, что дата рождения не в будущем
        if birth_date_obj > today:
            messagebox.showerror("Ошибка ввода",
                                 "Дата рождения не может быть в будущем.")
            return

        # Расчет возраста
        age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))

        if not (MIN_AGE_YEARS <= age <= MAX_AGE_YEARS):
            messagebox.showerror("Ошибка ввода",
                                 f"Возраст пациента ({age} лет) выходит за биологические пределы "
                                 f"({MIN_AGE_YEARS}-{MAX_AGE_YEARS} лет).")
            return

        data = {
            "last_name": self.entry_last_name.get(),
            "first_name": self.entry_first_name.get(),
            "middle_name": self.entry_middle_name.get(),
            "gender": self.combo_gender.get(),
            "birth_date": self.date_entry.get_date(),
            "height": height,
            "weight": weight
        }

        self.on_save_callback(data, self.patient)
        self.destroy()
