"""Console input and output helpers for laboratory work 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path


class InputHelper:
    """Helper with safe console input methods."""

    @staticmethod
    def ask_text(prompt: str, allow_empty: bool = False) -> str:
        """Ask the user for a text value and validate it."""
        while True:
            value = input(prompt).strip()
            if value or allow_empty:
                return value
            print("Input cannot be empty. Please try again.")

    @staticmethod
    def ask_int(prompt: str, minimum: int | None = None) -> int:
        """Ask the user for an integer value."""
        while True:
            try:
                value = int(input(prompt).strip())
                if minimum is not None and value < minimum:
                    print(f"The value must be at least {minimum}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid integer.")

    @staticmethod
    def ask_float(prompt: str, minimum: float | None = None) -> float:
        """Ask the user for a floating-point value."""
        while True:
            raw_value = input(prompt).strip().replace(",", ".")
            try:
                value = float(raw_value)
                if minimum is not None and value < minimum:
                    print(f"The value must be at least {minimum}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def ask_choice(prompt: str, choices: set[str]) -> str:
        """Ask the user for a value from a fixed set."""
        normalized = {item.lower() for item in choices}
        while True:
            value = input(prompt).strip().lower()
            if value in normalized:
                return value
            print(f"Please enter one of the following values: {', '.join(sorted(normalized))}.")

    @staticmethod
    def ensure_directory(path: Path) -> Path:
        """Create the directory if it does not exist."""
        path.mkdir(parents=True, exist_ok=True)
        return path
