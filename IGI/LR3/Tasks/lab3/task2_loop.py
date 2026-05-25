"""Task 2: count values less than 10 until sentinel 100."""

from lab3.decorators import log_call
from lab3.io_utils import read_int


def count_less_than_ten() -> int:
    """Read integers until 100 is entered and count values less than 10."""
    count = 0
    while True:
        value = read_int("Введите целое число (100 для завершения): ")
        if value == 100:
            break
        if value < 10:
            count += 1
    return count


@log_call
def run_task_2() -> None:
    """Run interactive workflow for task 2."""
    print("Задание 2: подсчитать числа < 10, окончание ввода: 100.")
    count = count_less_than_ten()
    print(f"Количество чисел, меньших 10 = {count}")
