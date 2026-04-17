"""Renderers for task 4.

Lab work: LR4 - Files, classes, serializers, regular expressions and standard libraries.
Version: 1.0.0
Developer: Lozhachnik
Date: 2026-04-17
"""

from __future__ import annotations

import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from app.task4.models import RegularHexagon


def _normalize_points(points: list[tuple[float, float]], canvas_size: int = 420, padding: int = 40) -> list[tuple[float, float]]:
    """Move the figure points into the drawing area."""
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    scale = min((canvas_size - 2 * padding) / width, (canvas_size - 2 * padding) / height)
    centered = []
    for x, y in points:
        normalized_x = (x - min(xs)) * scale + padding
        normalized_y = (y - min(ys)) * scale + padding
        centered.append((normalized_x, normalized_y))
    return centered


class FigureRenderer(ABC):
    """Abstract renderer for a geometric figure."""

    @abstractmethod
    def render(self, figure: RegularHexagon, output_path: Path | None = None) -> str:
        """Render the figure and return a status message."""


class SvgRenderer(FigureRenderer):
    """SVG file renderer."""

    def render(self, figure: RegularHexagon, output_path: Path | None = None) -> str:
        """Render the figure into an SVG file."""
        if output_path is None:
            raise ValueError("SVG renderer requires an output path.")

        points = _normalize_points(figure.vertices())
        polygon_points = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        svg_text = f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"420\" height=\"420\" viewBox=\"0 0 420 420\">\n  <rect width=\"100%\" height=\"100%\" fill=\"white\" />\n  <polygon points=\"{polygon_points}\" fill=\"{figure.color.name}\" stroke=\"black\" stroke-width=\"3\" />\n  <text x=\"210\" y=\"400\" text-anchor=\"middle\" font-size=\"20\" font-family=\"Helvetica\">{figure.label}</text>\n</svg>\n"""
        output_path.write_text(svg_text, encoding="utf-8")
        return f"Figure saved to {output_path}"


class TkRenderer(FigureRenderer):
    """Renderer that displays the figure in a small Tk window."""

    def render(self, figure: RegularHexagon, output_path: Path | None = None) -> str:
        """Show the figure in a window if a GUI is available."""
        points = _normalize_points(figure.vertices())
        flat_points = [coordinate for point in points for coordinate in point]
        child_code = f"""
import tkinter as tk

flat_points = {flat_points!r}
root = tk.Tk()
root.title({figure.get_figure_name()!r})
canvas = tk.Canvas(root, width=420, height=420, bg='white')
canvas.pack()
canvas.create_polygon(flat_points, fill={figure.color.name!r}, outline='black', width=3)
canvas.create_text(210, 395, text={figure.label!r}, font=('Helvetica', 16))
root.after(2500, root.destroy)
root.mainloop()
"""
        try:
            completed = subprocess.run(
                [sys.executable, "-c", child_code],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return "GUI window did not close in time. The SVG file was still created."

        if completed.returncode != 0:
            return "GUI display is unavailable in the current environment. The SVG file was created successfully."
        return "Figure displayed on the screen."
