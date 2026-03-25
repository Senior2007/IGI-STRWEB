"""Main menu and task dispatcher."""

from lab3.io_utils import ask_continue, read_int
from lab3.meta import APP_VERSION, LAB_TITLE
from lab3.task1_series import run_task_1
from lab3.task2_loop import run_task_2
from lab3.task3_text import run_task_3
from lab3.task4_fixed_text import run_task_4
from lab3.task5_list import run_task_5


def print_menu() -> None:
    """Print available menu items."""
    print("Выберите задание:")
    print("1 - Задание 1 (ряд cos(x))")
    print("2 - Задание 2 (цикл, числа < 10)")
    print("3 - Задание 3 (строчные буквы и цифры)")
    print("4 - Задание 4 (анализ фиксированного текста)")
    print("5 - Задание 5 (обработка списка)")
    print("0 - Выход")


def run_application() -> None:
    """Run app loop with input validation and repeated execution."""
    print(f"{LAB_TITLE}\nVersion: {APP_VERSION}\n")

    handlers = {
        1: run_task_1,
        2: run_task_2,
        3: run_task_3,
        4: run_task_4,
        5: run_task_5,
    }

    try:
        while True:
            print_menu()
            choice = read_int("Введите номер задания: ")
            if choice == 0:
                print("Завершение программы.")
                return

            handler = handlers.get(choice)
            if handler is None:
                print("Ошибка: выберите номер от 0 до 5.\n")
                continue

            handler()
            if not ask_continue():
                print("Завершение программы.")
                return
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
    except EOFError:
        print("\nВвод завершен.")
