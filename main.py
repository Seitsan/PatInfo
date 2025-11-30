import sys
import os
import tkinter as tk
from tkinter import messagebox


def get_resource_path(relative_path):
    """
    Возвращает абсолютный путь к ресурсу, работая как в режиме разработки,
    так и в упакованном PyInstaller исполняемом файле.
    """
    # Определяем базовый путь
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, 'src', relative_path)


def ensure_resource_directories():
    """Проверяет и создает необходимые папки ресурсов."""
    data_dir = get_resource_path('resources/data')
    icons_dir = get_resource_path('resources/icons')

    # Создаем папки, если они не существуют
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Создана папка: {data_dir}")
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"Создана папка: {icons_dir}")


# Вызываем функцию для создания папок ресурсов
ensure_resource_directories()

current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from src.models.data_manager import DataManager
    from src.gui.main_window import MainWindow
except ImportError as e:
    print(f"Критическая ошибка импорта: {e}")
    print(f"Текущий sys.path: {sys.path}")
    sys.exit(1)


def main():
    try:
        data_manager = DataManager(get_resource_path)
        patients = data_manager.load_patients()

        app = MainWindow(data_manager, patients, get_resource_path)
        app.mainloop()

    except Exception as e:
        try:
            tk.messagebox.showerror("Ошибка", f"Произошла ошибка при запуске: {e}")
        except tk.TclError:
            print(f"Произошла ошибка при запуске: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
