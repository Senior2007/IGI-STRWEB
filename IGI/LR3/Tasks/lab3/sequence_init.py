"""Sequence initialization helpers for list tasks."""

import random

from lab3.io_utils import read_float


def init_by_generator(sequence: list[float], size: int, left: float = -10.0, right: float = 10.0) -> list[float]:
    """Fill given sequence with random float values and return it."""
    sequence.clear()
    sequence.extend(random.uniform(left, right) for _ in range(size))
    return sequence


def init_by_user_input(sequence: list[float], size: int) -> list[float]:
    """Fill given sequence from user input and return it."""
    sequence.clear()
    for idx in range(size):
        sequence.append(read_float(f"Элемент [{idx}]: "))
    return sequence
