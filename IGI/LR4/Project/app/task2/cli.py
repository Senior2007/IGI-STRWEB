"""Console interface for task 2.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import LabTask
from app.common.io_utils import InputHelper
from app.task2.analyzers import (
    IpAddressRule,
    LowercaseDigitWordsRule,
    ShortestWordEndingWithWRule,
    ShortWordsCountRule,
    TextStatisticsCalculator,
    WordsSortedByLengthRule,
)
from app.task2.archive_utils import ResultArchiver
from app.task2.models import TextDocument


class Task2Runner(LabTask):
    """Interactive runner for task 2."""

    task_name = "Task 2 - Text analysis and archiving"

    def run(self, **kwargs: object) -> None:
        """Analyze the source text and archive the result file."""
        source_document = TextDocument(Path("data/task2/source_text.txt"))
        result_document = TextDocument(Path("data/task2/result.txt"))
        statistics_document = TextDocument(Path("data/task2/statistics.txt"))
        source_text = source_document.read()
        ip_candidate = InputHelper.ask_text("Enter a string to check as an IP address: ")

        text_rules = [
            LowercaseDigitWordsRule(),
            ShortWordsCountRule(),
            ShortestWordEndingWithWRule(),
            WordsSortedByLengthRule(),
        ]

        report_lines = ["Task 2 report", "=" * 40, "Source text:", source_text, ""]
        for rule in text_rules:
            report_lines.append(f"{rule.title}: {rule.apply(source_text)}")

        ip_rule = IpAddressRule()
        report_lines.append(f"{ip_rule.title}: {ip_rule.apply(ip_candidate)}")

        report_text = "\n".join(report_lines)
        result_document.write(report_text)
        statistics_lines = TextStatisticsCalculator.build_report_lines(source_text)
        statistics_text = "\n".join(statistics_lines)
        statistics_document.write(statistics_text)

        archive_path = Path("data/task2/result.zip")
        archiver = ResultArchiver(archive_path)
        archiver.archive(result_document.path)

        print("\n" + report_text)
        print("\n" + statistics_text)
        print("\nArchive info:")
        print(archiver.get_info())
        print(f"\nResult file saved to: {result_document.path}")
        print(f"Statistics file saved to: {statistics_document.path}")
        print(f"Archive saved to: {archive_path}")
