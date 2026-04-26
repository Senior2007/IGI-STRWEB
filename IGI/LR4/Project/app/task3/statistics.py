"""Statistics helpers for task 3.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path

from app.task3.models import SeriesPoint


class SequenceStatistics:
    """Compute descriptive statistics for a numeric sequence."""

    def __init__(self, values: list[float]) -> None:
        """Store the source values."""
        self.values = values

    def mean(self) -> float:
        """Return the arithmetic mean."""
        return statistics.fmean(self.values)

    def median(self) -> float:
        """Return the sequence median."""
        return statistics.median(self.values)

    def mode_text(self) -> str:
        """Return the mode or a message when it does not exist."""
        rounded = [round(value, 10) for value in self.values]
        modes = statistics.multimode(rounded)
        if not modes or len(modes) == len(set(rounded)):
            return "No mode"
        return ", ".join(f"{value:.10f}" for value in modes)

    def variance(self) -> float:
        """Return the population variance."""
        mean_value = self.mean()
        return sum((value - mean_value) ** 2 for value in self.values) / len(self.values)

    def standard_deviation(self) -> float:
        """Return the population standard deviation."""
        return math.sqrt(self.variance())


class SeriesReportWriter:
    """Save the computed table and statistics to files."""

    @staticmethod
    def save_table(file_path: Path, points: list[SeriesPoint]) -> None:
        """Save the series table to a CSV file."""
        with file_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["x", "n", "F(x)", "Math F(x)", "eps", "abs_error"])
            for point in points:
                writer.writerow([
                    f"{point.x:.6f}",
                    point.terms_used,
                    f"{point.series_value:.10f}",
                    f"{point.math_value:.10f}",
                    f"{point.epsilon:.10f}",
                    f"{point.absolute_error:.10f}",
                ])

    @staticmethod
    def save_report(file_path: Path, points: list[SeriesPoint], stats: SequenceStatistics, function_title: str) -> None:
        """Save a human-readable report to a text file."""
        lines = [
            "Task 3 report",
            "=" * 50,
            f"Function: {function_title}",
            "",
            "Table:",
            "x | n | F(x) | Math F(x) | eps | abs_error",
        ]
        for point in points:
            lines.append(
                f"{point.x:.3f} | {point.terms_used} | {point.series_value:.10f} | "
                f"{point.math_value:.10f} | {point.epsilon:.6f} | {point.absolute_error:.10f}"
            )

        lines.extend(
            [
                "",
                "Sequence statistics for F(x):",
                f"Mean: {stats.mean():.10f}",
                f"Median: {stats.median():.10f}",
                f"Mode: {stats.mode_text()}",
                f"Variance: {stats.variance():.10f}",
                f"Standard deviation: {stats.standard_deviation():.10f}",
            ]
        )
        file_path.write_text("\n".join(lines), encoding="utf-8")
