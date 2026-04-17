"""Console interface for task 5.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from app.common.base import LabTask
from app.common.io_utils import InputHelper
from app.task5.analytics import MatrixAnalyzer
from app.task5.models import RandomIntMatrix


class Task5Runner(LabTask):
    """Interactive runner for task 5."""

    task_name = "Task 5 - NumPy matrix"

    def run(self, **kwargs: object) -> None:
        """Generate a matrix and analyze the secondary diagonal."""
        rows = InputHelper.ask_int("Enter the number of rows n: ", minimum=1)
        columns = InputHelper.ask_int("Enter the number of columns m: ", minimum=1)
        low = InputHelper.ask_int("Enter the minimum random value: ")
        high = InputHelper.ask_int("Enter the maximum random value: ")
        while high < low:
            print("The maximum value cannot be smaller than the minimum value.")
            high = InputHelper.ask_int("Enter the maximum random value: ")

        matrix_wrapper = RandomIntMatrix(rows, columns, low, high)
        analyzer = MatrixAnalyzer(matrix_wrapper.secondary_diagonal)
        numpy_variance, manual_variance = analyzer.variance_report()

        print("\nGenerated matrix A:")
        print(matrix_wrapper)
        print("\nSecondary diagonal:")
        print(matrix_wrapper.secondary_diagonal)
        print(f"Minimum element on the secondary diagonal: {analyzer.minimum_value()}")
        print(f"Variance by numpy.var(): {numpy_variance:.2f}")
        print(f"Variance by the formula: {manual_variance:.2f}")
        print("\nSmall NumPy demonstration:")
        print(analyzer.numpy_demo(matrix_wrapper.matrix))
