import json
import os
from faker import Faker
import random
from src.models.patient import Patient


class DataManager:
    """Менеджер данных для работы с информацией о пациентах.

    Класс предоставляет функциональность для загрузки, сохранения и генерации
    данных о пациентах. Использует JSON-файл для хранения данных и библиотеку
    Faker для создания демонстрационных данных при отсутствии реальных.

    Attributes:
        FILE_PATH: Классовая константа с именем файла по умолчанию.
        fake: Экземпляр Faker для генерации фейковых данных.
        get_path: Функция для получения абсолютных путей к ресурсам.
    """

    FILE_PATH = "patients_data.json"

    def __init__(self, get_path_func):
        """Инициализирует менеджер данных.

        Args:
            get_path_func: Функция для получения абсолютных путей к ресурсам.
                Должна принимать относительный путь и возвращать абсолютный.
        """
        self.fake = Faker('ru_RU')
        self.get_path = get_path_func
        self.FILE_PATH = self.get_path("resources/data/patients_data.json")

    def load_patients(self):
        """Загружает список пациентов из JSON-файла.

        Попытка загрузки данных из файла по пути self.FILE_PATH.
        Если файл не существует или содержит некорректные данные,
        автоматически генерирует новые демонстрационные данные.

        Returns:
            list[Patient]: Список объектов Patient, загруженных из файла
                или сгенерированных автоматически.

        Raises:
            json.JSONDecodeError: Если файл содержит некорректный JSON.
            IOError: Если возникают проблемы с чтением файла.
            Note: Ошибки обрабатываются внутри метода с генерацией новых данных.
        """
        if not os.path.exists(self.FILE_PATH):
            return self.generate_initial_data()

        try:
            with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Patient.from_dict(p) for p in data]
        except (json.JSONDecodeError, IOError):
            return self.generate_initial_data()

    def save_patients(self, patients):
        """Сохраняет список пациентов в JSON-файл.

        Сериализует объекты Patient в словари и сохраняет их в формате JSON
        с человекочитаемым форматированием (отступы, поддержка кириллицы).

        Args:
            patients: Список объектов Patient для сохранения.

        Raises:
            IOError: Если возникают проблемы с записью в файл.
            TypeError: Если объекты Patient не могут быть сериализованы.
        """
        data = [p.to_dict() for p in patients]
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def generate_initial_data(self, count=15):
        """Генерирует демонстрационные данные о пациентах.

        Создает указанное количество фейковых пациентов с реалистичными
        данными, соответствующими русской локали. Данные автоматически
        сохраняются в файл для последующего использования.

        Генерируемые характеристики:
        - Пол (М/Ж) с равной вероятностью
        - ФИО в соответствии с полом и русскими традициями именования
        - Дата рождения в диапазоне 18-90 лет
        - Рост в диапазоне 150-200 см
        - Вес в диапазоне 50-120 кг

        Args:
            count: Количество генерируемых пациентов. По умолчанию 15.

        Returns:
            list[Patient]: Список сгенерированных объектов Patient.

        Note:
            После генерации данные автоматически сохраняются в файл
            с использованием метода save_patients.
        """
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