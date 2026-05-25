"""Serializers for task 1.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import csv
import pickle
from abc import ABC, abstractmethod
from pathlib import Path

from app.task1.models import GTOStudent


class StudentStorage(ABC):
    """Abstract storage for student data."""

    extension = ""

    @abstractmethod
    def save(self, file_path: Path, students: dict[str, GTOStudent]) -> None:
        """Save student data to a file."""

    @abstractmethod
    def load(self, file_path: Path) -> dict[str, GTOStudent]:
        """Load student data from a file."""


class CsvStudentStorage(StudentStorage):
    """CSV serializer for student data."""

    extension = ".csv"

    def save(self, file_path: Path, students: dict[str, GTOStudent]) -> None:
        """Write student data to a CSV file."""
        with file_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "sprint_seconds", "long_jump_cm"])
            writer.writeheader()
            for student in students.values():
                writer.writerow(student.to_dict())

    def load(self, file_path: Path) -> dict[str, GTOStudent]:
        """Read student data from a CSV file."""
        result: dict[str, GTOStudent] = {}
        with file_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = GTOStudent.from_dict(row)
                result[student.name] = student
        return result


class PickleStudentStorage(StudentStorage):
    """Pickle serializer for student data."""

    extension = ".pkl"

    def save(self, file_path: Path, students: dict[str, GTOStudent]) -> None:
        """Write student data to a pickle file."""
        raw_data = {name: student.to_dict() for name, student in students.items()}
        with file_path.open("wb") as file:
            pickle.dump(raw_data, file)

    def load(self, file_path: Path) -> dict[str, GTOStudent]:
        """Read student data from a pickle file."""
        with file_path.open("rb") as file:
            raw_data = pickle.load(file)
        return {name: GTOStudent.from_dict(data) for name, data in raw_data.items()}
