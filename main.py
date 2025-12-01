import sys
import os
import tkinter as tk
from tkinter import messagebox


def get_resource_path(relative_path):
    """Определяет абсолютный путь к ресурсу с учетом режима выполнения.

    Функция корректно работает в двух режимах:
    1. Режим разработки: используется обычная файловая структура проекта
    2. Режим исполняемого файла PyInstaller: ресурсы находятся в временной
       директории _MEIPASS

    Args:
        relative_path: Относительный путь к ресурсу от директории 'src'.
            Например: 'resources/data/patients_data.json'

    Returns:
        str: Абсолютный путь к указанному ресурсу.

    Raises:
        OSError: Если базовый путь не может быть определен.

    Note:
        PyInstaller создает временную директорию _MEIPASS при запуске
        исполняемого файла, куда помещаются все ресурсы.
    """
    # Определяем базовый путь
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, 'src', relative_path)


def ensure_resource_directories():
    """Проверяет существование и создает необходимые директории ресурсов.

    Функция гарантирует наличие обязательных директорий для работы приложения:
    - resources/data: для хранения данных пациентов
    - resources/icons: для хранения иконок интерфейса

    Если директории не существуют, они создаются автоматически с выводом
    соответствующего сообщения в консоль.

    Raises:
        OSError: Если не удается создать необходимые директории
            из-за недостаточных прав доступа или других системных ошибок.

    Note:
        В режиме PyInstaller эта функция может не выполнять создание директорий,
        так как ресурсы находятся в read-only временной директории.
    """
    data_dir = get_resource_path('resources/data')
    icons_dir = get_resource_path('resources/icons')

    # Создаем папки, если они не существуют
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Создана папка: {data_dir}")
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"Создана папка: {icons_dir}")


# Инициализация структуры директорий при импорте модуля
ensure_resource_directories()

# Добавление текущей директории в sys.path для корректного импорта модулей
current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Импорт основных модулей приложения с обработкой ошибок
try:
    from src.models.data_manager import DataManager
    from src.gui.main_window import MainWindow
except ImportError as e:
    print(f"Критическая ошибка импорта: {e}")
    print(f"Текущий sys.path: {sys.path}")
    sys.exit(1)


def main():
    """Точка входа в приложение PatInfo.

    Основная функция инициализирует приложение в следующем порядке:
    1. Создает экземпляр DataManager для управления данными
    2. Загружает список пациентов из хранилища
    3. Создает и запускает главное окно приложения
    4. Обрабатывает критические ошибки с пользовательским интерфейсом

    Raises:
        SystemExit: Приложение завершается с кодом 1 при критических ошибках.
        Exception: Все необработанные исключения перехватываются и логируются.

    Note:
        Функция использует двойной механизм обработки ошибок:
        - GUI-сообщения для пользователя (если интерфейс доступен)
        - Консольный вывод для разработчика (при невозможности показа GUI)
    """
    try:
        # Инициализация менеджера данных
        data_manager = DataManager(get_resource_path)

        # Загрузка данных пациентов
        patients = data_manager.load_patients()

        # Создание и запуск главного окна приложения
        app = MainWindow(data_manager, patients, get_resource_path)
        app.mainloop()

    except Exception as e:
        # Попытка показать ошибку через GUI
        try:
            tk.messagebox.showerror("Ошибка", f"Произошла ошибка при запуске: {e}")
        except tk.TclError:
            # Резервный вывод в консоль, если GUI недоступен
            print(f"Произошла ошибка при запуске: {e}")
        # Завершение приложения с кодом ошибки
        sys.exit(1)


if __name__ == "__main__":
    """Запуск приложения при прямом выполнении файла."""
    main()