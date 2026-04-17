"""Series models for task 3.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.common.mixins import DictMixin, PositiveValueMixin, PrettyReprMixin


@dataclass(slots=True)
class SeriesPoint:
    """Store one row of the computed series table."""

    x: float
    series_value: float
    terms_used: int
    math_value: float
    epsilon: float

    @property
    def absolute_error(self) -> float:
        """Return the absolute difference between two function values."""
        return abs(self.math_value - self.series_value)


class SeriesFunction(ABC, PositiveValueMixin, PrettyReprMixin):
    """Base class for a function represented by a series."""

    variant_number = 7
    title = "Series function"
    created_count = 0

    def __init__(self, epsilon: float) -> None:
        """Store the epsilon value for the series expansion."""
        type(self).created_count += 1
        self._epsilon = 0.0
        self.epsilon = epsilon

    @property
    def epsilon(self) -> float:
        """Return the epsilon value."""
        return self._epsilon

    @epsilon.setter
    def epsilon(self, value: float) -> None:
        """Validate and set epsilon."""
        self._epsilon = self.validate_positive(float(value), "Epsilon")

    @classmethod
    def get_title(cls) -> str:
        """Return the class title."""
        return cls.title

    @abstractmethod
    def math_value(self, x_value: float) -> float:
        """Return the exact function value from the math module."""

    @abstractmethod
    def calculate_point(self, x_value: float) -> SeriesPoint:
        """Return one computed row for the given x value."""


class CosineSeries(SeriesFunction, DictMixin):
    """Variant 7 series for the cosine function."""

    title = "cos(x) = sum((-1)^n * x^(2n) / (2n)!)"

    def math_value(self, x_value: float) -> float:
        """Return the exact cosine value."""
        return math.cos(x_value)

    def calculate_point(self, x_value: float) -> SeriesPoint:
        """Calculate one row of the cosine series table."""
        term = 1.0
        series_sum = term
        terms_used = 1
        index = 1

        while True:
            term *= -1 * x_value * x_value / ((2 * index - 1) * (2 * index))
            if abs(term) < self.epsilon:
                break
            series_sum += term
            terms_used += 1
            index += 1

        return SeriesPoint(
            x=x_value,
            series_value=series_sum,
            terms_used=terms_used,
            math_value=self.math_value(x_value),
            epsilon=self.epsilon,
        )

    def to_dict(self) -> dict[str, object]:
        """Return the main class parameters as a dictionary."""
        return {"variant": self.variant_number, "title": self.title, "epsilon": self.epsilon}

    def __str__(self) -> str:
        """Return a readable function description."""
        return f"Variant {self.variant_number}: {self.title}"
