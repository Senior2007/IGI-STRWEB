"""Task 3: count lowercase letters and digits in input text."""

from lab3.decorators import log_call


def count_lowercase_and_digits(text: str) -> tuple[int, int, int]:
    """Return counts of lowercase letters, digits and their total."""
    lowercase_count = sum(1 for ch in text if ch.islower())
    digits_count = sum(1 for ch in text if ch.isdigit())
    return lowercase_count, digits_count, lowercase_count + digits_count


@log_call
def run_task_3() -> None:
    """Run interactive workflow for task 3."""
    print("Задание 3: подсчет строчных букв и цифр.")
    text = input("Введите строку: ")
    lower_count, digits_count, total = count_lowercase_and_digits(text)
    print(f"Строчных букв: {lower_count}")
    print(f"Цифр: {digits_count}")
    print(f"Общее число: {total}")
