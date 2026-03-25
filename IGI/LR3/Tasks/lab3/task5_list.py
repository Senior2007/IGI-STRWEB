"""Task 5: processing a list of real numbers."""

from lab3.decorators import log_call
from lab3.io_utils import read_float, read_int, read_positive_int
from lab3.sequence_init import init_by_generator, init_by_user_input


def count_positive_greater_than_c(values: list[float], c_value: float) -> int:
    """Count positive list elements that are greater than C."""
    return sum(1 for item in values if item > 0 and item > c_value)


def product_after_max_abs(values: list[float]) -> float | None:
    """Return product of items after max-by-absolute-value element, or None if no such items."""
    if not values:
        return None

    max_abs_index = max(range(len(values)), key=lambda index: abs(values[index]))
    tail = values[max_abs_index + 1 :]

    if not tail:
        return None

    product = 1.0
    for item in tail:
        product *= item
    return product


def choose_initialization_method() -> int:
    """Ask user to choose list initialization method."""
    print("Выберите способ инициализации списка:")
    print("1 - генератор случайных чисел")
    print("2 - ввод вручную")
    while True:
        method = read_int("Ваш выбор (1/2): ")
        if method in (1, 2):
            return method
        print("Ошибка: допустимы только 1 или 2.")


@log_call
def run_task_5() -> None:
    """Run interactive workflow for task 5."""
    print("Задание 5: обработка вещественного списка.")
    size = read_positive_int("Введите размерность списка: ")
    values: list[float] = []

    method = choose_initialization_method()
    if method == 1:
        left = read_float("Левая граница генерации: ")
        right = read_float("Правая граница генерации: ")
        while right <= left:
            print("Ошибка: правая граница должна быть больше левой.")
            left = read_float("Левая граница генерации: ")
            right = read_float("Правая граница генерации: ")
        init_by_generator(values, size, left, right)
    else:
        init_by_user_input(values, size)

    c_value = read_float("Введите значение C: ")
    count = count_positive_greater_than_c(values, c_value)
    product = product_after_max_abs(values)

    print("\nСписок:")
    for value in values:
        print(value, end=" ")
    print(f"\nКоличество положительных элементов > C: {count}")
    if product is None:
        print("После максимального по модулю элемента нет элементов для произведения.")
    else:
        print(f"Произведение элементов после максимального по модулю: {product}")
