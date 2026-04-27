"""Console interface for task 6.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-27
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import LabTask
from app.task6.models import DatasetInfo
from app.task6.service import NetflixStockDataset


class Task6Runner(LabTask):
    """Interactive runner for task 6."""

    task_name = "Task 6 - Pandas and Netflix Stock"

    def run(self, **kwargs: object) -> None:
        """Run both required parts of task 6 for variant 7."""
        dataset_path = Path("data/task6/netflix_stock.csv")
        if not dataset_path.exists():
            print("Dataset file was not found: data/task6/netflix_stock.csv")
            return

        dataset = NetflixStockDataset(DatasetInfo("Netflix Stock", dataset_path))
        dataset.load()

        volume_series = dataset.task_a_series()
        high_mean, low_mean, ratio, thresholds = dataset.statistical_ratio()

        dataset.display_object(dataset.short_preview(), "Dataset preview")
        dataset.display_object(dataset.dtypes_series(), "Column types")
        dataset.display_object(dataset.null_counts(), "Missing values")
        dataset.display_object(dataset.describe_numeric(), "Numeric statistics")
        dataset.display_object(volume_series.tail(), "Task A - volume_series with appended average")

        report_lines = [
            "Task 6 report",
            "=" * 50,
            "Dataset: Netflix Stock",
            f"Rows loaded: {len(dataset)}",
            "",
            "Task A:",
            f"Average volume: {volume_series.loc['average']:.2f}",
            "",
            "Task B:",
            f"Close 5th percentile: {thresholds.low_percentile:.4f}",
            f"Close 95th percentile: {thresholds.high_percentile:.4f}",
            f"Average volume for Close > 95th percentile: {high_mean:.2f}",
            f"Average volume for Close < 5th percentile: {low_mean:.2f}",
            f"Ratio: {ratio:.2f}",
            "",
            "DataFrame info:",
            dataset.dataframe_info_text(),
        ]

        report_path = Path("data/task6/report.txt")
        report_path.write_text("\n".join(report_lines), encoding="utf-8")

        print("\nTask B result:")
        print(f"Average volume in high Close days: {high_mean:.2f}")
        print(f"Average volume in low Close days: {low_mean:.2f}")
        print(f"Required ratio: {ratio:.2f}")
        print(f"\nReport file: {report_path}")
