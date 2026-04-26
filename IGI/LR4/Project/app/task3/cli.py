"""Console interface for task 3.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from pathlib import Path

from app.common.base import LabTask
from app.common.io_utils import InputHelper
from app.task3.models import CosineSeries
from app.task3.plotters import MatplotlibPlotBuilder
from app.task3.statistics import SequenceStatistics, SeriesReportWriter


class Task3Runner(LabTask):
    """Interactive runner for task 3."""

    task_name = "Task 3 - Series and graph"

    @staticmethod
    def _build_x_values(start_x: float, end_x: float, step: float) -> list[float]:
        """Build a list of x values for the table."""
        values: list[float] = []
        current = start_x
        while current <= end_x + 1e-12:
            values.append(round(current, 10))
            current += step
        return values

    def run(self, **kwargs: object) -> None:
        """Compute a series table, sequence statistics and a graph file."""
        print("Task 3: cos(x) series.")
        start_x = InputHelper.ask_float("Enter the start value x_start: ")
        end_x = InputHelper.ask_float("Enter the end value x_end: ")
        while end_x < start_x:
            print("The end value must be greater than or equal to the start value.")
            end_x = InputHelper.ask_float("Enter the end value x_end: ")

        step = InputHelper.ask_float("Enter the step value: ", minimum=0.000001)
        epsilon = InputHelper.ask_float("Enter epsilon: ", minimum=0.0000000001)

        function = CosineSeries(epsilon)
        x_values = self._build_x_values(start_x, end_x, step)
        points = [function.calculate_point(x_value) for x_value in x_values]
        stats = SequenceStatistics([point.series_value for point in points])

        output_dir = Path("data/task3")
        output_dir.mkdir(parents=True, exist_ok=True)
        table_path = output_dir / "series_table.csv"
        report_path = output_dir / "report.txt"

        plot_builder = MatplotlibPlotBuilder()
        graph_path = output_dir / "graph.png"

        SeriesReportWriter.save_table(table_path, points)
        SeriesReportWriter.save_report(report_path, points, stats, function.get_title())
        plot_message = plot_builder.build(graph_path, points, function.get_title(), show_plot=True)

        print("\nComputed table:")
        print("x | n | F(x) | Math F(x) | eps | abs_error")
        for point in points:
            print(
                f"{point.x:.3f} | {point.terms_used} | {point.series_value:.10f} | "
                f"{point.math_value:.10f} | {point.epsilon:.6f} | {point.absolute_error:.10f}"
            )

        print("\nSequence statistics for F(x):")
        print(f"Mean: {stats.mean():.10f}")
        print(f"Median: {stats.median():.10f}")
        print(f"Mode: {stats.mode_text()}")
        print(f"Variance: {stats.variance():.10f}")
        print(f"Standard deviation: {stats.standard_deviation():.10f}")

        print(f"\nTable file: {table_path}")
        print(f"Report file: {report_path}")
        print(plot_message)
