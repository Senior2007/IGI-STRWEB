"""Reusable mixins for laboratory work 4 modules.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations


class DictMixin:
    """Provide a common protocol for dictionary conversion."""

    def to_dict(self) -> dict[str, object]:
        """Convert the current object to a plain dictionary."""
        raise NotImplementedError


class PrettyReprMixin:
    """Provide a compact developer-friendly representation."""

    def __repr__(self) -> str:
        """Return a simple representation based on instance fields."""
        attributes = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"


class PositiveValueMixin:
    """Provide validation helpers for positive numeric values."""

    @staticmethod
    def validate_positive(value: float, field_name: str) -> float:
        """Validate that a numeric value is positive."""
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than zero.")
        return value
