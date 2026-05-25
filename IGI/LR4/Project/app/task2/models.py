"""Models for task 2 text analysis.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path

from app.common.mixins import PositiveValueMixin


class TextDocument(PositiveValueMixin):
    """Represent a text document used in analysis."""

    def __init__(self, path: Path) -> None:
        """Store the file path."""
        self._path = path

    @property
    def path(self) -> Path:
        """Return the file path."""
        return self._path

    def read(self) -> str:
        """Read and return the document text."""
        return self.path.read_text(encoding="utf-8")

    def write(self, text: str) -> None:
        """Write text to the document file."""
        self.path.write_text(text, encoding="utf-8")
