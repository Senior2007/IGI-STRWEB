"""Input and output helpers with validation."""


def read_int(prompt: str) -> int:
    """Read one integer from user input with retry on invalid data."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def read_float(prompt: str) -> float:
    """Read one float value from user input with retry on invalid data."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите вещественное число.")


def read_positive_int(prompt: str) -> int:
    """Read a positive integer from user input."""
    while True:
        value = read_int(prompt)
        if value > 0:
            return value
        print("Ошибка: число должно быть больше 0.")


def ask_continue() -> bool:
    """Ask user if they want to continue in the application."""
    while True:
        answer = input("Продолжить выполнение? (y/n): ").strip().lower()
        if answer in {"y", "yes", "да"}:
            return True
        if answer in {"n", "no", "нет"}:
            return False
        print("Введите y/yes (да) или n/no (нет).")
