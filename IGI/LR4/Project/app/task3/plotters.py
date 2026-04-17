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
    def build(self, file_path: Path, points: list[SeriesPoint], function_title: str) -> str:
        """Create a graph file and return a status message."""


class MatplotlibPlotBuilder(PlotBuilder):
    """Build a graph with matplotlib when the library is available."""

    def build(self, file_path: Path, points: list[SeriesPoint], function_title: str) -> str:
        """Save a PNG graph with matplotlib."""
        import matplotlib

        matplotlib.use("Agg")
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
        plt.close()
        return f"Graph saved with matplotlib to {file_path}"


class SvgPlotBuilder(PlotBuilder):
    """Fallback SVG plot builder when matplotlib is unavailable."""

    width = 900
    height = 520
    padding = 60

    def _scale_x(self, x_value: float, x_min: float, x_max: float) -> float:
        """Scale x into the SVG viewbox."""
        if x_max == x_min:
            return self.width / 2
        return self.padding + (x_value - x_min) * (self.width - 2 * self.padding) / (x_max - x_min)

    def _scale_y(self, y_value: float, y_min: float, y_max: float) -> float:
        """Scale y into the SVG viewbox."""
        if y_max == y_min:
            return self.height / 2
        return self.height - self.padding - (y_value - y_min) * (self.height - 2 * self.padding) / (y_max - y_min)

    def build(self, file_path: Path, points: list[SeriesPoint], function_title: str) -> str:
        """Save an SVG graph file without external libraries."""
        x_values = [point.x for point in points]
        series_values = [point.series_value for point in points]
        math_values = [point.math_value for point in points]
        all_y = series_values + math_values
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(all_y), max(all_y)
        if y_min == y_max:
            y_min -= 1
            y_max += 1

        series_points = " ".join(
            f"{self._scale_x(point.x, x_min, x_max):.2f},{self._scale_y(point.series_value, y_min, y_max):.2f}"
            for point in points
        )
        math_points = " ".join(
            f"{self._scale_x(point.x, x_min, x_max):.2f},{self._scale_y(point.math_value, y_min, y_max):.2f}"
            for point in points
        )

        axis_x = self._scale_y(0, y_min, y_max)
        axis_y = self._scale_x(0, x_min, x_max)
        svg_text = f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{self.width}\" height=\"{self.height}\" viewBox=\"0 0 {self.width} {self.height}\">\n  <rect width=\"100%\" height=\"100%\" fill=\"white\" />\n  <line x1=\"{self.padding}\" y1=\"{axis_x:.2f}\" x2=\"{self.width - self.padding}\" y2=\"{axis_x:.2f}\" stroke=\"black\" stroke-width=\"1\" />\n  <line x1=\"{axis_y:.2f}\" y1=\"{self.padding}\" x2=\"{axis_y:.2f}\" y2=\"{self.height - self.padding}\" stroke=\"black\" stroke-width=\"1\" />\n  <polyline fill=\"none\" stroke=\"royalblue\" stroke-width=\"2\" points=\"{series_points}\" />\n  <polyline fill=\"none\" stroke=\"darkorange\" stroke-width=\"2\" points=\"{math_points}\" />\n  <text x=\"{self.padding}\" y=\"30\" font-size=\"22\" font-family=\"Helvetica\">Variant 7 graph: {function_title}</text>\n  <text x=\"{self.padding}\" y=\"55\" font-size=\"16\" font-family=\"Helvetica\" fill=\"royalblue\">Series F(x)</text>\n  <text x=\"{self.padding + 140}\" y=\"55\" font-size=\"16\" font-family=\"Helvetica\" fill=\"darkorange\">math F(x)</text>\n  <text x=\"{self.width - 110}\" y=\"{self.height - 20}\" font-size=\"16\" font-family=\"Helvetica\">x</text>\n  <text x=\"20\" y=\"{self.padding}\" font-size=\"16\" font-family=\"Helvetica\">y</text>\n</svg>\n"""
        file_path.write_text(svg_text, encoding="utf-8")
        return f"Matplotlib is unavailable, fallback SVG graph saved to {file_path}"


class PlotFactory:
    """Choose the best available plot builder."""

    @staticmethod
    def create() -> PlotBuilder:
        """Return matplotlib builder or fallback SVG builder."""
        try:
            import matplotlib  # noqa: F401
        except Exception:
            return SvgPlotBuilder()
        return MatplotlibPlotBuilder()
