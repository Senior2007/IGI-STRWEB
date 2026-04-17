"""Regex analyzers for task 2.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod


class RegexRule(ABC):
    """Base class for a regex-based analysis rule."""

    title = "Base regex rule"

    @abstractmethod
    def apply(self, text: str) -> str:
        """Apply the rule to the given text and return a report line."""


class LowercaseDigitWordsRule(RegexRule):
    """Find words that include lowercase letters and digits."""

    title = "Words with lowercase letters and digits"

    def apply(self, text: str) -> str:
        """Return matching words."""
        matches = re.findall(r"\b(?=[a-z0-9]*[a-z])(?=[a-z0-9]*\d)[a-z0-9]+\b", text)
        return ", ".join(matches) if matches else "No matches found"


class ShortWordsCountRule(RegexRule):
    """Count words shorter than six characters."""

    title = "Number of words shorter than 6 symbols"

    def apply(self, text: str) -> str:
        """Return the count of short words."""
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        count = sum(1 for word in words if len(word) < 6)
        return str(count)


class ShortestWordEndingWithWRule(RegexRule):
    """Find the shortest word ending with the letter w."""

    title = "Shortest word ending with 'w'"

    def apply(self, text: str) -> str:
        """Return the shortest matching word."""
        words = re.findall(r"\b[a-zA-Z]*w\b", text, flags=re.IGNORECASE)
        if not words:
            return "No such word found"
        return min(words, key=lambda word: (len(word), word.lower()))


class WordsSortedByLengthRule(RegexRule):
    """Sort words by length in ascending order."""

    title = "Words in ascending order of length"

    def apply(self, text: str) -> str:
        """Return sorted words."""
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        ordered = sorted(words, key=lambda word: (len(word), word.lower()))
        return ", ".join(ordered) if ordered else "No words found"


class IpAddressRule(RegexRule):
    """Validate a decimal IPv4 address."""

    title = "Entered string is a decimal IPv4 address"

    def apply(self, text: str) -> str:
        """Return whether the input string is a valid IPv4 address."""
        pattern = re.compile(
            r"^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
            r"\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
            r"\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
            r"\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
        )
        return "Yes" if pattern.fullmatch(text.strip()) else "No"
