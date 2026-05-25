"""Analysis classes for task 5.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class VarianceCalculator(ABC):
    """Abstract variance calculator."""

    @abstractmethod
    def calculate(self, values: np.ndarray) -> float:
        """Calculate variance for the given values."""


class NumpyVarianceCalculator(VarianceCalculator):
    """Variance calculator based on NumPy."""

    def calculate(self, values: np.ndarray) -> float:
        """Calculate variance with numpy.var."""
        return float(np.var(values))


class ManualVarianceCalculator(VarianceCalculator):
    """Variance calculator based on the mathematical formula."""

    def calculate(self, values: np.ndarray) -> float:
        """Calculate variance manually."""
        mean_value = float(np.mean(values))
        return float(sum((float(value) - mean_value) ** 2 for value in values) / len(values))


class MatrixAnalyzer:
    """Analyze the secondary diagonal of a matrix."""

    def __init__(self, values: np.ndarray) -> None:
        """Store the analyzed values."""
        self.values = values

    def minimum_value(self) -> int:
        """Return the minimum secondary diagonal value."""
        return int(np.min(self.values))

    def variance_report(self) -> tuple[float, float]:
        """Return variance values calculated in two ways."""
        numpy_value = round(NumpyVarianceCalculator().calculate(self.values), 2)
        manual_value = round(ManualVarianceCalculator().calculate(self.values), 2)
        return numpy_value, manual_value

    def numpy_demo(self, matrix: np.ndarray) -> str:
        """Return a short demonstration of NumPy operations."""
        zeros_matrix = np.zeros((2, 2), dtype=int)
        ones_matrix = np.ones((2, 2), dtype=int)
        first_row = matrix[0, :]
        absolute_matrix = np.abs(matrix)
        return (
            f"array() created matrix shape: {matrix.shape}\n"
            f"zeros():\n{zeros_matrix}\n"
            f"ones():\n{ones_matrix}\n"
            f"First row slice: {first_row}\n"
            f"Element-wise abs():\n{absolute_matrix}"
        )
