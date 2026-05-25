"""Common base classes for laboratory work 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LabTask(ABC):
    """Base class for every interactive laboratory task."""

    version = "1.0"
    task_counter = 0
    task_name = "Base task"

    def __init__(self) -> None:
        """Register the created task instance."""
        type(self).task_counter += 1

    @classmethod
    def get_task_name(cls) -> str:
        """Return the task name."""
        return cls.task_name

    @staticmethod
    def pause_message() -> str:
        """Return a pause message."""
        return "Press Enter to continue..."

    @abstractmethod
    def run(self, **kwargs: object) -> None:
        """Run the selected task."""


class NamedEntity:
    """Base entity with a validated name property."""

    created_count = 0

    def __init__(self, name: str) -> None:
        """Store the entity name after validation."""
        type(self).created_count += 1
        self._name = ""
        self.name = name

    @property
    def name(self) -> str:
        """Return the entity name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Validate and set the entity name."""
        clean_value = value.strip()
        if not clean_value:
            raise ValueError("Name cannot be empty.")
        self._name = clean_value

    def __str__(self) -> str:
        """Return a readable string for the entity."""
        return self.name
