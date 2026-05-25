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


class TextStatisticsCalculator:
    """Calculate common sentence and word statistics for a text."""

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        """Split text into non-empty sentences by terminal punctuation."""
        return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]

    @staticmethod
    def _words(text: str) -> list[str]:
        """Return words used for length-based statistics."""
        return re.findall(r"\b[0-9A-Za-zА-Яа-яЁё]+\b", text)

    @staticmethod
    def _smiley_count(text: str) -> int:
        """Count smileys matching the lab specification."""
        pattern = re.compile(r"[:;]-*(?:\(+|\)+|\[+|\]+)")
        return len(pattern.findall(text))

    @classmethod
    def build_report_lines(cls, text: str) -> list[str]:
        """Build formatted report lines with common text statistics."""
        sentences = cls._split_sentences(text)
        declarative = sum(1 for sentence in sentences if sentence.endswith("."))
        interrogative = sum(1 for sentence in sentences if sentence.endswith("?"))
        imperative = sum(1 for sentence in sentences if sentence.endswith("!"))

        sentence_word_lengths: list[int] = []
        for sentence in sentences:
            sentence_words = cls._words(sentence)
            sentence_word_lengths.append(sum(len(word) for word in sentence_words))

        all_words = cls._words(text)
        average_sentence_length = (
            sum(sentence_word_lengths) / len(sentence_word_lengths)
            if sentence_word_lengths
            else 0.0
        )
        average_word_length = (
            sum(len(word) for word in all_words) / len(all_words)
            if all_words
            else 0.0
        )
        smiley_count = cls._smiley_count(text)

        return [
            "Additional common statistics:",
            f"Total number of sentences: {len(sentences)}",
            (
                "Number of sentences by type "
                f"(declarative/interrogative/imperative): "
                f"{declarative}/{interrogative}/{imperative}"
            ),
            f"Average sentence length in symbols (words only): {average_sentence_length:.2f}",
            f"Average word length in symbols: {average_word_length:.2f}",
            f"Number of smileys in text: {smiley_count}",
        ]
