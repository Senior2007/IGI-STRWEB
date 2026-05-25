"""Business logic for task 1.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from app.task1.data_source import DEFAULT_STUDENTS
from app.task1.models import GTOStudent


class GTORegistry:
    """Store students and compute reports for task 1."""

    def __init__(self, students: dict[str, GTOStudent]) -> None:
        """Store the internal student dictionary."""
        self._students = students

    @property
    def students(self) -> dict[str, GTOStudent]:
        """Return the student dictionary."""
        return self._students

    @classmethod
    def from_seed_data(cls) -> "GTORegistry":
        """Create a registry from the predefined dictionary."""
        students = {
            name: GTOStudent(name, data["sprint_seconds"], data["long_jump_cm"])
            for name, data in DEFAULT_STUDENTS.items()
        }
        return cls(students)

    def failed_students(self) -> list[GTOStudent]:
        """Return all students who failed at least one norm."""
        return [student for student in self.students.values() if not student.passed_all]

    def passed_count(self) -> int:
        """Return the number of students who passed both norms."""
        return sum(1 for student in self.students.values() if student.passed_all)

    def top_three(self) -> list[GTOStudent]:
        """Return the three best students by combined rating score."""
        return sorted(self.students.values(), reverse=True)[:3]

    def find_student(self, student_name: str) -> GTOStudent | None:
        """Find a student by full name."""
        return self.students.get(student_name.strip())
