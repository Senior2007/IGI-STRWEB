"""Models for task 1 GTO records.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from app.common.base import NamedEntity
from app.common.mixins import DictMixin, PositiveValueMixin, PrettyReprMixin


class SportsPerson(NamedEntity, PrettyReprMixin):
    """Base class for a person involved in sports activities."""

    def __init__(self, name: str) -> None:
        """Initialize the base sports person."""
        super().__init__(name)


class GTOStudent(SportsPerson, DictMixin, PositiveValueMixin):
    """Represent a student with GTO results for two disciplines."""

    sprint_norm_seconds = 15.0
    long_jump_norm_cm = 220

    def __init__(self, name: str, sprint_seconds: float, long_jump_cm: int) -> None:
        """Store validated GTO results for a student."""
        super().__init__(name)
        self._sprint_seconds = 0.0
        self._long_jump_cm = 0
        self.sprint_seconds = sprint_seconds
        self.long_jump_cm = long_jump_cm

    @property
    def sprint_seconds(self) -> float:
        """Return the 100 meter sprint result."""
        return self._sprint_seconds

    @sprint_seconds.setter
    def sprint_seconds(self, value: float) -> None:
        """Validate and set the sprint result."""
        validated = self.validate_positive(float(value), "Sprint result")
        self._sprint_seconds = validated

    @property
    def long_jump_cm(self) -> int:
        """Return the long jump result in centimeters."""
        return self._long_jump_cm

    @long_jump_cm.setter
    def long_jump_cm(self, value: int) -> None:
        """Validate and set the jump result."""
        validated = int(self.validate_positive(int(value), "Long jump result"))
        self._long_jump_cm = validated

    @property
    def passed_sprint(self) -> bool:
        """Return True when the sprint norm is passed."""
        return self.sprint_seconds <= self.sprint_norm_seconds

    @property
    def passed_jump(self) -> bool:
        """Return True when the long jump norm is passed."""
        return self.long_jump_cm >= self.long_jump_norm_cm

    @property
    def passed_all(self) -> bool:
        """Return True when both norms are passed."""
        return self.passed_sprint and self.passed_jump

    @property
    def rating_score(self) -> float:
        """Return a simple combined score for ranking students."""
        sprint_bonus = (self.sprint_norm_seconds - self.sprint_seconds) * 10
        jump_bonus = self.long_jump_cm - self.long_jump_norm_cm
        return round(sprint_bonus + jump_bonus, 2)

    def to_dict(self) -> dict[str, object]:
        """Convert the student to a plain dictionary."""
        return {
            "name": self.name,
            "sprint_seconds": self.sprint_seconds,
            "long_jump_cm": self.long_jump_cm,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "GTOStudent":
        """Create a student object from a dictionary."""
        return cls(
            name=str(data["name"]),
            sprint_seconds=float(data["sprint_seconds"]),
            long_jump_cm=int(data["long_jump_cm"]),
        )

    def __lt__(self, other: object) -> bool:
        """Compare students by rating score for sorting."""
        if not isinstance(other, GTOStudent):
            return NotImplemented
        return self.rating_score < other.rating_score

    def __str__(self) -> str:
        """Return a readable summary of the student results."""
        status = "passed" if self.passed_all else "failed"
        return (
            f"{self.name}: 100 m = {self.sprint_seconds:.1f} s, "
            f"long jump = {self.long_jump_cm} cm, status = {status}"
        )
