"""Task 1: cos(x) via power series."""

import math

from lab3.decorators import log_call
from lab3.io_utils import read_float

MAX_ITERATIONS = 500


def my_cos(x: float, eps: float, max_iterations: int = MAX_ITERATIONS) -> tuple[float, int]:
    """Return cos(x) approximation and number of summed terms."""
    two_pi = 2 * math.pi
    x = x % two_pi
    term = 1.0
    result = 0.0
    terms_count = 0
    n = 0

    while n < max_iterations and abs(term) >= eps:
        result += term
        terms_count += 1
        n += 1
        term *= -1.0 * x * x / ((2 * n - 1) * (2 * n))

    return result, terms_count


@log_call
def run_task_1() -> None:
    """Run interactive workflow for task 1."""
    print("Задание 1: F(x) = cos(x) через степенной ряд.")
    x = read_float("Введите x: ")

    while True:
        eps = read_float("Введите eps (> 0): ")
        if eps > 0:
            break
        print("Ошибка: eps должен быть больше 0.")

    f_x, n = my_cos(x, eps)
    print(f"x = {x}")
    print(f"F(x) = {f_x}")
    print(f"n = {n}")
    print(f"Math F(x) = {math.cos(x)}")
