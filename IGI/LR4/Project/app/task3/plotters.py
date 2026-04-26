"""Plot builders for task 3.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.task3.models import SeriesPoint


class PlotBuilder(ABC):
    """Base class for graph builders."""

    @abstractmethod
    def build(
        self,
        file_path: Path,
        points: list[SeriesPoint],
        function_title: str,
        show_plot: bool = False,
    ) -> str:
        """Create a graph file and return a status message."""


class MatplotlibPlotBuilder(PlotBuilder):
    """Build a graph with matplotlib."""

    def build(
        self,
        file_path: Path,
        points: list[SeriesPoint],
        function_title: str,
        show_plot: bool = False,
    ) -> str:
        """Save a PNG graph and optionally show it on screen."""

        import matplotlib.pyplot as plt

        x_values = [point.x for point in points]
        series_values = [point.series_value for point in points]
        math_values = [point.math_value for point in points]
        max_error_point = max(points, key=lambda point: point.absolute_error)

        plt.figure(figsize=(10, 6))
        plt.plot(x_values, series_values, color="royalblue", marker="o", label="Series F(x)")
        plt.plot(x_values, math_values, color="darkorange", marker="s", label="math F(x)")
        plt.axhline(0, color="black", linewidth=0.8)
        plt.axvline(0, color="black", linewidth=0.8)
        plt.title(f"Variant 7 series graph: {function_title}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.text(x_values[0], max(math_values), "Series and exact function", fontsize=10)
        plt.annotate(
            f"Max error = {max_error_point.absolute_error:.2e}",
            xy=(max_error_point.x, max_error_point.series_value),
            xytext=(max_error_point.x, max_error_point.series_value + 0.25),
            arrowprops={"arrowstyle": "->", "color": "black"},
        )
        plt.tight_layout()
        plt.savefig(file_path, dpi=150)
        show_message = " The graph window was not opened."
        if show_plot:
            try:
                plt.show()
                show_message = " The graph window was opened."
            except Exception:
                show_message = " GUI is unavailable, graph saved without opening a window."
        plt.close()
        return f"Graph saved with matplotlib to {file_path}.{show_message}"


