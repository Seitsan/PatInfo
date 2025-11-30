import json
import os
from faker import Faker
import random
from src.models.patient import Patient


class DataManager:
    """
    Класс для управления данными: загрузка, сохранение, генерация.
    """
    FILE_PATH = "patients_data.json"

    def __init__(self, get_path_func):
        self.fake = Faker('ru_RU')
        self.get_path = get_path_func
        self.FILE_PATH = self.get_path("resources/data/patients_data.json")

    def load_patients(self):
        """Загрузка пациентов из JSON. Если файла нет, генерирует новые данные."""
        if not os.path.exists(self.FILE_PATH):
            return self.generate_initial_data()

        try:
            with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Patient.from_dict(p) for p in data]
        except (json.JSONDecodeError, IOError):
            return self.generate_initial_data()

    def save_patients(self, patients):
        """Сохранение списка пациентов в JSON."""
        data = [p.to_dict() for p in patients]
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def generate_initial_data(self, count=15):
        """Генерация фейковых данных."""
        patients = []
        for _ in range(count):
            gender = random.choice(['М', 'Ж'])
            if gender == 'М':
                first_name = self.fake.first_name_male()
                last_name = self.fake.last_name_male()
                middle_name = self.fake.middle_name_male()
            else:
                first_name = self.fake.first_name_female()
                last_name = self.fake.last_name_female()
                middle_name = self.fake.middle_name_female()

            birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=90)
            height = random.randint(150, 200)
            weight = random.randint(50, 120)

            patients.append(Patient(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                gender=gender,
                birth_date=birth_date,
                height=height,
                weight=weight
            ))

        self.save_patients(patients)
        return patients