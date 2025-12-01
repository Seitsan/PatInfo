import uuid
from datetime import date, datetime


class Patient:
    """Модель данных пациента медицинской информационной системы.

    Класс представляет пациента с основными антропометрическими данными,
    предоставляет методы для расчета производных показателей (возраст, ИМТ)
    и поддерживает сериализацию/десериализацию для хранения в JSON.

    Attributes:
        id: Уникальный идентификатор пациента (UUID).
        last_name: Фамилия пациента.
        first_name: Имя пациента.
        middle_name: Отчество пациента.
        gender: Пол пациента ('М' или 'Ж').
        birth_date: Дата рождения пациента (datetime.date).
        height: Рост пациента в сантиметрах (float).
        weight: Вес пациента в килограммах (float).
    """

    def __init__(self, last_name, first_name, middle_name, gender,
                 birth_date, height, weight, patient_id=None):
        """Инициализирует объект пациента.

        Args:
            last_name: Фамилия пациента.
            first_name: Имя пациента.
            middle_name: Отчество пациента.
            gender: Пол пациента. Допустимые значения: 'М' или 'Ж'.
            birth_date: Дата рождения. Может быть строкой в формате "dd-mm-yyyy"
                или объектом datetime.date.
            height: Рост пациента в сантиметрах. Может быть числом или строкой.
            weight: Вес пациента в килограммах. Может быть числом или строкой.
            patient_id: Уникальный идентификатор пациента. Если не указан,
                генерируется новый UUID.

        Raises:
            ValueError: Если строка birth_date имеет неверный формат.
            TypeError: Если height или weight не могут быть преобразованы в float.
        """
        self.id = patient_id or str(uuid.uuid4())
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.gender = gender

        # Обработка даты рождения
        if isinstance(birth_date, str):
            self.birth_date = datetime.strptime(birth_date, "%d-%m-%Y").date()
        else:
            self.birth_date = birth_date

        self.height = float(height)
        self.weight = float(weight)

    @property
    def age(self):
        """Рассчитывает возраст пациента на текущую дату.

        Вычисляет точный возраст с учетом месяца и дня рождения.
        Использует алгоритм, корректно обрабатывающий граничные случаи.

        Returns:
            int: Возраст пациента в полных годах.

        Example:
            >>> patient = Patient(..., birth_date=date(1990, 5, 15))
            >>> # Если сегодня 2024-05-14, возраст будет 33
            >>> # Если сегодня 2024-05-15, возраст будет 34
        """
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    @property
    def bmi(self):
        """Рассчитывает индекс массы тела (ИМТ).

        Использует стандартную формулу ВОЗ: BMI = вес (кг) / (рост (м))².
        Рост конвертируется из сантиметров в метры.

        Returns:
            float: Значение ИМТ, округленное до двух десятичных знаков.
                Возвращает 0, если рост меньше или равен 0.

        Note:
            Формула ИМТ применима для взрослых в возрасте 18-65 лет.
            Для детей, беременных и пожилых требуются другие формулы.
        """
        if self.height <= 0:
            return 0
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)

    @property
    def bmi_category(self):
        """Определяет категорию ИМТ согласно классификации ВОЗ.

        Категории:
        - Недостаточный вес: ИМТ < 18.5
        - Нормальный вес: 18.5 ≤ ИМТ < 25
        - Избыточный вес: 25 ≤ ИМТ < 30
        - Ожирение: ИМТ ≥ 30

        Returns:
            str: Текстовая категория ИМТ:
                "Недостаточный вес", "Норма", "Избыточный вес" или "Ожирение".

        Note:
            Классификация может различаться для азиатского населения и
            профессиональных спортсменов с развитой мускулатурой.
        """
        bmi = self.bmi
        if bmi < 18.5:
            return "Недостаточный вес"
        elif 18.5 <= bmi < 25:
            return "Норма"
        elif 25 <= bmi < 30:
            return "Избыточный вес"
        else:
            return "Ожирение"

    def to_dict(self):
        """Сериализует объект пациента в словарь для JSON.

        Преобразует все атрибуты пациента в формат, пригодный для сериализации
        в JSON. Дата рождения преобразуется в строковый формат.

        Returns:
            dict: Словарь с данными пациента:
                - id (str): Уникальный идентификатор
                - last_name (str): Фамилия
                - first_name (str): Имя
                - middle_name (str): Отчество
                - gender (str): Пол
                - birth_date (str): Дата рождения в формате "dd-mm-yyyy"
                - height (float): Рост в см
                - weight (float): Вес в кг

        Note:
            Формат даты выбран как "dd-mm-yyyy" для лучшей читаемости
            в русскоязычной среде.
        """
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "gender": self.gender,
            "birth_date": self.birth_date.strftime("%d-%m-%Y"),
            "height": self.height,
            "weight": self.weight
        }

    @classmethod
    def from_dict(cls, data):
        """Десериализует объект пациента из словаря.

        Фабричный метод для создания экземпляра Patient из словаря,
        полученного при десериализации JSON.

        Args:
            data: Словарь с данными пациента. Ожидаются ключи:
                - id (str, опционально): Уникальный идентификатор
                - last_name (str): Фамилия
                - first_name (str): Имя
                - middle_name (str): Отчество
                - gender (str): Пол
                - birth_date (str): Дата рождения в формате "dd-mm-yyyy"
                - height (float/int/str): Рост в см
                - weight (float/int/str): Вес в кг

        Returns:
            Patient: Новый экземпляр класса Patient с данными из словаря.

        Raises:
            KeyError: Если отсутствуют обязательные поля в словаре.
            ValueError: Если birth_date имеет неверный формат.

        Example:
            >>> data = {
            ...     "last_name": "Иванов",
            ...     "first_name": "Иван",
            ...     "middle_name": "Иванович",
            ...     "gender": "М",
            ...     "birth_date": "15-05-1990",
            ...     "height": 180,
            ...     "weight": 75
            ... }
            >>> patient = Patient.from_dict(data)
        """
        return cls(
            patient_id=data.get("id"),
            last_name=data.get("last_name"),
            first_name=data.get("first_name"),
            middle_name=data.get("middle_name"),
            gender=data.get("gender"),
            birth_date=data.get("birth_date"),
            height=data.get("height"),
            weight=data.get("weight")
        )