"""Pandas models for task 6.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-27
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import NamedEntity
from app.common.mixins import PositiveValueMixin, PrettyReprMixin


class DatasetInfo(NamedEntity, PrettyReprMixin):
    """Store dataset metadata for task 6."""

    def __init__(self, name: str, file_path: Path) -> None:
        """Store the dataset name and path."""
        super().__init__(name)
        self.file_path = file_path

    @property
    def suffix(self) -> str:
        """Return the dataset file suffix."""
        return self.file_path.suffix.lower()


class PercentileThresholds(PositiveValueMixin, PrettyReprMixin):
    """Store low and high percentile values."""

    def __init__(self, low_percentile: float, high_percentile: float) -> None:
        """Store both percentile thresholds."""
        self.low_percentile = float(low_percentile)
        self.high_percentile = float(high_percentile)

    def __str__(self) -> str:
        """Return a readable description for the thresholds."""
        return f"low={self.low_percentile:.4f}, high={self.high_percentile:.4f}"
