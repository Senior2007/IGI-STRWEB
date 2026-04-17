"""NumPy models for task 5.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import numpy as np

from app.common.mixins import PositiveValueMixin, PrettyReprMixin


class MatrixBase(PositiveValueMixin, PrettyReprMixin):
    """Base matrix wrapper."""

    def __init__(self, rows: int, columns: int) -> None:
        """Store the matrix shape."""
        self._rows = int(self.validate_positive(rows, "Rows"))
        self._columns = int(self.validate_positive(columns, "Columns"))

    @property
    def rows(self) -> int:
        """Return the number of rows."""
        return self._rows

    @property
    def columns(self) -> int:
        """Return the number of columns."""
        return self._columns


class RandomIntMatrix(MatrixBase):
    """Generate a random integer matrix with NumPy."""

    created_count = 0

    def __init__(self, rows: int, columns: int, low: int, high: int) -> None:
        """Generate the matrix values."""
        super().__init__(rows, columns)
        type(self).created_count += 1
        self.low = low
        self.high = high
        self._matrix = np.random.randint(low, high + 1, size=(self.rows, self.columns))

    @property
    def matrix(self) -> np.ndarray:
        """Return the NumPy matrix."""
        return self._matrix

    @property
    def secondary_diagonal(self) -> np.ndarray:
        """Return the secondary diagonal values."""
        indices = range(min(self.rows, self.columns))
        return np.array([self.matrix[index, self.columns - 1 - index] for index in indices])

    def __getitem__(self, item: object) -> np.ndarray:
        """Allow index-based access to the underlying matrix."""
        return self.matrix[item]

    def __str__(self) -> str:
        """Return a readable string for the matrix."""
        return str(self.matrix)
