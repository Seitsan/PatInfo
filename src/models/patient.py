import uuid
from datetime import date, datetime


class Patient:
    """
    Класс, представляющий модель данных пациента.
    """

    def __init__(self, last_name, first_name, middle_name, gender,
                 birth_date, height, weight, patient_id=None):
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
        """Расчет возраста на текущую дату."""
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    @property
    def bmi(self):
        """Расчет ИМТ: вес / (рост/100)²."""
        if self.height <= 0:
            return 0
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)

    @property
    def bmi_category(self):
        """Категория ИМТ: недостаточный, нормальный, избыточный, ожирение."""
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
        """Преобразование объекта в словарь для JSON."""
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
        """Создание объекта из словаря."""
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
